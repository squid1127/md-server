"""Main application module and user-facing endpoints."""

import os
from fastapi import FastAPI, Request, Response
from dotenv import load_dotenv
from contextlib import asynccontextmanager

from .static import static_files
from .templates import templates
from .constants import APP_NAME, HOME_PAGE
from .md import render_md_page
from .logging_config import setup_logging, get_logger
from .middleware import RequestLoggingMiddleware, NoCacheMiddleware
from .api import router as api_router


load_dotenv()  # Load environment variables from a .env file if present
setup_logging()  # Configure logging

logger = get_logger(__name__)

# Lifespan event to initialize database connection
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager to handle startup and shutdown events."""
    logger.info("Application startup: initializing database")
    try:
        from .db import init_db
        await init_db()
        logger.info("Database initialization completed successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise
    
    yield
    
    logger.info("Application shutdown: cleaning up resources")
    # Any shutdown code can go here if needed

# Initialize FastAPI application
app = FastAPI(title=APP_NAME, version="0.1.0", lifespan=lifespan)

app.mount("/static", static_files)
app.include_router(api_router, prefix="/api")
app.add_middleware(RequestLoggingMiddleware)
# Optionally add NoCacheMiddleware based on environment variable
if os.getenv("NO_CACHE", "false").lower() == "true":
    app.add_middleware(NoCacheMiddleware)
# app.mount("/templates", templates)

logger.info(f"Starting {APP_NAME} v0.1.0")

# User-facing endpoints
@app.get("/")
async def read_root(request: Request):
    """Render the index page using the HOME_PAGE markdown content.
    """
    logger.info(f"Home page requested from {request.client.host}")
    try:
        return render_md_page(HOME_PAGE, request=request, title="Home")
    except Exception as e:
        logger.error(f"Error rendering home page: {e}")
        raise

@app.get("/d/{md_id}")
async def read_markdown(md_id: str, request: Request):
    """Read and render a markdown document by its ID."""
    logger.info(f"Markdown document requested: {md_id} from {request.client.host}")
    
    try:
        from .db import get_markdown_document
        document = await get_markdown_document(md_id)
        if not document:
            logger.warning(f"Document not found: {md_id}")
            return templates.TemplateResponse("404.html", {"request": request, "md_id": md_id}, status_code=404)
        
        return render_md_page(document.content, request=request, title=document.title)
    except Exception as e:
        logger.error(f"Error rendering markdown document {md_id}: {e}")
        raise
    
@app.get("/raw/{md_id}")
async def read_raw_markdown(md_id: str):
    """Fetch the raw markdown content of a document by its ID."""
    logger.info(f"Raw markdown requested: {md_id}")
    
    try:
        from .db import get_markdown_document
        document = await get_markdown_document(md_id)
        if not document:
            logger.warning(f"Document not found: {md_id}")
            return {"error": "Document not found"}, 404
        
        return Response(content=document.content, media_type="text/markdown")
    except Exception as e:
        logger.error(f"Error fetching raw markdown document {md_id}: {e}")
        raise
    
@app.get("/render")
async def render_markdown_endpoint(request: Request):
    """Render arbitrary markdown content provided via query parameter."""
    logger.info(f"Arbitrary markdown rendering requested from {request.client.host}")

    md = request.query_params.get("md", "")
    title = request.query_params.get("title", "Document")
    try:
        return render_md_page(md, request=request, title=title)
    except Exception as e:
        logger.error(f"Error rendering arbitrary markdown: {e}")
        raise
    
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}
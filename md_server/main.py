"""Main application module and user-facing endpoints."""

import os
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, PlainTextResponse
from dotenv import load_dotenv
from contextlib import asynccontextmanager

from .static import static_files
from .templates import templates
from .constants import APP_NAME, HOME_PAGE, APP_SOURCE
from .md import render_md_page, render_markdown
from .logging_config import setup_logging, get_logger
from .middleware import RequestLoggingMiddleware, NoCacheMiddleware
from .api import router as api_router
from .dashboard import router as dashboard_router


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
app.include_router(dashboard_router, prefix="/dash")
app.add_middleware(RequestLoggingMiddleware)
# Optionally add NoCacheMiddleware based on environment variable
if os.getenv("NO_CACHE", "false").lower() == "true":
    app.add_middleware(NoCacheMiddleware)
# app.mount("/templates", templates)

logger.info(f"Starting {APP_NAME} v0.1.0")


# User-facing endpoints
@app.get("/", tags=["UI"], name="Home", response_class=HTMLResponse)
async def read_root(request: Request):
    """Render the index page using the HOME_PAGE markdown content."""
    logger.info(f"Home page requested from {request.client.host}")
    try:
        return render_md_page(
            HOME_PAGE,
            request=request,
            title="Home",
            source=APP_SOURCE,
        )
    except Exception as e:
        logger.error(f"Error rendering home page: {e}")
        raise


@app.get(
    "/d/{md_id}",
    tags=["UI", "Render", "Document"],
    name="Render Markdown Document",
    response_class=HTMLResponse,
)
async def read_markdown(md_id: str, request: Request):
    """Read and render a markdown document by its ID."""
    logger.info(f"Markdown document requested: {md_id} from {request.client.host}")

    try:
        from .db import get_markdown_document

        document = await get_markdown_document(md_id)
        if not document:
            logger.warning(f"Document not found: {md_id}")
            return templates.TemplateResponse(
                "404.html",
                {
                    "request": request,
                    "md_id": md_id,
                    "app_name": APP_NAME,
                    "page_title": "[?]",
                },
                status_code=404,
            )

        return render_md_page(
            document.content,
            request=request,
            title=document.title,
            md_id=md_id,
        )
    except Exception as e:
        logger.error(f"Error rendering markdown document {md_id}: {e}")
        raise


@app.get(
    "/raw/{md_id}",
    tags=["UI"],
    name="Raw Markdown Document",
    response_class=PlainTextResponse,
)
async def read_raw_markdown(md_id: str):
    """Fetch the raw markdown content of a document by its ID."""
    logger.info(f"Raw markdown requested: {md_id}")

    try:
        from .db import get_markdown_document

        document = await get_markdown_document(md_id)
        if not document:
            logger.warning(f"Document not found: {md_id}")
            return Response(
                content="Document not found", status_code=404, media_type="text/plain"
            )

        return Response(content=document.content, media_type="text/markdown")
    except Exception as e:
        logger.error(f"Error fetching raw markdown document {md_id}: {e}")
        raise


@app.get(
    "/editor",
    tags=["UI"],
    name="Interactive Markdown Editor",
    response_class=HTMLResponse,
)
async def editor(request: Request):
    """Render the editor page."""
    logger.info(f"Editor page requested from {request.client.host}")
    try:
        return templates.TemplateResponse(
            "editor.html",
            {
                "request": request,
                "app_name": APP_NAME,
                "page_title": "Editor",
                "initial_width_index": 1,  # Default to medium width (More space because dual panes)
            },
        )
    except Exception as e:
        logger.error(f"Error rendering editor page: {e}")
        raise


@app.get(
    "/render",
    tags=["UI", "Render"],
    name="Render document page from query",
    response_class=HTMLResponse,
)
async def render_markdown_endpoint(
    request: Request, md: str = "", title: str = "Document"
):
    """Render arbitrary markdown content provided via query parameter."""
    logger.info(f"Arbitrary markdown rendering requested from {request.client.host}")

    try:
        return render_md_page(md, request=request, title=title)
    except Exception as e:
        logger.error(f"Error rendering arbitrary markdown: {e}")
        raise


@app.post(
    "/render-embed",
    tags=["API", "Render"],
    name="Render HTML from a JSON body",
    response_class=HTMLResponse,
)
async def render_markdown_embed(request: Request):
    """Render markdown content provided in json body."""
    logger.info(f"Embedded markdown rendering requested from {request.client.host}")

    try:
        data = await request.json()
        md = data.get("md", "")
        return render_markdown(md)
    except Exception as e:
        logger.error(f"Error rendering embedded markdown: {e}")
        raise


@app.get("/health", tags=["UI"])
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}

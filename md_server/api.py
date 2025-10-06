"""
API module for the markdown server.
"""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from starlette.status import HTTP_401_UNAUTHORIZED
from .auth import verify_api_key
from .constants import HOME_PAGE
from .md import render_md_page
from .logging_config import get_logger

logger = get_logger(__name__)
router = APIRouter()

@router.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    logger.info("Health check requested")
    return {"status": "ok"}

@router.post("/new", tags=["API Key"])
async def new_markdown_document(request: Request, api_key=Depends(verify_api_key)):
    """
    Create a new markdown document with default content.
    Requires a valid API key.
    
    Body Parameters (JSON):
    - title: Title of the markdown document (default: "Untitled")
    - content: Content of the markdown document (default: "")
    """
    logger.info(f"API key verified for request from {request.client.host}")
   
    # Parse request body
    try:
        body = await request.json()
        title = body.get("title", "Untitled")
        content = body.get("content", "")
    except Exception as e:
        logger.error(f"Error parsing request body: {e}")
        return JSONResponse(status_code=400, content={"error": "Invalid request body"})
    
    try:
        from .db import create_markdown_document
        document = await create_markdown_document(title=title, content=content)
        logger.info(f"New markdown document created with ID: {document.doc_id}")
        return {
            "id": str(document.doc_id),
            "title": document.title,
            "content": document.content,
            "created_at": document.created_at.isoformat()
        }
    except Exception as e:
        logger.error(f"Error creating markdown document: {e}")
        return JSONResponse(status_code=500, content={"error": "Failed to create document"})
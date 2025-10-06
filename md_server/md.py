"""Markdown Handler for the Markdown Server."""

import mistune

from fastapi import Request
from md_server.constants import APP_NAME
from md_server.templates import templates
from .logging_config import get_logger

logger = get_logger(__name__)

markdown = mistune.create_markdown("html")


def render_markdown(md_text: str) -> str:
    """Render markdown text to HTML using Mistune.

    Args:
        md_text (str): The markdown text to render.

    Returns:
        str: The rendered HTML.
    """
    logger.debug(f"Rendering markdown content of length: {len(md_text)}")
    
    if not md_text.strip():
        logger.warning("Empty markdown content provided")
        return f"<p> This document has no content. </p><p> - {APP_NAME} </p>"
    
    try:
        html = markdown(md_text)
        logger.debug("Markdown rendering completed successfully")
        return html
    except Exception as e:
        logger.error(f"Error rendering markdown: {e}")
        return f"<p>Error rendering markdown content.</p><p> - {APP_NAME} </p>"


def render_md_page(md_text: str, title: str = None, request: Request = None) -> str:
    """Render a full HTML page with the given markdown content.

    Args:
        md_text (str): The markdown text to render.
        title (str): The title of the page.
        request (Request): The FastAPI request object.

    Returns:
        str: The complete HTML page with rendered markdown.
    """
    logger.info(f"Rendering page: {title or 'Untitled'}")
    
    try:
        html_content = render_markdown(md_text)
        response = templates.TemplateResponse(
            "markdown.html",
            {
                "page_title": title,
                "markdown_content": html_content,
                "app_name": APP_NAME,
                "request": request,
            },
        )
        logger.debug(f"Page rendered successfully: {title or 'Untitled'}")
        return response
    except Exception as e:
        logger.error(f"Error rendering page '{title or 'Untitled'}': {e}")
        raise

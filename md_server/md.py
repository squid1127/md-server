"""Markdown Renderer using markdown-it-py with useful plugins."""

# Markdown imports
from markdown_it import MarkdownIt
from mdit_py_plugins.tasklists import tasklists_plugin
from mdit_py_plugins.anchors import anchors_plugin
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.admon import admon_plugin

# Actually needed imports
from fastapi import Request
import os
from md_server.constants import APP_NAME
from md_server.templates import templates
from .logging_config import get_logger

# Prism.js-compatible code block formatting
def highlight_code(code: str, lang: str | None) -> str:
    """Format code blocks for Prism.js client-side highlighting."""
    # Return raw code - Prism.js will handle the highlighting on the client side
    # This is much faster than server-side highlighting
    lang_class = f"language-{lang}" if lang else "language-text"
    return f'<pre><code class="{lang_class}">{code}</code></pre>'

logger = get_logger(__name__)
md = MarkdownIt("gfm-like", {"html": True, "linkify": False, "typographer": True})
# Attach a highlight function for Prism.js compatibility
md.options["highlight"] = lambda code, lang, _: highlight_code(code, lang)

# Add useful plugins
md.use(tasklists_plugin)      # task lists: - [ ] / - [x]
md.use(anchors_plugin)        # heading anchors/permalinks
md.use(front_matter_plugin)   # front matter parsing (if you want it)
md.use(admon_plugin)          # admonitions: !!! note/warning etc.

def get_name() -> str:
    """
    Get the app name from environment or use default.
    """
    return os.getenv("APP_NAME", APP_NAME)

def render_markdown(md_text: str) -> str:
    """Render markdown text to HTML using Markdown-it.

    Args:
        md_text (str): The markdown text to render.

    Returns:
        str: The rendered HTML.
    """
    logger.debug(f"Rendering markdown content of length: {len(md_text)}")
    
    if not md_text.strip():
        logger.warning("Empty markdown content provided")
        return f"<p> This document has no content. </p>"
    
    try:
        html = md.render(md_text)
        logger.debug("Markdown rendering completed successfully")
        return html
    except Exception as e:
        logger.error(f"Error rendering markdown: {e}")
        return f"<p>Error rendering markdown content.</p>"


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
                "app_name": get_name(),
                "request": request,
            },
        )
        logger.debug(f"Page rendered successfully: {title or 'Untitled'}")
        return response
    except Exception as e:
        logger.error(f"Error rendering page '{title or 'Untitled'}': {e}")
        raise

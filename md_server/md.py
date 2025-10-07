"""Markdown Handler for the Markdown Server."""

# Bruh there's so many markdown imports
from markdown_it import MarkdownIt
from mdit_py_plugins.tasklists import tasklists_plugin
from mdit_py_plugins.anchors import anchors_plugin
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.admon import admon_plugin
from pygments import highlight
from pygments.lexers import get_lexer_by_name, TextLexer
from pygments.formatters import HtmlFormatter

# Actually needed imports
from fastapi import Request
from md_server.constants import APP_NAME
from md_server.templates import templates
from .logging_config import get_logger

# Pygments highlight function
def highlight_code(code: str, lang: str | None) -> str:
    try:
        lexer = get_lexer_by_name(lang) if lang else TextLexer()
    except Exception:
        lexer = TextLexer()
    formatter = HtmlFormatter(nowrap=True)
    return highlight(code, lexer, formatter)

logger = get_logger(__name__)
md = MarkdownIt("gfm-like", {"html": True, "linkify": False, "typographer": True})
# Attach a highlight function (markdown-it-py will call this for fenced code)
md.options["highlight"] = lambda code, lang, _: (
    f'<pre class="code"><code>{highlight_code(code, lang)}</code></pre>'
)

# Add useful plugins
md.use(tasklists_plugin)      # task lists: - [ ] / - [x]
md.use(anchors_plugin)        # heading anchors/permalinks
md.use(front_matter_plugin)   # front matter parsing (if you want it)
md.use(admon_plugin)          # admonitions: !!! note/warning etc.


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
                "app_name": APP_NAME,
                "request": request,
            },
        )
        logger.debug(f"Page rendered successfully: {title or 'Untitled'}")
        return response
    except Exception as e:
        logger.error(f"Error rendering page '{title or 'Untitled'}': {e}")
        raise

"""Markdown Renderer using markdown-it-py with useful plugins."""

# Markdown imports
from markdown_it import MarkdownIt
from mdit_py_plugins.tasklists import tasklists_plugin
from mdit_py_plugins.anchors import anchors_plugin
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.admon import admon_plugin
from bleach import clean

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
md.use(tasklists_plugin)  # task lists: - [ ] / - [x]
md.use(anchors_plugin)  # heading anchors/permalinks
md.use(front_matter_plugin)  # front matter parsing (if you want it)
md.use(admon_plugin)  # admonitions: !!! note/warning etc.


def enhance_admonitions(html: str) -> str:
    """Post-process HTML to enhance admonition structure with custom elements."""
    import re

    # Icon mapping for different admonition types
    icons = {
        "note": "edit_square",
        "info": "ℹnfo",
        "tip": "emoji_objects",
        "hint": "emoji_objects",
        "important": "exclamation",
        "attention": "exclamation",
        "warning": "warning",
        "caution": "warning",
        "danger": "error",
        "error": "error",
        "failure": "error",
        "success": "check_circle",
        "check": "check_circle",
        "question": "question_mark",
        "bug": "bug_report",
        "quote": "format_quote",
        "example": "note_alt",
        "abstract": "note_alt",
        "summary": "notes",
    }

    def replace_admonition(match):
        full_match = match.group(0)
        classes = match.group(1)
        title_content = match.group(2)
        body_content = match.group(3)

        # Extract admonition type from classes
        admon_type = "note"  # default
        for cls in classes.split():
            if cls != "admonition" and cls in icons:
                admon_type = cls
                break

        icon = icons.get(admon_type, "ℹ️")

        # Build enhanced structure
        # + Really stupid icon
        enhanced = f"""
<div class="admonition admonition-{admon_type}">
    <div class="admonition-indicator"></div>
    <div class="admonition-container">
        <div class="admonition-header">
            <div class="admonition-icon">
                <span class="icon">{icon}</span>
            </div>
            <div class="admonition-title">{title_content}</div>
        </div>
        <div class="admonition-content">{body_content}</div>
    </div>
</div>"""

        return enhanced

    # Pattern to match standard admonition HTML structure
    # Matches: <div class="admonition TYPE"><p class="admonition-title">TITLE</p>CONTENT</div>
    pattern = r'<div class="([^"]*admonition[^"]*)">\s*<p class="admonition-title">([^<]*)</p>\s*(.*?)\s*</div>'

    # Replace all admonitions with enhanced structure
    enhanced_html = re.sub(pattern, replace_admonition, html, flags=re.DOTALL)

    return enhanced_html


def clean_html(html: str) -> str:
    """Sanitize HTML to prevent XSS attacks."""
    allowed_tags = [
        "a",
        "abbr",
        "acronym",
        "b",
        "blockquote",
        "code",
        "em",
        "i",
        "li",
        "ol",
        "strong",
        "ul",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "p",
        "pre",
        "br",
        "hr",
        "img",
        "div",
        "span",
        "table",
        "thead",
        "tbody",
        "tr",
        "th",
        "td",
    ]
    allowed_attributes = {
        "*": ["class", "id"],
        "a": ["href", "title"],
        "img": ["src", "alt", "title"],
    }
    cleaned_html = clean(html, tags=allowed_tags, attributes=allowed_attributes)
    return cleaned_html


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
    html_jobs = [enhance_admonitions, clean_html]

    logger.debug(f"Rendering markdown content of length: {len(md_text)}")

    if not md_text.strip():
        logger.warning("Empty markdown content provided")
        return f"<p> This document has no content. </p>"

    try:
        html = md.render(md_text)

        # Apply HTML enhancement jobs
        for job in html_jobs:
            html = job(html)
        logger.debug("Markdown rendering and enhancement completed successfully")
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

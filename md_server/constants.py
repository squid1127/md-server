"""Constants for the Markdown Server."""

APP_NAME = "md-server"
APP_DESCRIPTION = "A tiny markdown preview server for your services."
APP_SOURCE = "https://github.com/squid1127/md-server"

API_KEY_HEADER = "X-API-KEY"

HOME_PAGE = f"""# {APP_NAME}

{APP_DESCRIPTION}

([Source]({APP_SOURCE}))

## Markdown Feature Support
{APP_NAME} uses markdown-it-py for rendering markdown (+plugins), which the following:

### Basic Markdown
**Bold** / *Italic* / ~~Strikethrough~~ / `Inline code`
#### Headers (H1, H2, H3, H4, H5, H6)

### Blockquotes
> This is a blockquote.

### Admonition
Note that admonitions use `!!!` rather than `> [type]` syntax. (Yes it's not GFM whatever)
!!! success This is a note admonition.
    This is the content of the admonition.
!!! warning This is a warning admonition.
    This is the content of the warning admonition.
"""

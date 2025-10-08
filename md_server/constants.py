"""Constant variables"""

APP_NAME = "md-server"
APP_DESCRIPTION = "A tiny markdown preview server for your services."
APP_SOURCE = "https://github.com/squid1127/md-server"

API_KEY_HEADER = "X-API-KEY"

HOME_PAGE = f"""# {APP_NAME}

{APP_DESCRIPTION}

([Source]({APP_SOURCE}))

## Markdown Support
{APP_NAME} uses markdown-it-py for rendering markdown (+plugins), in addition to github-flavored-markdown (GFM) for styling.

### Basic Markdown
**Bold** / *Italic* / ~~Strikethrough~~ / `Inline code`
#### Headers (H1, H2, H3, H4, H5, H6)

### Blockquotes
> This is a blockquote.

### Admonition
Note that admonitions use `!!!` rather than `> [type]` syntax. (Yes it's not GFM whatever)
!!! success Success Admonition
    This is the content of the admonition.
!!! warning Warning Admonition
    This is the content of the warning admonition.
    This is a [Link](https://github.com/squid1127/md-server)
    
### Lists
- Unordered list item 1
- Unordered list item 2
    - Nested unordered list item 1
    - Nested unordered list item 2

1. Ordered list item 1
2. Ordered list item 2
    1. Nested ordered list item 1
    2. Nested ordered list item 2

### [Several Links](https://github.com/squid1127/md-server)
[Google](https://www.google.com) | [GitHub](https://github.com) | [squid1127](https://github.com/squid1127) | [Arch](https://archlinux.org) | [Reddit](https://www.reddit.com)


### Tables
| Header 1 | Header 2 | Header 3 | a | [b](https://github.com/squid1127/md-server) |
|----------|----------|---------:|:-|-:|
| Row 1   | Data 1   | [Data 2](https://github.com/squid1127/md-server)   | [1](https://github.com/squid1127/md-server) | [4](https://github.com/squid1127/md-server) |
| Row 2   | Data 3   | Data 4   | 2 | 5 |
| Row 3   | Data 5   | Data 6   | 3 | 6 |
"""

"""Constants for the Markdown Server."""

APP_NAME = "md-server"
APP_DESCRIPTION = "A tiny markdown preview server for your services."
APP_SOURCE = "https://github.com/squid1127/md-server"

API_KEY_HEADER = "X-API-KEY"

HOME_PAGE = f"""# {APP_NAME}

{APP_DESCRIPTION}

([Source]({APP_SOURCE}))

## Markdown Format Test

# Heading 1
## Heading 2
### Heading 3
#### Heading 4
##### Heading 5

This is a paragraph with **bold text**, *italic text*, and ***bold italic text***.
"""

"""Template files for the markdown server."""

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="md_server/templates")
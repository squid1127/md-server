"""Static files for the markdown server."""

from fastapi.staticfiles import StaticFiles

static_files = StaticFiles(directory="md_server/static", html=True)
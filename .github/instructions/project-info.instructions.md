---
applyTo: "**"
---

# Project Information

# md-server

This project is a tiny markdown preview server for your services, built with FastAPI. It allows you to serve and preview markdown files with ease.

## Features

- Serve markdown files from a specified directory.
- Render markdown content to HTML using `markdown-it-py` with various plugins for enhanced functionality.
- Syntax highlighting for code blocks using Prism.js.
- Simple and clean user interface with GitHub-style markdown rendering.
- Refer to README.md for more details.

## Execution

Assuming the environment is set up correctly, you can run the server using the following command:

```bash
poetry run fastapi dev md_server
```

To initialize the dev environment (with Poetry installed), use:

```bash
poetry install
```

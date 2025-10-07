# md-server

A tiny markdown preview server for your services.

How much of this was AI generated? Too much.

## Features

- Serves markdown previews styled with GitHub's markdown CSS.
- Renders markdown to HTML using `markdown-it-py` with plugins for tables, task lists
- Uploads and manages files using a RESTful API, designed for integration with other services. (Authentication required)
- MongoDB backend for file storage, metadata, and api keys.
- Configuration via environment variables or `.env` file.
- CLI for api key management and server control.
- Comprehensive logging with configurable levels and file rotation.

### Notablably Missing Features

- [ ] DB support for SQL databases
- [ ] Complete markdown support (e.g., math, diagrams)
- [ ] Currently, the markdown styling is a bit messy

## Installation

For docker installation, refer to [docker instructions](docs/docker.md).

To install and run locally, ensure you have Python 3.13+ and Poetry installed. Then:

```bash
git clone https://github.com/squid1127/md-server.git # Clone the repository
cd md-server # Change to the project directory
poetry install # Install dependencies
poetry run md-server # Run the server
```

### Usage Example

```bash
# Set log level to DEBUG for development
export LOG_LEVEL=DEBUG
python cli.py run

# Or set in .env file
echo "LOG_LEVEL=DEBUG" >> .env
```

Refer to [environment variables](docs/env.md) for configuration options.

### API Usage

Refer to [API documentation](docs/api.md)

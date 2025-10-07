# md-server

A tiny markdown preview server for your services.

How much of this was AI generated? Too much.

## Features

- Serve markdown files to users.
- Upload and manage files using a RESTful API. (Authentication required)
- Render markdown files to HTML for easy viewing in browsers.
- Minimalistic frontend
- MongoDB backend for file storage, metadata, and api keys.
- Configuration via environment variables or `.env` file.
- CLI for api key management and server control.
- Comprehensive logging with configurable levels and file rotation.

### Usage Example

```bash
# Set log level to DEBUG for development
export LOG_LEVEL=DEBUG
python cli.py run

# Or set in .env file
echo "LOG_LEVEL=DEBUG" >> .env
```

Refer to [environment variables](docs/env.md)

#### API Usage

Refer to [API documentation](docs/api.md)

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

## Logging

The application includes comprehensive logging with the following features:

### Configuration

Logging can be configured through environment variables:

- `LOG_LEVEL`: Set the logging level (DEBUG, INFO, WARNING, ERROR). Default: INFO

### Log Files

Logs are written to the `logs/` directory:

- `logs/md_server.log`: General application logs with rotation (10MB max, 5 backups)
- `logs/errors.log`: Error-level logs only with rotation (10MB max, 5 backups)

### Console Output

All logs are also displayed in the console with appropriate formatting.

### Log Levels

- **DEBUG**: Detailed information for debugging
- **INFO**: General application flow and important events
- **WARNING**: Warnings about potential issues
- **ERROR**: Error conditions that need attention

### Usage Example

```bash
# Set log level to DEBUG for development
export LOG_LEVEL=DEBUG
python cli.py run

# Or set in .env file
echo "LOG_LEVEL=DEBUG" >> .env
```

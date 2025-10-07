# Environment Variables / Configuration

The application can be configured using environment variables or a `.env` file. Below are the available configuration options:

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

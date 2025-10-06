"""Entry point for the markdown server CLI."""

import sys
from md_server.cli.main import cli
from md_server.logging_config import setup_logging, get_logger

# Setup logging for CLI usage
setup_logging()
logger = get_logger(__name__)

if __name__ == "__main__":
    try:
        cli()
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)
"""Command-line interface for managing the markdown server."""

import os
import typer
from dotenv import load_dotenv
from ..logging_config import setup_logging, get_logger
from .auth import cli as auth_cli

# Load environment variables
load_dotenv()

# Setup logging before creating the CLI
setup_logging()
logger = get_logger(__name__)

cli = typer.Typer()
cli.add_typer(auth_cli, name="auth")

@cli.command()
def run(
    host: str = typer.Option(
        os.getenv("HOST", "127.0.0.1"), 
        help="Host to bind the server to"
    ),
    port: int = typer.Option(
        int(os.getenv("PORT", "8000")), 
        help="Port to bind the server to"
    ),
    reload: bool = typer.Option(
        os.getenv("RELOAD", "false").lower() == "true", 
        help="Enable auto-reload for development"
    ),
    log_level: str = typer.Option(
        os.getenv("LOG_LEVEL", "info").lower(), 
        help="Log level (debug, info, warning, error)"
    )
):
    """Start the markdown server."""
    logger.info(f"Starting markdown server on {host}:{port}")
    logger.info(f"Reload mode: {reload}")
    logger.info(f"Log level: {log_level}")
    
    try:
        import uvicorn
        uvicorn.run(
            "md_server.main:app", 
            host=host, 
            port=port, 
            reload=reload,
            log_level=log_level
        )
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        raise typer.Exit(code=1)
    
if __name__ == "__main__":
    cli()
"""CLI for managing API keys."""
import typer
import asyncio
from functools import wraps
from ..db import list_api_keys, init_db as db_init, create_markdown_document
from ..auth import new_api_key
from ..logging_config import get_logger

logger = get_logger(__name__)
cli = typer.Typer(help="Manage API keys for the markdown server. / Perform database operations.")

def async_command(func):
    """Decorator to handle async operations in CLI commands."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))
    return wrapper

async def init_db():
    """Initialize the database connection."""
    try:
        await db_init()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

@cli.command()
@async_command
async def new(description: str = typer.Argument(..., help="Description for the new API key")):
    """Create a new API key."""
    await init_db()
    
    try:
        key = await new_api_key(description)
        typer.echo(f"New API key created: {key}")
        typer.echo("Please store this key securely; it will not be shown again.")
    except Exception as e:
        logger.error(f"Error creating new API key: {e}")
        typer.echo("Failed to create new API key", err=True)
        raise typer.Exit(code=1)
        
@cli.command()
@async_command
async def list():
    """List all API keys."""    
    await init_db()
    
    try:
        keys = await list_api_keys()
        if not keys:
            typer.echo("No API keys found.")
            return
        for key in keys:
            typer.echo(f"Key (SHA256): {key.hash} | Description: {key.description or 'No description'} | Created At: {key.created_at}")
    except Exception as e:
        logger.error(f"Error listing API keys: {e}")
        typer.echo("Failed to list API keys", err=True)
        raise typer.Exit(code=1)
    
@cli.command()
@async_command
async def new_doc(
    title: str = typer.Argument(..., help="Title of the new document"),
    fp: str = typer.Argument(..., help="File containing the markdown content"),
):
    """[Experimental] Create a new markdown document to insert into the database."""
    await init_db()
    
    try:
        with open(fp, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        logger.error(f"Error reading file '{fp}': {e}")
        typer.echo(f"Failed to read file: {fp}", err=True)
        raise typer.Exit(code=1)

    try:
        doc = await create_markdown_document(title, content)
        typer.echo(f"New document created with ID: {doc.doc_id}")
    except Exception as e:
        logger.error(f"Error creating new document: {e}")
        typer.echo("Failed to create new document", err=True)
        raise typer.Exit(code=1)
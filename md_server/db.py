"""Database module for the markdown server."""

import os
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from .models import MarkdownDocument, APIKey, APIUsageLog, User
from .logging_config import get_logger

logger = get_logger(__name__)

def get_connection_string() -> str:
    """Get the MongoDB connection string from environment or use default."""
    connection_string = os.getenv("MONGO_URL", None)
    if not connection_string:
        connection_string = "mongodb://localhost:27017"
        logger.warning("MONGO_URL not set, defaulting to mongodb://localhost:27017")
    return connection_string


async def init_db():
    """Initialize the database connection and Beanie ODM."""
    connection_str = get_connection_string()
    logger.info(f"Connecting to MongoDB at: {connection_str}")
    
    try:
        client = AsyncIOMotorClient(connection_str)
        
        # Test the connection
        await client.admin.command('ping')
        logger.info("MongoDB connection successful")
        
        database = client.get_default_database()
        logger.info(f"Using database: {database.name}")
        
        await init_beanie(
            database=database, document_models=[MarkdownDocument, APIKey, APIUsageLog, User]
        )
        logger.info("Beanie initialization completed successfully")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise
    
async def get_db():
    """Get the database connection."""
    connection_str = get_connection_string()
    client = AsyncIOMotorClient(connection_str)
    return client.get_default_database()

#* Document Operations
async def get_markdown_document(md_id: str) -> MarkdownDocument | None:
    """Retrieve a markdown document by its ID."""
    logger.info(f"Fetching markdown document with ID: {md_id}")
    document = await MarkdownDocument.find_one(MarkdownDocument.doc_id == md_id)
    if document:
        logger.info(f"Document found: {document.title}")
    else:
        logger.warning(f"No document found with ID: {md_id}")
    return document

async def create_markdown_document(title: str, content: str) -> MarkdownDocument:
    """Create a new markdown document."""
    logger.info(f"Creating new markdown document: {title}")
    document = MarkdownDocument(title=title, content=content)
    await document.save()
    logger.info(f"Document created with ID: {document.doc_id}")
    return document

async def delete_markdown_document(md_id: str) -> bool:
    """Delete a markdown document by its ID."""
    logger.info(f"Deleting markdown document with ID: {md_id}")
    document = await get_markdown_document(md_id)
    if document:
        await document.delete()
        logger.info(f"Document with ID: {md_id} deleted successfully")
        return True
    else:
        logger.warning(f"Cannot delete, no document found with ID: {md_id}")
        return False
    
    
#* API Key Operations
async def create_api_key(hash: str, description: str = None) -> APIKey:
    """Create a new API key."""
    logger.info(f"Creating new API key: {description or 'No description'}")
    api_key = APIKey(hash=hash, description=description)
    await api_key.save()
    logger.info(f"API key created with ID: {api_key.id}")
    return api_key
async def get_api_key(hash: str) -> APIKey | None:
    """Retrieve an API key by its hash."""
    logger.info(f"Fetching API key with hash: {hash}")
    api_key = await APIKey.find_one(APIKey.hash == hash)
    if api_key:
        logger.info(f"API key found: {api_key.description or 'No description'}")
    else:
        logger.warning(f"No API key found with hash: {hash}")
    return api_key
async def list_api_keys() -> list[APIKey]:
    """List all API keys."""
    logger.info("Listing all API keys")
    api_keys = await APIKey.find_all().to_list()
    logger.info(f"Total API keys found: {len(api_keys)}")
    return api_keys

async def log_api_usage(api_key: str, endpoint: str, client_ip: str = None):
    """Log an API usage event."""
    logger.info(f"Logging API usage for key: {api_key} at endpoint: {endpoint}")
    usage_log = APIUsageLog(api_key=api_key, endpoint=endpoint, client_ip=client_ip)
    await usage_log.save()
    logger.info("API usage logged successfully")
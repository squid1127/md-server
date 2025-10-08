"""Database models for the markdown server."""

from beanie import Document
from pydantic import Field
from typing import Optional
import datetime
from .logging_config import get_logger
from uuid import uuid4

logger = get_logger(__name__)

class LoggedDocument(Document):
    async def save(self, *args, **kwargs):
        """Override save to add logging."""
        doc_name = getattr(self, 'title', getattr(self, 'description', str(self.__class__.__name__)))
        logger.info(f"Saving document: {doc_name}")
        result = await super().save(*args, **kwargs)
        logger.info(f"Document saved successfully with ID: {self.id}")
        return result
    
    async def delete(self, *args, **kwargs):
        """Override delete to add logging."""
        doc_name = getattr(self, 'title', getattr(self, 'description', str(self.__class__.__name__)))
        logger.info(f"Deleting document: {doc_name} (ID: {self.id})")
        result = await super().delete(*args, **kwargs)
        logger.info(f"Document deleted successfully")
        return result

class MarkdownDocument(LoggedDocument):
    doc_id: str = Field(index=True, unique=True, default_factory=lambda: str(uuid4()))
    title: str
    content: str
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))

    class Settings:
        name = "md_server.documents"
    
class APIKey(LoggedDocument):
    hash: str = Field(index=True, unique=True)
    description: Optional[str] = None
    created_at: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))

    class Settings:
        name = "md_server.api_keys"
        
class APIUsageLog(LoggedDocument):
    api_key: str
    endpoint: str
    timestamp: datetime.datetime = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))
    client_ip: Optional[str] = None

    class Settings:
        name = "md_server.api_usage_logs"
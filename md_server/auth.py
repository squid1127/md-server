"""API Key Management and Authentication."""

import os
from fastapi import Security, HTTPException, Depends
from fastapi.security import APIKeyHeader
from datetime import datetime
import hashlib

from .db import create_api_key, get_api_key, log_api_usage, APIKey
from .constants import API_KEY_HEADER
from .logging_config import get_logger

logger = get_logger(__name__)

api_key_header = APIKeyHeader(name=API_KEY_HEADER, auto_error=False)

def hash_api_key(key: str) -> str:
    """Hash the API key using SHA-256."""
    return hashlib.sha256(key.encode()).hexdigest()

async def verify_api_key(api_key: str = Security(api_key_header), request_ip: str = None):
    """Verify the provided API key."""
    if not api_key:
        logger.warning("No API key provided")
        raise HTTPException(status_code=403, detail="API key required")
    
    hashed_key = hash_api_key(api_key)
    api_key_record: APIKey | None = await get_api_key(hashed_key)
    
    if not api_key_record:
        logger.warning(f"Invalid API key attempt from IP: {request_ip}")
        raise HTTPException(status_code=403, detail="Invalid API key")
    
    # Log the API usage
    await log_api_usage(api_key=hashed_key, endpoint=request_ip or "unknown", client_ip=request_ip)
    
    logger.info(f"API key verified for IP: {request_ip}")
    return api_key_record

async def new_api_key(description: str = None) -> str:
    """Generate a new API key and store its hash in the database."""
    raw_key = os.urandom(24).hex()
    hashed_key = hash_api_key(raw_key)
    
    await create_api_key(hash=hashed_key, description=description)
    logger.info(f"New API key created: {description or 'No description'}")
    return raw_key  # Return the raw key to the user only once
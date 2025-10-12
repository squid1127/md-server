"""API Key Management and Authentication."""

import os
from fastapi import Header, Security, HTTPException, Depends
from fastapi.security import APIKeyHeader
from datetime import datetime
import hashlib

from .db import create_api_key, get_api_key, log_api_usage, APIKey
from .models import User
from .constants import API_KEY_HEADER, AUTHENTIK_ID_HEADER, AUTHENTIK_NAME_HEADER
from .logging_config import get_logger

logger = get_logger(__name__)

#* API Keys
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

#* Authentik Authentication
user_id_header = APIKeyHeader(name=AUTHENTIK_ID_HEADER, auto_error=False)
user_name_header = APIKeyHeader(name=AUTHENTIK_NAME_HEADER, auto_error=True)

async def verify_user_auto(user_id: str = Security(user_id_header), user_name: str = Security(user_name_header)) -> User:
    """Verify the user from Authentik headers."""
    if os.getenv("AUTH_CREATE_USERS", "true").lower() == "true":
        create = True
    else:
        create = False
    return await _verify_user(user_id, user_name, create=create)

async def verify_user(user_id: str = Security(user_id_header)) -> User:
    """Verify the user from Authentik headers without creating new users."""
    return await _verify_user(user_id, create=False)

async def _verify_user(user_id: str, user_name: str = None, create: bool = False) -> User:
    """Verify the user from Authentik headers."""
    if os.getenv("AUTH_DISABLE", "false").lower() == "true":
        logger.warning("Authentication is disabled via environment variable")
        raise HTTPException(status_code=403, detail="Authenticated endpoints are disabled")
    
    if not user_id:
        logger.warning("No Authentik user ID provided")
        raise HTTPException(status_code=403, detail="User authentication required")
    
    id_sha = hash_api_key(user_id)# Hash the user ID for privacy
    user: User | None = await User.find_one(User.uid_sha256 == id_sha)
    
    if not user and create:
        # Create a new user record if not found and creation is allowed
        user = User(uid_sha256=id_sha, name=user_name)
        await user.save()
        logger.info(f"New user created with ID hash: {id_sha}")
    elif not user:
        logger.warning(f"User with ID hash {id_sha} not found and creation not allowed")
        raise HTTPException(status_code=403, detail="User not recognized")

    logger.info(f"User authenticated: {user_id}")
    return user
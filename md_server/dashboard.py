"""
Dashboard routes for authenticated users.
"""

from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from starlette.status import HTTP_401_UNAUTHORIZED

from .constants import APP_NAME
from .md import render_md_page
from .logging_config import get_logger
from .auth import verify_user, verify_user_auto
from .models import User
from .templates import templates

logger = get_logger(__name__)
router = APIRouter()


@router.get(
    "/", tags=["UI", "Dashboard"], name="Dashboard", response_class=HTMLResponse
)
async def read_home(request: Request, user: User = Depends(verify_user_auto)):
    """[Debug] Read out request headers and client info."""
    logger.info(f"Home page requested from {request.client.host}")
    try:
        for header, value in request.headers.items():
            logger.info(f"Header: {header} = {value}")
        return templates.TemplateResponse(
            "dashboard.html",
            {
                "request": request,
                "page_title": "Dashboard",
                "app_name": APP_NAME,
                "user": user,
            },
        )
    except Exception as e:
        logger.error(f"Error rendering home page: {e}")
        raise
    
@router.get(
    "/status",
    tags=["Dashboard"],
    name="Authentication Status (Check if Authenticated)",
    response_class=JSONResponse,
)
async def auth_status(user: User = Depends(verify_user)):
    """Check if the user is authenticated or raises 401."""
    if not user:
        logger.warning("Unauthenticated access attempt to /status")
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    
    logger.info(f"Authenticated user {user.id} accessed /status")
    return {
        "authenticated": True,
        "user_id": str(user.id),
        "username": user.name,
    }


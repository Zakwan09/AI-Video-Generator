"""
Health check endpoint.
"""

from fastapi import APIRouter, status

from app.config import settings

router = APIRouter(tags=["health"])


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check() -> dict[str, str]:
    """Simple liveness check used by the frontend and deployment tooling."""
    return {"status": "ok", "service": settings.APP_NAME}

"""
Reusable FastAPI dependency providers.
"""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.services.video_generation_service import VideoGenerationService
from app.services.video_service import VideoService

DbSession = Annotated[AsyncSession, Depends(get_db)]


def get_video_service(db: DbSession) -> VideoService:
    """Provide a VideoService bound to the current request's DB session."""
    return VideoService(db)


def get_video_generation_service() -> VideoGenerationService:
    """Provide the AI video generation orchestrator."""
    return VideoGenerationService()


VideoServiceDep = Annotated[VideoService, Depends(get_video_service)]
VideoGenServiceDep = Annotated[VideoGenerationService, Depends(get_video_generation_service)]

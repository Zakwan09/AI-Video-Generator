"""
Data-access layer for the `videos` table.

Encapsulates all SQLAlchemy queries so routers stay thin and the
"keep only the last N records" rule lives in exactly one place.
"""

import uuid

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.video import Video, VideoStatus
from app.utils.exceptions import VideoNotFoundError


class VideoService:
    """CRUD operations for Video records."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_video(self, prompt: str) -> Video:
        """Insert a new pending Video record."""
        video = Video(prompt=prompt, status=VideoStatus.PENDING, video_url=None)
        self.db.add(video)
        await self.db.commit()
        await self.db.refresh(video)
        return video

    async def mark_completed(self, video: Video, video_url: str) -> Video:
        video.status = VideoStatus.COMPLETED
        video.video_url = video_url
        await self.db.commit()
        await self.db.refresh(video)
        return video

    async def mark_failed(self, video: Video) -> Video:
        video.status = VideoStatus.FAILED
        await self.db.commit()
        await self.db.refresh(video)
        return video

    async def get_history(self) -> list[Video]:
        """Return the most recent records, newest first (capped at MAX_HISTORY_RECORDS)."""
        result = await self.db.execute(
            select(Video)
            .order_by(Video.created_at.desc())
            .limit(settings.MAX_HISTORY_RECORDS)
        )
        return list(result.scalars().all())

    async def delete_video(self, video_id: uuid.UUID) -> None:
        video = await self.db.get(Video, video_id)
        if video is None:
            raise VideoNotFoundError(str(video_id))
        await self.db.delete(video)
        await self.db.commit()

    async def enforce_history_limit(self) -> None:
        """
        Delete the oldest record(s) whenever there are more than
        MAX_HISTORY_RECORDS rows in the table.
        """
        result = await self.db.execute(select(Video.id).order_by(Video.created_at.desc()))
        all_ids = [row[0] for row in result.all()]

        if len(all_ids) <= settings.MAX_HISTORY_RECORDS:
            return

        stale_ids = all_ids[settings.MAX_HISTORY_RECORDS :]
        await self.db.execute(delete(Video).where(Video.id.in_(stale_ids)))
        await self.db.commit()

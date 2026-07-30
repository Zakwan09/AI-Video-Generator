"""
Pydantic schemas used for request validation and response serialization.
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.video import VideoStatus


class VideoGenerateRequest(BaseModel):
    """Payload for POST /generate."""

    prompt: str = Field(..., description="Text prompt describing the desired video")

    @field_validator("prompt")
    @classmethod
    def prompt_must_not_be_blank(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("Prompt must not be empty.")
        if len(value.strip()) < 5:
            raise ValueError("Prompt is too short to generate a meaningful video.")
        return value.strip()


class VideoResponse(BaseModel):
    """Serialized representation of a Video record returned to the client."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    prompt: str
    video_url: str | None
    status: VideoStatus
    created_at: datetime


class ErrorResponse(BaseModel):
    """Standard error envelope returned on failure."""

    detail: str
    error_code: str

"""
API endpoints for video generation and history management.
"""

import logging
import uuid

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.schemas.video import VideoGenerateRequest, VideoResponse
from app.utils.dependencies import VideoGenServiceDep, VideoServiceDep
from app.utils.exceptions import (
    ProviderAPIKeyMissingError,
    ProviderRequestError,
    ProviderTimeoutError,
    VideoNotFoundError,
)

logger = logging.getLogger(__name__)
router = APIRouter(tags=["videos"])


@router.post("/generate", response_model=VideoResponse, status_code=status.HTTP_201_CREATED)
async def generate_video(
    payload: VideoGenerateRequest,
    video_service: VideoServiceDep,
    generation_service: VideoGenServiceDep,
) -> VideoResponse:
    """
    Generate an AI video from a text prompt.

    Creates a pending record, calls the configured free-tier provider,
    then updates the record with the result (or marks it failed).
    Validation of an empty prompt is handled by VideoGenerateRequest.
    """
    video = await video_service.create_video(payload.prompt)

    try:
        video_url = await generation_service.generate(payload.prompt)
    except ProviderTimeoutError as exc:
        await video_service.mark_failed(video)
        return JSONResponse(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            content={"detail": exc.message, "error_code": exc.error_code},
        )
    except ProviderAPIKeyMissingError as exc:
        await video_service.mark_failed(video)
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": exc.message, "error_code": exc.error_code},
        )
    except ProviderRequestError as exc:
        await video_service.mark_failed(video)
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content={"detail": exc.message, "error_code": exc.error_code},
        )
    except Exception:  # noqa: BLE001 - guarantee a clean JSON error for any unexpected failure
        logger.exception("Unexpected error during video generation")
        await video_service.mark_failed(video)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "An unexpected error occurred while generating the video.",
                "error_code": "UNEXPECTED_ERROR",
            },
        )

    video = await video_service.mark_completed(video, video_url)
    await video_service.enforce_history_limit()
    return video


@router.get("/history", response_model=list[VideoResponse])
async def get_history(video_service: VideoServiceDep) -> list[VideoResponse]:
    """Return the last five generated videos, most recent first."""
    return await video_service.get_history()


@router.delete("/history/{video_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_history_item(video_id: uuid.UUID, video_service: VideoServiceDep) -> None:
    """Delete a single video record from history."""
    try:
        await video_service.delete_video(video_id)
    except VideoNotFoundError as exc:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": exc.message, "error_code": exc.error_code},
        )

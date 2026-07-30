"""
Orchestrates AI video generation using the Replicate Provider.
"""

import logging

from app.services.providers.base import BaseVideoProvider
from app.services.providers.replicate_provider import ReplicateProvider
from app.utils.exceptions import (
    ProviderAPIKeyMissingError,
    ProviderRequestError,
    ProviderTimeoutError,
    VideoGenerationError,
)

logger = logging.getLogger(__name__)


class VideoGenerationService:
    """Selects and invokes the Replicate Provider."""

    def __init__(self) -> None:
        self._providers: list[BaseVideoProvider] = [
            ReplicateProvider(),
        ]

    async def generate(self, prompt: str) -> str:
        """
        Generate a video using the configured Replicate provider.

        Returns:
            str: URL of the generated video.
        """

        configured_providers = [
            provider for provider in self._providers if provider.is_configured()
        ]

        if not configured_providers:
            raise ProviderAPIKeyMissingError()

        last_error: VideoGenerationError | None = None

        for provider in configured_providers:
            try:
                logger.info(
                    "Generating video using provider: %s",
                    provider.name,
                )

                return await provider.generate_video(
                    prompt,
                    timeout_seconds=300,
                )

            except (ProviderTimeoutError, ProviderRequestError) as exc:
                logger.warning(
                    "Provider %s failed: %s",
                    provider.name,
                    exc.message,
                )
                last_error = exc

        raise last_error or ProviderRequestError(
            "Video generation failed."
        )
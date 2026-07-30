"""
Abstract interface that every video generation provider must implement.

Keeping providers behind a common interface lets the orchestrating service
(VideoGenerationService) invoke them without knowing any provider-specific
implementation details.
"""

from abc import ABC, abstractmethod


class BaseVideoProvider(ABC):
    """Common contract for all video generation providers."""

    name: str = "base"

    @abstractmethod
    def is_configured(self) -> bool:
        """
        Return True if this provider is ready to generate videos.
        """
        raise NotImplementedError

    @abstractmethod
    async def generate_video(
        self,
        prompt: str,
        timeout_seconds: int | None = None,
    ) -> str:
        """
        Generate a video for the given prompt.

        Args:
            prompt: User's text prompt.
            timeout_seconds: Optional timeout for providers that require it.

        Returns:
            str: URL or relative path of the generated video.

        Raises:
            Exception: Provider-specific generation error.
        """
        raise NotImplementedError
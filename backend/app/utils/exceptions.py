"""
Custom application exceptions.

Each maps to a specific HTTP status code in the router layer, giving the
frontend consistent, predictable error responses.
"""


class VideoGenerationError(Exception):
    """Base exception for all video-generation related failures."""

    def __init__(self, message: str, error_code: str = "GENERATION_ERROR") -> None:
        self.message = message
        self.error_code = error_code
        super().__init__(message)


class EmptyPromptError(VideoGenerationError):
    """Raised when the submitted prompt is empty or whitespace only."""

    def __init__(self) -> None:
        super().__init__("Prompt must not be empty.", "EMPTY_PROMPT")


class ProviderAPIKeyMissingError(VideoGenerationError):
    """Raised when no valid API key is configured for any provider."""

    def __init__(self) -> None:
        super().__init__(
            "No valid API key configured for any video generation provider.",
            "MISSING_API_KEY",
        )


class ProviderTimeoutError(VideoGenerationError):
    """Raised when the generation provider takes too long to respond."""

    def __init__(self) -> None:
        super().__init__(
            "Video generation timed out. Please try again.",
            "GENERATION_TIMEOUT",
        )


class ProviderRequestError(VideoGenerationError):
    """Raised when the provider API call fails (network error, bad response, etc.)."""

    def __init__(self, message: str) -> None:
        super().__init__(message, "PROVIDER_ERROR")


class VideoNotFoundError(VideoGenerationError):
    """Raised when a requested video record does not exist."""

    def __init__(self, video_id: str) -> None:
        super().__init__(f"Video with id '{video_id}' was not found.", "NOT_FOUND")

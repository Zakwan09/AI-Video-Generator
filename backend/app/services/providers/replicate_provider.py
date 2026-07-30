"""
Replicate text-to-video provider using the official Replicate SDK.
"""

import asyncio
import replicate

from app.config import settings
from app.services.providers.base import BaseVideoProvider
from app.utils.exceptions import (
    ProviderRequestError,
    ProviderTimeoutError,
)

# Current Replicate model
MODEL_NAME = "wan-video/wan-2.2-t2v-fast"


class ReplicateProvider(BaseVideoProvider):
    name = "replicate"

    def __init__(self):
        self.client = replicate.Client(
            api_token=settings.REPLICATE_API_TOKEN
        )

    def is_configured(self) -> bool:
        return bool(settings.REPLICATE_API_TOKEN)

    async def generate_video(
        self,
        prompt: str,
        timeout_seconds: int,
    ) -> str:

        try:
            output = await asyncio.wait_for(
                asyncio.to_thread(
                    self.client.run,
                    MODEL_NAME,
                    input={
                        "prompt": prompt,
                        "go_fast": True,
                        "num_frames": 81,
                        "resolution": "480p",
                        "aspect_ratio": "16:9",
                    },
                ),
                timeout=timeout_seconds,
            )

        except asyncio.TimeoutError:
            raise ProviderTimeoutError()

        except Exception as e:
            raise ProviderRequestError(
                f"Replicate error: {e}"
            ) from e

        if output is None:
            raise ProviderRequestError(
                "Replicate returned no output."
            )

        if isinstance(output, list):
            output = output[0]

        # Replicate File object
        if hasattr(output, "url"):
            return output.url()

        # String URL
        if isinstance(output, str):
            return output

        raise ProviderRequestError(
            f"Unexpected output type: {type(output)}"
        )
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database.session import init_db
from app.routers import health_router, video_router
from app.utils.exceptions import VideoGenerationError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

STATIC_VIDEOS_DIR = Path(__file__).resolve().parent / "static" / "videos"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Run startup/shutdown tasks: create DB tables, ensure static dir exists."""
    STATIC_VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
    await init_db()
    logger.info("Database initialized and application ready.")
    yield


app = FastAPI(
    title=settings.APP_NAME,
    description="Generate AI videos from text prompts using free-tier providers.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serves any videos produced by the HuggingFace fallback provider, which
# returns raw bytes rather than a hosted URL.
app.mount("/static", StaticFiles(directory=str(Path(__file__).resolve().parent / "static")), name="static")


@app.exception_handler(VideoGenerationError)
async def video_generation_error_handler(request: Request, exc: VideoGenerationError) -> JSONResponse:
    """Catch-all handler for any VideoGenerationError subclass that escapes a router."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": exc.message, "error_code": exc.error_code},
    )


app.include_router(health_router.router)
app.include_router(video_router.router)

from fastapi import FastAPI

from app.api.health import router as health_router
from app.core.config import settings

app = FastAPI(
    version=settings.app_version,
    title=settings.app_name,
    description=settings.app_description,
    debug=settings.debug,
)

app.include_router(health_router)

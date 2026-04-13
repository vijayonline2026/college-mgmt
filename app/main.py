import time
from sqlalchemy import text
from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

import redis.asyncio as redis

from app.db.deps import get_db
from app.core.config import get_settings
from app.infra.celery.worker import celery_app

settings = get_settings()
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    decode_responses=True
)

app = FastAPI(
    title="College Management API",
    description="My FastAPI App",
    docs_url="/docs",
)

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "API is working 🚀"}

@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check(db: AsyncSession = Depends(get_db)):
    health_status = {
        "status": "healthy",
        "timestamp": time.time(),
        "services": {}
    }
    errors = []

    #1. Check DB
    try:
        await db.execute(text("SELECT 1"))
        health_status["services"]["mysql"] = "up"
    except Exception as e:
        health_status["services"]["mysql"] = "down"
        errors.append(f"mysql: {str(e)}")

    # 2. Check Redis
    try:
        await redis_client.ping()
        health_status["services"]["redis"] = "up"
    except Exception as e:
        health_status["services"]["redis"] = "down"
        errors.append(f"Redis: {str(e)}")

    # 3. Celery
    try:
        inspector = celery_app.control.inspect()
        active_workers = inspector.ping()
        if not active_workers:
            raise Exception("No active Celery workers")

        health_status["services"]["celery"] = "up"

    except Exception as e:
        health_status["services"]["celery"] = "down"
        errors.append(f"Celery: {str(e)}")

    if errors:
        health_status["status"] = "unhealthy"
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=health_status
        )

    return health_status

@router.get("/health/live")
async def liveness_check():
    return {"status": "alive"}

app.include_router(router, prefix="/api")

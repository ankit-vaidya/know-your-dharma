from fastapi import FastAPI

from backend.app.api.v1.health import router as health_router

app = FastAPI(
    title="Know Your Dharma API",
    description="Backend API for the Know Your Dharma Scripture Intelligence Platform",
    version="0.1.0",
)

app.include_router(
    health_router,
    prefix="/api/v1/health",
)


@app.get("/api/v1/health")
async def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
        "service": "know-your-dharma-api",
    }
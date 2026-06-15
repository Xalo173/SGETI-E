from fastapi import APIRouter

from app.api.v1.routes import audits, health

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health.router, tags=["health"])
api_router.include_router(audits.router, tags=["audits"])

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.core.database import init_db


def create_app() -> FastAPI:
    app = FastAPI(
        title="AuditAI API",
        version="1.0.0",
        description="API REST para planificación y ejecución de auditorías de software con IA.",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router)

    @app.on_event("startup")
    async def on_startup() -> None:
        init_db()

    return app


app = create_app()

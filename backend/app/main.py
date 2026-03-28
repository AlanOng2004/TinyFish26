from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.health import router as health_router
from app.api.routes.runs import router as runs_router
from app.core.config import get_settings
from app.core.scheduler import start_scheduler, stop_scheduler
from app.db.session import Base, check_database_connection, engine


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="Autonomous Equity Analyst API", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_origins=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router)
    app.include_router(runs_router, prefix="/runs", tags=["runs"])

    @app.on_event("startup")
    async def on_startup() -> None:
        db_ok, db_message = check_database_connection()
        if not db_ok:
            raise RuntimeError(
                "Database connection failed during startup. "
                f"Current DATABASE_URL could not be reached: {db_message}"
            )
        Base.metadata.create_all(bind=engine)
        start_scheduler()

    @app.on_event("shutdown")
    async def on_shutdown() -> None:
        stop_scheduler()

    return app


app = create_app()

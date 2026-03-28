from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.runs import router as runs_router
from app.core.scheduler import start_scheduler, stop_scheduler


def create_app() -> FastAPI:
    app = FastAPI(title="Autonomous Equity Analyst API", version="0.1.0")

    app.include_router(health_router)
    app.include_router(runs_router, prefix="/runs", tags=["runs"])

    @app.on_event("startup")
    async def on_startup() -> None:
        start_scheduler()

    @app.on_event("shutdown")
    async def on_shutdown() -> None:
        stop_scheduler()

    return app


app = create_app()

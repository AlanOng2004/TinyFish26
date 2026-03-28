from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.core.config import get_settings
from app.db.session import SessionLocal
from app.services.batch_runner import run_batch_analysis

_scheduler: BackgroundScheduler | None = None


def start_scheduler() -> None:
    global _scheduler

    if _scheduler is not None:
        return

    settings = get_settings()
    _scheduler = BackgroundScheduler(timezone="UTC")
    _scheduler.add_job(
        scheduled_batch_job,
        trigger=IntervalTrigger(minutes=settings.scheduler_minutes),
        id="scheduled-nvda-batch",
        replace_existing=True,
    )
    _scheduler.start()


def stop_scheduler() -> None:
    global _scheduler

    if _scheduler is None:
        return

    _scheduler.shutdown(wait=False)
    _scheduler = None


def scheduled_batch_job() -> None:
    db = SessionLocal()
    try:
        run_batch_analysis(db=db, ticker="NVDA")
    finally:
        db.close()

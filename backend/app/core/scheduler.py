from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.api.routes.runs import seed_placeholder_history
from app.core.config import get_settings

_scheduler: BackgroundScheduler | None = None


def start_scheduler() -> None:
    global _scheduler

    if _scheduler is not None:
        return

    settings = get_settings()
    _scheduler = BackgroundScheduler(timezone="UTC")
    _scheduler.add_job(
        seed_placeholder_history,
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

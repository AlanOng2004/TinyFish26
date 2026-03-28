from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Query

from app.schemas.run import RunDetailResponse, RunHistoryItem, TriggerRunRequest
from app.services.batch_runner import run_batch_analysis

router = APIRouter()

_latest_run: RunDetailResponse | None = None
_run_history: list[RunHistoryItem] = []


@router.post("/trigger", response_model=RunDetailResponse)
def trigger_run(payload: TriggerRunRequest) -> RunDetailResponse:
    global _latest_run

    result = run_batch_analysis(ticker=payload.ticker)
    _latest_run = result
    _run_history.append(
        RunHistoryItem(
            run_id=result.id,
            ticker=result.ticker,
            run_timestamp=result.run_timestamp,
            discrepancy_score=result.final_assessment.discrepancy_score,
            stance=result.final_assessment.stance,
        )
    )
    return result


@router.get("/latest", response_model=RunDetailResponse)
def get_latest_run(
    ticker: str = Query(default="NVDA", description="Ticker symbol")
) -> RunDetailResponse:
    if _latest_run is None or _latest_run.ticker != ticker:
        raise HTTPException(status_code=404, detail="No run found for ticker")
    return _latest_run


@router.get("/history", response_model=list[RunHistoryItem])
def get_run_history(
    ticker: str = Query(default="NVDA", description="Ticker symbol")
) -> list[RunHistoryItem]:
    return [item for item in _run_history if item.ticker == ticker]


@router.get("/{run_id}", response_model=RunDetailResponse)
def get_run_by_id(run_id: int) -> RunDetailResponse:
    if _latest_run is None or _latest_run.id != run_id:
        raise HTTPException(status_code=404, detail="Run not found")
    return _latest_run


def seed_placeholder_history() -> None:
    global _latest_run

    seeded = run_batch_analysis("NVDA")
    seeded.run_timestamp = datetime.now(timezone.utc)
    _latest_run = seeded
    _run_history.clear()
    _run_history.append(
        RunHistoryItem(
            run_id=seeded.id,
            ticker=seeded.ticker,
            run_timestamp=seeded.run_timestamp,
            discrepancy_score=seeded.final_assessment.discrepancy_score,
            stance=seeded.final_assessment.stance,
        )
    )

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db.session import get_db
from app.models.run import Run
from app.schemas.run import RunDetailResponse, RunHistoryItem, TriggerRunRequest
from app.services.batch_runner import build_run_response, run_batch_analysis

router = APIRouter()


@router.post("/trigger", response_model=RunDetailResponse)
def trigger_run(
    payload: TriggerRunRequest,
    db: Session = Depends(get_db),
) -> RunDetailResponse:
    return run_batch_analysis(db=db, ticker=payload.ticker)


@router.get("/latest", response_model=RunDetailResponse)
def get_latest_run(
    ticker: str = Query(default="NVDA", description="Ticker symbol"),
    db: Session = Depends(get_db),
) -> RunDetailResponse:
    run = db.scalar(
        select(Run)
        .options(
            selectinload(Run.articles),
            selectinload(Run.technical_snapshot),
            selectinload(Run.historical_assessment),
        )
        .where(Run.ticker == ticker)
        .order_by(Run.run_timestamp.desc())
    )
    if run is None:
        raise HTTPException(status_code=404, detail="No run found for ticker")
    return build_run_response(run)


@router.get("/history", response_model=list[RunHistoryItem])
def get_run_history(
    ticker: str = Query(default="NVDA", description="Ticker symbol"),
    db: Session = Depends(get_db),
) -> list[RunHistoryItem]:
    runs = db.scalars(
        select(Run).where(Run.ticker == ticker).order_by(Run.run_timestamp.asc())
    ).all()
    return [
        RunHistoryItem(
            run_id=run.id,
            ticker=run.ticker,
            run_timestamp=run.run_timestamp,
            discrepancy_score=run.discrepancy_score,
            stance=run.stance,
        )
        for run in runs
    ]


@router.get("/{run_id}", response_model=RunDetailResponse)
def get_run_by_id(run_id: int, db: Session = Depends(get_db)) -> RunDetailResponse:
    run = db.scalar(
        select(Run)
        .options(
            selectinload(Run.articles),
            selectinload(Run.technical_snapshot),
            selectinload(Run.historical_assessment),
        )
        .where(Run.id == run_id)
    )
    if run is None:
        raise HTTPException(status_code=404, detail="Run not found")
    return build_run_response(run)

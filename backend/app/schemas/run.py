from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class TriggerRunRequest(BaseModel):
    ticker: str = Field(default="NVDA")


class ArticleItem(BaseModel):
    title: str
    source: str
    published_at: datetime
    summary: str
    sentiment: Literal["bullish", "bearish", "neutral"]
    relevance_score: float
    catalyst_type: str


class TechnicalAssessment(BaseModel):
    short_ma: float
    long_ma: float
    rsi: float
    score: float
    label: Literal["bullish", "bearish", "neutral"]
    price_points: int
    data_quality: Literal["strong", "usable", "limited", "insufficient"]


class SentimentAssessment(BaseModel):
    score: float
    label: Literal["bullish", "bearish", "neutral"]
    top_catalysts: list[str]


class HistoricalAssessmentView(BaseModel):
    matched_pattern: str
    score: float
    label: Literal["bullish", "bearish", "neutral"]
    rationale: str


class FinalAssessment(BaseModel):
    discrepancy_score: float
    stance: Literal["undervalued", "overvalued", "unclear", "mildly_undervalued", "mildly_overvalued"]
    confidence: float


class MemoSection(BaseModel):
    thesis: str
    technical_view: str
    news_sentiment_view: str
    historical_pattern_view: str
    risks: str
    final_verdict: str


class SourceRunItem(BaseModel):
    source_name: str
    status: Literal["completed", "failed", "fallback"]
    started_at: datetime | None
    finished_at: datetime | None
    num_of_steps: int | None
    article_count: int
    price_point_count: int
    error_message: str | None


class RunDiagnostics(BaseModel):
    source_success_count: int
    source_failure_count: int
    price_point_count: int
    technical_data_quality: Literal["strong", "usable", "limited", "insufficient"]
    sentiment_mode: str
    memo_mode: str
    fallback_reason: str | None


class RunDetailResponse(BaseModel):
    id: int
    ticker: str
    run_timestamp: datetime
    articles: list[ArticleItem]
    technical: TechnicalAssessment
    sentiment: SentimentAssessment
    historical: HistoricalAssessmentView
    final_assessment: FinalAssessment
    memo: MemoSection
    source_runs: list[SourceRunItem]
    diagnostics: RunDiagnostics


class RunHistoryItem(BaseModel):
    run_id: int
    ticker: str
    run_timestamp: datetime
    discrepancy_score: float
    stance: str

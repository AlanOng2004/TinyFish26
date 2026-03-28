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


class RunHistoryItem(BaseModel):
    run_id: int
    ticker: str
    run_timestamp: datetime
    discrepancy_score: float
    stance: str

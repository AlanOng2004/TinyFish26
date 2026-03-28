from datetime import datetime, timezone

from app.schemas.run import (
    ArticleItem,
    FinalAssessment,
    HistoricalAssessmentView,
    MemoSection,
    RunDetailResponse,
    SentimentAssessment,
    TechnicalAssessment,
)
from app.services.historical_patterns import score_historical_pattern
from app.services.memo_generator import generate_structured_memo
from app.services.normalization import normalize_tinyfish_payload
from app.services.scoring import combine_scores
from app.services.sentiment_analysis import score_news_sentiment
from app.services.technical_analysis import score_technical_signal
from app.services.tinyfish_client import fetch_ticker_context


def run_batch_analysis(ticker: str = "NVDA") -> RunDetailResponse:
    raw_payload = fetch_ticker_context(ticker=ticker)
    normalized = normalize_tinyfish_payload(raw_payload)

    technical = score_technical_signal(normalized["prices"])
    sentiment = score_news_sentiment(normalized["articles"])
    historical = score_historical_pattern(technical=technical, sentiment=sentiment)
    final_assessment = combine_scores(
        technical_score=technical["score"],
        sentiment_score=sentiment["score"],
        historical_score=historical["score"],
    )
    memo = generate_structured_memo(
        ticker=ticker,
        technical=technical,
        sentiment=sentiment,
        historical=historical,
        final_assessment=final_assessment,
    )

    return RunDetailResponse(
        id=1,
        ticker=ticker,
        run_timestamp=datetime.now(timezone.utc),
        articles=[ArticleItem(**article) for article in sentiment["articles"]],
        technical=TechnicalAssessment(**technical),
        sentiment=SentimentAssessment(
            score=sentiment["score"],
            label=sentiment["label"],
            top_catalysts=sentiment["top_catalysts"],
        ),
        historical=HistoricalAssessmentView(**historical),
        final_assessment=FinalAssessment(**final_assessment),
        memo=MemoSection(**memo),
    )

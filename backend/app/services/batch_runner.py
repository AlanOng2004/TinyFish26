from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.article import Article
from app.models.historical_assessment import HistoricalAssessment
from app.models.run import Run
from app.models.technical_snapshot import TechnicalSnapshot
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


def run_batch_analysis(db: Session, ticker: str = "NVDA") -> RunDetailResponse:
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

    db_run = Run(
        ticker=ticker,
        run_timestamp=datetime.now(timezone.utc),
        technical_score=technical["score"],
        sentiment_score=sentiment["score"],
        historical_score=historical["score"],
        discrepancy_score=final_assessment["discrepancy_score"],
        stance=final_assessment["stance"],
        confidence=final_assessment["confidence"],
        memo_thesis=memo["thesis"],
        memo_technical_view=memo["technical_view"],
        memo_news_view=memo["news_sentiment_view"],
        memo_historical_view=memo["historical_pattern_view"],
        memo_risks=memo["risks"],
        memo_final_verdict=memo["final_verdict"],
    )
    db.add(db_run)
    db.flush()

    for article in sentiment["articles"]:
        db.add(
            Article(
                run_id=db_run.id,
                title=article["title"],
                source=article["source"],
                published_at=article["published_at"],
                summary=article["summary"],
                sentiment=article["sentiment"],
                relevance_score=article["relevance_score"],
                catalyst_type=article["catalyst_type"],
            )
        )

    db.add(
        TechnicalSnapshot(
            run_id=db_run.id,
            short_ma=technical["short_ma"],
            long_ma=technical["long_ma"],
            rsi=technical["rsi"],
            technical_label=technical["label"],
        )
    )
    db.add(
        HistoricalAssessment(
            run_id=db_run.id,
            matched_pattern=historical["matched_pattern"],
            historical_label=historical["label"],
            rationale=historical["rationale"],
            pattern_score=historical["score"],
        )
    )

    db.commit()
    db.refresh(db_run)
    return build_run_response(db_run)


def build_run_response(db_run: Run) -> RunDetailResponse:
    articles = sorted(db_run.articles, key=lambda item: item.published_at, reverse=True)

    return RunDetailResponse(
        id=db_run.id,
        ticker=db_run.ticker,
        run_timestamp=db_run.run_timestamp,
        articles=[
            ArticleItem(
                title=article.title,
                source=article.source,
                published_at=article.published_at,
                summary=article.summary,
                sentiment=article.sentiment,
                relevance_score=article.relevance_score,
                catalyst_type=article.catalyst_type,
            )
            for article in articles
        ],
        technical=TechnicalAssessment(
            short_ma=db_run.technical_snapshot.short_ma,
            long_ma=db_run.technical_snapshot.long_ma,
            rsi=db_run.technical_snapshot.rsi,
            score=db_run.technical_score,
            label=db_run.technical_snapshot.technical_label,
        ),
        sentiment=SentimentAssessment(
            score=db_run.sentiment_score,
            label=resolve_sentiment_label(articles),
            top_catalysts=extract_top_catalysts(articles),
        ),
        historical=HistoricalAssessmentView(
            matched_pattern=db_run.historical_assessment.matched_pattern,
            score=db_run.historical_assessment.pattern_score,
            label=db_run.historical_assessment.historical_label,
            rationale=db_run.historical_assessment.rationale,
        ),
        final_assessment=FinalAssessment(
            discrepancy_score=db_run.discrepancy_score,
            stance=db_run.stance,
            confidence=db_run.confidence,
        ),
        memo=MemoSection(
            thesis=db_run.memo_thesis,
            technical_view=db_run.memo_technical_view,
            news_sentiment_view=db_run.memo_news_view,
            historical_pattern_view=db_run.memo_historical_view,
            risks=db_run.memo_risks,
            final_verdict=db_run.memo_final_verdict,
        ),
    )


def resolve_sentiment_label(articles: list[Article]) -> str:
    counts = {"bullish": 0, "bearish": 0, "neutral": 0}
    for article in articles:
        counts[article.sentiment] = counts.get(article.sentiment, 0) + 1
    return max(counts, key=counts.get)


def extract_top_catalysts(articles: list[Article]) -> list[str]:
    seen: set[str] = set()
    catalysts: list[str] = []
    for article in articles:
        if article.catalyst_type not in seen:
            seen.add(article.catalyst_type)
            catalysts.append(article.catalyst_type)
    return catalysts[:3]

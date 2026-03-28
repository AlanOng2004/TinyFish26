from datetime import datetime, timezone
from typing import Any


def normalize_tinyfish_payload(payload: dict[str, Any]) -> dict[str, Any]:
    articles: list[dict[str, Any]] = []
    prices: list[float] = []
    market_snapshots: list[dict[str, Any]] = []

    for source_run in payload.get("source_runs", []):
        result = source_run.get("result") or {}
        market_snapshot = result.get("market_snapshot")
        if isinstance(market_snapshot, dict):
            market_snapshots.append({"source_name": source_run.get("source_name"), **market_snapshot})

        for price in result.get("prices", []):
            normalized_price = normalize_price_value(price)
            if normalized_price is not None:
                prices.append(normalized_price)

        for article in result.get("articles", []):
            normalized_article = normalize_article(article)
            if normalized_article is not None:
                articles.append(normalized_article)

    deduped_articles = dedupe_articles(articles)[:10]
    recent_prices = prices[-10:] if len(prices) > 10 else prices

    return {
        "ticker": payload["ticker"],
        "articles": deduped_articles,
        "prices": recent_prices,
        "market_snapshots": market_snapshots,
    }


def normalize_article(article: dict[str, Any]) -> dict[str, Any] | None:
    title = article.get("title")
    summary = article.get("summary")
    if not title or not summary:
        return None

    return {
        "title": str(title).strip(),
        "source": str(article.get("source") or "Unknown").strip(),
        "published_at": normalize_timestamp(article.get("published_at")),
        "summary": str(summary).strip(),
        "excerpt": str(summary).strip(),
    }


def normalize_timestamp(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc)
    if isinstance(value, str) and value:
        cleaned = value.replace("Z", "+00:00")
        try:
            return datetime.fromisoformat(cleaned).astimezone(timezone.utc)
        except ValueError:
            pass
    return datetime.now(timezone.utc)


def normalize_price_value(value: Any) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        cleaned = value.replace("$", "").replace(",", "").strip()
        try:
            return float(cleaned)
        except ValueError:
            return None
    return None


def dedupe_articles(articles: list[dict[str, Any]]) -> list[dict[str, Any]]:
    deduped: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for article in sorted(articles, key=lambda item: item["published_at"], reverse=True):
        key = (article["title"].lower(), article["source"].lower())
        if key in seen:
            continue
        seen.add(key)
        deduped.append(article)
    return deduped

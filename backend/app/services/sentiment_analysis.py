from collections import Counter


def score_news_sentiment(articles: list[dict]) -> dict:
    enriched_articles = []
    labels = []
    catalysts = []

    for article in articles:
        text = f"{article['title']} {article['summary']}".lower()
        if "partnership" in text or "demand" in text or "growth" in text:
            label = "bullish"
            relevance = 0.88
            catalyst = "ai_demand"
        elif "valuation" in text or "risk" in text or "downgrade" in text:
            label = "bearish"
            relevance = 0.78
            catalyst = "valuation_pressure"
        else:
            label = "neutral"
            relevance = 0.65
            catalyst = "general_news"

        labels.append(label)
        catalysts.append(catalyst)
        enriched_articles.append(
            {
                **article,
                "sentiment": label,
                "relevance_score": relevance,
                "catalyst_type": catalyst,
            }
        )

    dominant = Counter(labels).most_common(1)[0][0] if labels else "neutral"
    score_map = {"bullish": 72.0, "neutral": 50.0, "bearish": 34.0}

    return {
        "articles": enriched_articles,
        "score": score_map[dominant],
        "label": dominant,
        "top_catalysts": list(dict.fromkeys(catalysts))[:3],
        "mode": "heuristic",
    }

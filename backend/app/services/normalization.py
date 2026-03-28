def normalize_tinyfish_payload(payload: dict) -> dict:
    articles = []
    for article in payload.get("articles", [])[:10]:
        articles.append(
            {
                "title": article["title"],
                "source": article["source"],
                "published_at": article["published_at"],
                "summary": article["summary"],
                "excerpt": article["excerpt"],
            }
        )

    return {
        "ticker": payload["ticker"],
        "articles": articles,
        "prices": payload.get("prices", []),
    }

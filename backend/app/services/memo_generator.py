def generate_structured_memo(
    ticker: str,
    technical: dict,
    sentiment: dict,
    historical: dict,
    final_assessment: dict,
) -> dict:
    return {
        "thesis": f"{ticker} shows a {final_assessment['stance'].replace('_', ' ')} setup over the next 1 to 2 weeks based on combined market, news, and pattern signals.",
        "technical_view": f"Short MA is {technical['short_ma']} versus long MA {technical['long_ma']}, with RSI at {technical['rsi']}. The technical regime is classified as {technical['label']}.",
        "news_sentiment_view": f"Recent article flow is assessed as {sentiment['label']} with primary catalysts: {', '.join(sentiment['top_catalysts']) or 'none identified'}.",
        "historical_pattern_view": f"The current setup most closely matches '{historical['matched_pattern']}', which is interpreted as {historical['label']}. {historical['rationale']}",
        "risks": "This MVP relies on scraped web context and heuristic scoring, so missing articles, incomplete price history, or noisy catalysts may distort the 1 to 2 week view.",
        "final_verdict": f"Final discrepancy score is {final_assessment['discrepancy_score']}, with confidence {final_assessment['confidence']}. Current stance: {final_assessment['stance'].replace('_', ' ')}.",
    }

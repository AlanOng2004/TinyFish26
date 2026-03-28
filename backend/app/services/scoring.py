def combine_scores(
    technical_score: float,
    sentiment_score: float,
    historical_score: float,
    price_point_count: int,
    source_failure_count: int,
) -> dict:
    discrepancy_score = round(
        (0.4 * technical_score) + (0.35 * sentiment_score) + (0.25 * historical_score),
        2,
    )

    if discrepancy_score >= 70:
        stance = "undervalued"
    elif discrepancy_score >= 55:
        stance = "mildly_undervalued"
    elif discrepancy_score >= 45:
        stance = "unclear"
    elif discrepancy_score >= 30:
        stance = "mildly_overvalued"
    else:
        stance = "overvalued"

    confidence = min(0.95, max(0.5, abs(discrepancy_score - 50) / 40 + 0.5))
    if price_point_count < 5:
        confidence -= 0.18
    elif price_point_count < 7:
        confidence -= 0.1
    elif price_point_count < 10:
        confidence -= 0.04
    confidence -= min(0.2, source_failure_count * 0.08)
    confidence = round(min(0.95, max(0.35, confidence)), 2)
    return {
        "discrepancy_score": discrepancy_score,
        "stance": stance,
        "confidence": confidence,
    }

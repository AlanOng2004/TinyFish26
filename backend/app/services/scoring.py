def combine_scores(technical_score: float, sentiment_score: float, historical_score: float) -> dict:
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

    confidence = round(min(0.95, max(0.5, abs(discrepancy_score - 50) / 40 + 0.5)), 2)
    return {
        "discrepancy_score": discrepancy_score,
        "stance": stance,
        "confidence": confidence,
    }

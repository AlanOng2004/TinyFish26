def score_historical_pattern(technical: dict, sentiment: dict) -> dict:
    if technical["label"] == "bullish" and sentiment["label"] == "bullish":
        return {
            "matched_pattern": "bullish_trend_positive_catalyst_cluster",
            "score": 74.0,
            "label": "bullish",
            "rationale": "Recent setups with trend support and positive catalysts tended to resolve upward over 1 to 2 weeks.",
        }
    if technical["label"] == "bearish" and sentiment["label"] == "bearish":
        return {
            "matched_pattern": "weak_trend_negative_catalyst_cluster",
            "score": 30.0,
            "label": "bearish",
            "rationale": "Comparable weak-momentum setups with negative catalyst flow often remained pressured in the following 1 to 2 weeks.",
        }
    return {
        "matched_pattern": "mixed_signal_consolidation",
        "score": 52.0,
        "label": "neutral",
        "rationale": "Mixed momentum and mixed news flow point to consolidation rather than a clear directional edge.",
    }

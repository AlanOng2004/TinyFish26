from statistics import mean


def compute_rsi(prices: list[float]) -> float:
    if len(prices) < 2:
        return 50.0

    gains = []
    losses = []
    for previous, current in zip(prices, prices[1:]):
        delta = current - previous
        if delta >= 0:
            gains.append(delta)
        else:
            losses.append(abs(delta))

    average_gain = mean(gains) if gains else 0.0
    average_loss = mean(losses) if losses else 1.0
    rs = average_gain / average_loss if average_loss else average_gain
    return round(100 - (100 / (1 + rs)), 2)


def score_technical_signal(prices: list[float]) -> dict:
    price_points = len(prices)
    if price_points >= 10:
        data_quality = "strong"
    elif price_points >= 7:
        data_quality = "usable"
    elif price_points >= 5:
        data_quality = "limited"
    else:
        data_quality = "insufficient"

    short_window = prices[-5:] if len(prices) >= 5 else prices
    long_window = prices[-10:] if len(prices) >= 10 else prices
    short_ma = round(mean(short_window), 2) if short_window else 0.0
    long_ma = round(mean(long_window), 2) if long_window else 0.0
    rsi = compute_rsi(prices)

    if data_quality == "insufficient":
        return {
            "short_ma": short_ma,
            "long_ma": long_ma,
            "rsi": rsi,
            "score": 50.0,
            "label": "neutral",
            "price_points": price_points,
            "data_quality": data_quality,
        }
    if short_ma > long_ma and rsi < 70:
        return {
            "short_ma": short_ma,
            "long_ma": long_ma,
            "rsi": rsi,
            "score": 76.0,
            "label": "bullish",
            "price_points": price_points,
            "data_quality": data_quality,
        }
    if short_ma < long_ma and rsi < 45:
        return {
            "short_ma": short_ma,
            "long_ma": long_ma,
            "rsi": rsi,
            "score": 32.0,
            "label": "bearish",
            "price_points": price_points,
            "data_quality": data_quality,
        }
    return {
        "short_ma": short_ma,
        "long_ma": long_ma,
        "rsi": rsi,
        "score": 52.0,
        "label": "neutral",
        "price_points": price_points,
        "data_quality": data_quality,
    }

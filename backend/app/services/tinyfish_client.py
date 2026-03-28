from datetime import datetime, timedelta, timezone


def fetch_ticker_context(ticker: str) -> dict:
    now = datetime.now(timezone.utc)
    return {
        "ticker": ticker,
        "articles": [
            {
                "title": f"{ticker} expands AI partnerships",
                "source": "MarketWire",
                "published_at": now - timedelta(hours=2),
                "summary": "Recent partnership headlines reinforce demand expectations.",
                "excerpt": "Partnership activity suggests strong enterprise AI momentum.",
            },
            {
                "title": f"{ticker} faces valuation debate ahead of earnings",
                "source": "Finance Daily",
                "published_at": now - timedelta(hours=5),
                "summary": "Analysts remain divided on near-term upside versus rich multiples.",
                "excerpt": "Investors are weighing strong growth against elevated expectations.",
            },
        ],
        "prices": [101.0, 103.5, 104.2, 106.0, 107.1, 108.4, 109.0, 110.2, 111.4, 112.6],
    }

from datetime import datetime, timedelta, timezone
from typing import Any

import httpx

from app.core.config import get_settings


class TinyFishError(RuntimeError):
    pass


SOURCE_CONFIGS = [
    {
        "name": "bloomberg_quote",
        "url": "https://www.bloomberg.com/quote/{ticker}:US",
        "goal_template": """
Extract a structured market snapshot for {ticker} from this quote page.
Return JSON with exactly these keys:
- market_snapshot: object with current_price, daily_change, daily_change_percent, market_cap, currency
- prices: array of up to 10 recent daily closing prices as numbers if visible, otherwise an empty array
- articles: empty array
Do not include commentary outside the JSON structure.
""".strip(),
    },
    {
        "name": "yahoo_quote",
        "url": "https://sg.finance.yahoo.com/quote/{ticker}/",
        "goal_template": """
Extract a structured market snapshot for {ticker} from this Yahoo Finance page.
Return JSON with exactly these keys:
- market_snapshot: object with current_price, daily_change, daily_change_percent, market_cap, currency
- prices: array of up to 10 recent daily closing prices as numbers if visible on the page, otherwise an empty array
- articles: empty array
Do not include commentary outside the JSON structure.
""".strip(),
    },
    {
        "name": "google_finance_news",
        "url": "https://www.google.com/finance/quote/{ticker}:NASDAQ",
        "goal_template": """
Extract the 5 most relevant recent news items about {ticker} from the Top News section on this page.
Return JSON with exactly these keys:
- market_snapshot: object with current_price, daily_change, daily_change_percent, market_cap, currency if visible, otherwise null values
- prices: array of up to 10 recent daily closing prices as numbers if visible, otherwise an empty array
- articles: array of up to 5 objects with title, source, published_at, summary
Use ISO-8601 for published_at when visible. If a field is missing, use null. Do not include commentary outside the JSON structure.
""".strip(),
    },
    {
        "name": "cnbc_news",
        "url": "https://www.cnbc.com/quotes/{ticker}",
        "goal_template": """
Extract the 5 most relevant recent news items about {ticker} from this CNBC quote page.
Return JSON with exactly these keys:
- market_snapshot: object with current_price, daily_change, daily_change_percent, market_cap, currency if visible, otherwise null values
- prices: array of up to 10 recent daily closing prices as numbers if visible, otherwise an empty array
- articles: array of up to 5 objects with title, source, published_at, summary
Use ISO-8601 for published_at when visible. If a field is missing, use null. Do not include commentary outside the JSON structure.
""".strip(),
    },
]


def fetch_ticker_context(ticker: str) -> dict[str, Any]:
    settings = get_settings()
    if not settings.tinyfish_api_key:
        return build_mock_context(ticker)

    source_runs = []
    source_errors = []
    selected_sources = resolve_enabled_sources(settings.enabled_tickers, settings.tinyfish_enabled_sources)
    timeout = httpx.Timeout(
        timeout=float(settings.tinyfish_request_timeout_seconds),
        connect=20.0,
        read=float(settings.tinyfish_request_timeout_seconds),
    )

    with httpx.Client(timeout=timeout) as client:
        for source in selected_sources:
            try:
                source_runs.append(run_tinyfish_source(client=client, ticker=ticker, source=source))
            except Exception as exc:
                source_errors.append({"source_name": source["name"], "error": str(exc)})

    if not source_runs:
        fallback = build_mock_context(ticker, enabled_source_names=settings.tinyfish_enabled_sources)
        fallback["source_errors"] = source_errors
        fallback["fallback_reason"] = "all_live_sources_failed"
        return fallback

    return {"ticker": ticker, "source_runs": source_runs, "source_errors": source_errors}


def run_tinyfish_source(client: httpx.Client, ticker: str, source: dict[str, str]) -> dict[str, Any]:
    settings = get_settings()
    payload = {
        "url": source["url"].format(ticker=ticker),
        "goal": source["goal_template"].format(ticker=ticker),
        "browser_profile": settings.tinyfish_browser_profile,
        "proxy_config": {
            "enabled": True,
            "country_code": settings.tinyfish_proxy_country_code,
        },
    }

    response = client.post(
        f"{settings.tinyfish_base_url}/automation/run",
        headers={
            "Content-Type": "application/json",
            "X-API-Key": settings.tinyfish_api_key,
        },
        json=payload,
    )
    response.raise_for_status()
    body = response.json()

    status = body.get("status")
    error = body.get("error")
    if status != "COMPLETED" or error is not None:
        raise TinyFishError(
            f"TinyFish run failed for {source['name']}: status={status}, error={error}"
        )

    return {
        "source_name": source["name"],
        "run_id": body.get("run_id"),
        "status": status,
        "started_at": body.get("started_at"),
        "finished_at": body.get("finished_at"),
        "num_of_steps": body.get("num_of_steps"),
        "result": body.get("result") or {},
    }


def build_mock_context(ticker: str, enabled_source_names: list[str] | None = None) -> dict[str, Any]:
    now = datetime.now(timezone.utc)
    source_runs = [
        {
            "source_name": "bloomberg_quote",
            "run_id": "mock-bloomberg",
            "status": "COMPLETED",
            "started_at": now.isoformat(),
            "finished_at": now.isoformat(),
            "num_of_steps": 3,
            "result": {
                "market_snapshot": {
                    "current_price": 112.6,
                    "daily_change": 1.2,
                    "daily_change_percent": 1.08,
                    "market_cap": "2.7T",
                    "currency": "USD",
                },
                "prices": [101.0, 103.5, 104.2, 106.0, 107.1],
                "articles": [],
            },
        },
        {
            "source_name": "yahoo_quote",
            "run_id": "mock-yahoo",
            "status": "COMPLETED",
            "started_at": now.isoformat(),
            "finished_at": now.isoformat(),
            "num_of_steps": 4,
            "result": {
                "market_snapshot": {
                    "current_price": 112.6,
                    "daily_change": 1.2,
                    "daily_change_percent": 1.08,
                    "market_cap": "2.7T",
                    "currency": "USD",
                },
                "prices": [108.4, 109.0, 110.2, 111.4, 112.6],
                "articles": [],
            },
        },
        {
            "source_name": "google_finance_news",
            "run_id": "mock-google",
            "status": "COMPLETED",
            "started_at": now.isoformat(),
            "finished_at": now.isoformat(),
            "num_of_steps": 5,
            "result": {
                "market_snapshot": {
                    "current_price": 112.6,
                    "daily_change": 1.2,
                    "daily_change_percent": 1.08,
                    "market_cap": "2.7T",
                    "currency": "USD",
                },
                "prices": [],
                "articles": [
                    {
                        "title": f"{ticker} expands AI partnerships",
                        "source": "Barron's",
                        "published_at": (now - timedelta(hours=2)).isoformat(),
                        "summary": "Recent partnership headlines reinforce demand expectations.",
                    },
                    {
                        "title": f"{ticker} gains as AI demand remains strong",
                        "source": "WSJ",
                        "published_at": (now - timedelta(hours=4)).isoformat(),
                        "summary": "Investors continue to focus on sustained data center demand.",
                    },
                ],
            },
        },
        {
            "source_name": "cnbc_news",
            "run_id": "mock-cnbc",
            "status": "COMPLETED",
            "started_at": now.isoformat(),
            "finished_at": now.isoformat(),
            "num_of_steps": 5,
            "result": {
                "market_snapshot": {
                    "current_price": 112.6,
                    "daily_change": 1.2,
                    "daily_change_percent": 1.08,
                    "market_cap": "2.7T",
                    "currency": "USD",
                },
                "prices": [],
                "articles": [
                    {
                        "title": f"{ticker} faces valuation debate ahead of earnings",
                        "source": "CNBC",
                        "published_at": (now - timedelta(hours=5)).isoformat(),
                        "summary": "Analysts remain divided on near-term upside versus rich multiples.",
                    },
                    {
                        "title": f"{ticker} remains in focus amid analyst calls",
                        "source": "CNBC",
                        "published_at": (now - timedelta(hours=7)).isoformat(),
                        "summary": "The stock remains central to AI trade positioning and analyst revisions.",
                    },
                ],
            },
        },
    ]
    allowed_names = set(enabled_source_names or [])
    filtered_runs = [run for run in source_runs if not allowed_names or run["source_name"] in allowed_names]
    return {
        "ticker": ticker,
        "source_runs": filtered_runs,
    }


def resolve_enabled_sources(
    enabled_tickers: list[str],
    enabled_source_names: list[str],
) -> list[dict[str, str]]:
    del enabled_tickers
    allowed_names = set(enabled_source_names)
    resolved = [source for source in SOURCE_CONFIGS if source["name"] in allowed_names]
    return resolved or [source for source in SOURCE_CONFIGS if source["name"] in {"yahoo_quote", "google_finance_news"}]

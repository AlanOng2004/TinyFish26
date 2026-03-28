# Autonomous Equity Analyst

An `NVDA`-first hackathon MVP that uses TinyFish web agents to collect live market context, then turns that data into an explainable short-horizon equity thesis.

The goal is not to build a trading bot. The goal is to build an agentic research workflow that can surface possible market discrepancies by combining:

- live financial news
- market and quote page context
- technical signals
- historical pattern heuristics
- LLM-generated analyst reasoning

This MVP is designed for a `1 to 2 week` outlook and currently supports `batch analysis` with a `web dashboard`.

## What It Does

For each scheduled or manually triggered run, the system:

1. Scrapes recent `NVDA` market context with TinyFish.
2. Normalizes the scraped output into structured records.
3. Scores the ticker across three signal families:
   - technical analysis
   - news sentiment
   - historical pattern similarity
4. Aggregates those signals into a single discrepancy score.
5. Produces a structured analyst memo with thesis, evidence, risks, and final verdict.
6. Stores the run in Postgres so the dashboard can show score changes over time.

## Why This Is Interesting

Most stock dashboards either show raw data or a black-box prediction. This project aims for a more inspectable middle ground:

- TinyFish handles live, concurrent web collection.
- The backend converts noisy web pages into structured financial context.
- Scoring stays transparent and explainable.
- OpenAI is used for synthesis and memo generation rather than replacing the entire pipeline.

That makes the output easier to demo, debug, and trust.

## Current MVP Scope

- `Ticker support`: dropdown exists, but only `NVDA` is enabled
- `Run mode`: scheduled every `60 minutes` and manually triggerable
- `Time horizon`: `1 to 2 weeks`
- `Technical indicators`: moving averages and RSI
- `News volume`: top 10 recent items
- `Historical analysis`: simple rule-based pattern matching
- `Output`: structured analyst memo plus score history

## Architecture

### Backend

- `FastAPI` for API endpoints
- `SQLAlchemy` for ORM models
- `Alembic` for migrations
- `Postgres` for persistence
- `APScheduler` for recurring batch runs

### Frontend

- `React`
- `Vite`
- `Recharts` for historical score visualization

## Analysis Pipeline

### 1. TinyFish Collection

TinyFish agents are responsible for gathering:

- recent financial news
- quote and market pages
- catalyst-relevant pages

The current codebase already has a service boundary for this in:

- `backend/app/services/tinyfish_client.py`

### 2. Normalization

Scraped pages are normalized into structured fields such as:

- title
- source
- published timestamp
- summary
- extracted sentiment-relevant text

### 3. Technical Analysis

The MVP technical layer computes:

- short moving average
- long moving average
- RSI

These are converted into a technical score and label.

### 4. News Sentiment

The sentiment layer evaluates the top 10 articles and assigns:

- bullish / bearish / neutral sentiment
- relevance score
- catalyst type

These are then aggregated into a run-level sentiment score.

### 5. Historical Pattern Matching

The historical layer uses simple rules to classify the current setup into patterns such as:

- bullish trend with positive catalysts
- weak trend with negative catalysts
- mixed-signal consolidation

This keeps the system interpretable for a hackathon demo.

### 6. Final Scoring

The three signal families are combined into a single discrepancy score using fixed weights:

- `technical`: 40%
- `sentiment`: 35%
- `historical`: 25%

The final output is mapped to a stance such as:

- `undervalued`
- `mildly_undervalued`
- `unclear`
- `mildly_overvalued`
- `overvalued`

### 7. Analyst Memo

Each run also produces a strict memo with these sections:

- Thesis
- Technical View
- News Sentiment View
- Historical Pattern View
- Risks
- Final Verdict

## Dashboard

The frontend dashboard is built to make the reasoning visible, not just the score.

Current views:

- latest discrepancy score
- signal breakdown
- structured analyst memo
- top analyzed articles
- score history over time

## Repository Layout

```text
backend/
  app/
    api/
      routes/
    core/
    db/
    models/
    schemas/
    services/
  alembic/

frontend/
  src/
    api/
    charts/
    components/
    pages/
```

## API Endpoints

- `GET /health`
- `POST /runs/trigger`
- `GET /runs/latest?ticker=NVDA`
- `GET /runs/history?ticker=NVDA`
- `GET /runs/{id}`

## Local Setup

### Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

The backend expects a running Postgres instance. Update `DATABASE_URL` in `backend/.env` as needed.

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

By default, the frontend expects the API at:

- `http://localhost:8000`

## Environment Files

Backend template:

- `backend/.env.example`

Frontend template:

- `frontend/.env.example`

## Current Status

Implemented:

- project structure
- backend API skeleton
- Postgres models
- Alembic scaffold
- scheduled/manual run flow
- persisted run history
- TinyFish HTTP client with configurable source goals
- OpenAI-backed structured sentiment and memo services with deterministic fallback
- frontend dashboard
- API-backed frontend client

Still placeholder:

- production-quality price/history sourcing

## TinyFish Sources

The current TinyFish source plan uses:

- Yahoo Finance quote page for market snapshot and visible price context
- Google Finance NVDA page for top news aggregation

Optional sources kept in code but disabled by default for faster live demo runs:

- Bloomberg quote page for market snapshot
- CNBC NVDA page for company-specific news flow

The service sends narrowly scoped extraction goals to TinyFish and expects structured JSON in the response `result`.

If `TINYFISH_API_KEY` is not set, the backend falls back to mock data so the app remains runnable during UI development.

## Next Steps

The next implementation step is improving price-history quality and tightening the technical-analysis input source so moving averages and RSI rely on stronger market data than whatever is visible on scraped pages.

import { useEffect, useState } from "react";

import { fetchLatestRun, fetchRunHistory, triggerRun } from "../api/client";
import { HistoryChart } from "../charts/HistoryChart";
import { ArticleTable } from "../components/ArticleTable";
import { MemoPanel } from "../components/MemoPanel";
import { ScoreCard } from "../components/ScoreCard";
import { TickerSelector } from "../components/TickerSelector";

export function DashboardPage() {
  const [ticker, setTicker] = useState("NVDA");
  const [run, setRun] = useState(null);
  const [history, setHistory] = useState([]);

  useEffect(() => {
    async function load() {
      const [latest, historyItems] = await Promise.all([
        fetchLatestRun(ticker),
        fetchRunHistory(ticker),
      ]);
      setRun(latest);
      setHistory(historyItems);
    }

    load();
  }, [ticker]);

  async function handleTrigger() {
    const nextRun = await triggerRun(ticker);
    setRun(nextRun);
    setHistory((current) => [
      ...current,
      {
        run_id: nextRun.id,
        ticker: nextRun.ticker,
        run_timestamp: nextRun.run_timestamp,
        discrepancy_score: nextRun.final_assessment.discrepancy_score,
        stance: nextRun.final_assessment.stance,
      },
    ]);
  }

  if (!run) {
    return <main className="app-shell">Loading...</main>;
  }

  return (
    <main className="app-shell">
      <section className="hero">
        <div>
          <p className="eyebrow">TinyFish Hackathon MVP</p>
          <h1>Autonomous Equity Analyst</h1>
          <p className="hero-copy">
            Scheduled NVDA analysis that combines TinyFish web scraping, signal scoring,
            and a structured analyst memo for a 1 to 2 week horizon.
          </p>
        </div>
        <div className="hero-controls">
          <TickerSelector value={ticker} onChange={setTicker} />
          <button className="run-button" onClick={handleTrigger}>
            Run Analysis
          </button>
        </div>
      </section>

      <section className="score-grid">
        <ScoreCard
          title="Discrepancy Score"
          value={run.final_assessment.discrepancy_score}
          subtitle={run.final_assessment.stance.replaceAll("_", " ")}
        />
        <ScoreCard
          title="Technical Score"
          value={run.technical.score}
          subtitle={`MA ${run.technical.short_ma} / ${run.technical.long_ma}, RSI ${run.technical.rsi}`}
        />
        <ScoreCard
          title="Sentiment Score"
          value={run.sentiment.score}
          subtitle={run.sentiment.top_catalysts.join(", ")}
        />
        <ScoreCard
          title="Historical Score"
          value={run.historical.score}
          subtitle={run.historical.matched_pattern.replaceAll("_", " ")}
        />
      </section>

      <section className="content-grid">
        <MemoPanel memo={run.memo} />
        <HistoryChart data={history} />
      </section>

      <ArticleTable articles={run.articles} />
    </main>
  );
}

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
  const [loading, setLoading] = useState(true);
  const [isTriggering, setIsTriggering] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    async function load() {
      setLoading(true);
      setError("");
      try {
        const historyItems = await fetchRunHistory(ticker);
        setHistory(historyItems);
        try {
          const latest = await fetchLatestRun(ticker);
          setRun(latest);
        } catch (latestError) {
          if (latestError.status === 404) {
            setRun(null);
          } else {
            throw latestError;
          }
        }
      } catch (loadError) {
        setError(loadError.message);
      } finally {
        setLoading(false);
      }
    }

    load();
  }, [ticker]);

  async function handleTrigger() {
    setIsTriggering(true);
    setError("");
    try {
      const nextRun = await triggerRun(ticker);
      setRun(nextRun);
      const nextHistory = await fetchRunHistory(ticker);
      setHistory(nextHistory);
    } catch (triggerError) {
      setError(triggerError.message);
    } finally {
      setIsTriggering(false);
    }
  }

  if (loading) {
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
          <button className="run-button" onClick={handleTrigger} disabled={isTriggering}>
            {isTriggering ? "Running..." : "Run Analysis"}
          </button>
        </div>
      </section>

      {error ? <section className="panel error-panel">{error}</section> : null}

      {!run ? (
        <section className="panel empty-panel">
          <h2>No Analysis Yet</h2>
          <p>Trigger the first NVDA batch run to populate the dashboard.</p>
        </section>
      ) : (
        <>
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
        </>
      )}
    </main>
  );
}

import { startTransition, useEffect, useEffectEvent, useState } from "react";

import {
  API_BASE_URL,
  fetchHealth,
  fetchLatestRun,
  fetchRunHistory,
  triggerRun,
} from "../api/client";
import { HistoryChart } from "../charts/HistoryChart";
import { ArticleTable } from "../components/ArticleTable";
import { MemoPanel } from "../components/MemoPanel";
import { ScoreCard } from "../components/ScoreCard";
import { TickerSelector } from "../components/TickerSelector";
import {
  formatConfidence,
  formatList,
  formatRelativeTime,
  formatScore,
  formatTimestamp,
  getLabelTone,
  getScoreTone,
  titleCaseLabel,
} from "../lib/formatters";

function buildHealthState(payload) {
  if (payload?.status === "ok") {
    return {
      state: "online",
      label: "API online",
      detail: "Connected to the remote stock analysis backend and database.",
    };
  }

  if (payload?.status === "degraded") {
    return {
      state: "warning",
      label: "Backend degraded",
      detail: payload?.database?.detail ?? "The backend is reachable, but its database is unhealthy.",
    };
  }

  return {
    state: "offline",
    label: "API unavailable",
    detail: "The configured backend could not be reached from the browser.",
  };
}

export function DashboardPage() {
  const [ticker, setTicker] = useState("NVDA");
  const [run, setRun] = useState(null);
  const [history, setHistory] = useState([]);
  const [health, setHealth] = useState({
    state: "checking",
    label: "Checking API",
    detail: "Verifying remote backend connectivity.",
  });
  const [loading, setLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [isTriggering, setIsTriggering] = useState(false);
  const [error, setError] = useState("");

  const loadDashboard = useEffectEvent(
    async (nextTicker, { pageLoad = false, refreshHealth = false } = {}) => {
      if (pageLoad) {
        setLoading(true);
      } else {
        setIsRefreshing(true);
      }

      setError("");

      try {
        const healthPromise = refreshHealth
          ? fetchHealth()
              .then((payload) => buildHealthState(payload))
              .catch(() => buildHealthState(null))
          : Promise.resolve(null);

        const historyPromise = fetchRunHistory(nextTicker);
        const latestPromise = fetchLatestRun(nextTicker).catch((latestError) => {
          if (latestError.status === 404) {
            return null;
          }

          throw latestError;
        });

        const [healthResult, historyItems, latestRun] = await Promise.all([
          healthPromise,
          historyPromise,
          latestPromise,
        ]);

        startTransition(() => {
          if (healthResult) {
            setHealth(healthResult);
          }
          setHistory(Array.isArray(historyItems) ? historyItems : []);
          setRun(latestRun);
        });
      } catch (loadError) {
        setError(loadError.message);

        if (refreshHealth) {
          startTransition(() => {
            setHealth(buildHealthState(null));
          });
        }
      } finally {
        if (pageLoad) {
          setLoading(false);
        } else {
          setIsRefreshing(false);
        }
      }
    },
  );

  useEffect(() => {
    void loadDashboard(ticker, { pageLoad: true, refreshHealth: true });
  }, [ticker]);

  async function handleRefresh() {
    setIsTriggering(true);
    setError("");

    try {
      const nextRun = await triggerRun(ticker);
      const nextHistory = await fetchRunHistory(ticker);

      startTransition(() => {
        setRun(nextRun);
        setHistory(Array.isArray(nextHistory) ? nextHistory : []);
        setHealth(buildHealthState({ status: "ok" }));
      });
    } catch (triggerError) {
      setError(triggerError.message);
      startTransition(() => {
        setHealth(buildHealthState(null));
      });
    } finally {
      setIsTriggering(false);
    }
  }

  function handleReload() {
    void loadDashboard(ticker, { refreshHealth: true });
  }

  if (loading) {
    return (
      <main className="app-shell">
        <section className="panel loading-panel">
          <span className="section-kicker">Loading Dashboard</span>
          <h1>Preparing the equity analyst workspace.</h1>
          <p>
            Pulling health, latest run, and stored history from the configured stock
            backend.
          </p>
        </section>
      </main>
    );
  }

  const lastRunLabel = run
    ? `${formatTimestamp(run.run_timestamp, "full")} (${formatRelativeTime(
        run.run_timestamp,
      )})`
    : "Waiting for the first completed run.";

  const historyLabel = history.length
    ? `${history.length} stored run${history.length === 1 ? "" : "s"}`
    : "No stored history yet";

  const catalystLabel = run
    ? formatList(run.sentiment.top_catalysts)
    : "Refresh the board to identify the top catalysts.";
  const sourceSummary = run
    ? `${run.diagnostics.source_success_count} success / ${run.diagnostics.source_failure_count} failed`
    : "Waiting for first run";

  return (
    <main className="app-shell">
      <section className="hero">
        <section className="panel hero-copy-block">
          <div className="hero-topline">
            <p className="eyebrow">Stocks Control Room</p>
            <span className={`status-pill status-pill-${health.state}`}>
              {health.label}
            </span>
          </div>
          <p className="eyebrow">TinyFish Hackathon</p>
          <h1>Short-horizon equity readout built for live demo.</h1>
          <p className="hero-copy">
            This dashboard assumes a remote backend at <code>{API_BASE_URL}</code> and
            turns each run into a clear stance, signal breakdown, history curve, and
            memo you can walk through with confidence.
          </p>
          <p className="hero-supporting-copy">{health.detail}</p>
          <div className="hero-meta-grid">
            <article className="hero-meta-card">
              <span className="field-label">Active ticker</span>
              <strong>{ticker}</strong>
              <p>Current pilot universe for the frontend and backend flow.</p>
            </article>
            <article className="hero-meta-card">
              <span className="field-label">Latest completed run</span>
              <strong>{run ? formatRelativeTime(run.run_timestamp) : "Not seeded yet"}</strong>
              <p>{lastRunLabel}</p>
            </article>
            <article className="hero-meta-card">
              <span className="field-label">Stored history</span>
              <strong>{history.length}</strong>
              <p>{historyLabel}</p>
            </article>
            <article className="hero-meta-card">
              <span className="field-label">Source health</span>
              <strong>{run ? sourceSummary : "Not available"}</strong>
              <p>Tracks TinyFish source completion and failure pressure per run.</p>
            </article>
          </div>
        </section>

        <section className="panel hero-controls">
          <TickerSelector
            value={ticker}
            onChange={setTicker}
            disabled={isRefreshing || isTriggering}
          />
          <div className="button-row">
            <button
              className="ghost-button"
              onClick={handleRefresh}
              disabled={isRefreshing || isTriggering}
            >
              {isTriggering ? "Refreshing history..." : "Refresh board"}
            </button>
            <button
              className="run-button"
              onClick={handleReload}
              disabled={isTriggering || isRefreshing}
            >
              {isRefreshing ? "Reloading board..." : "Reload saved board"}
            </button>
          </div>
          <p className="control-note">
            Refresh board creates a brand-new persisted run and updates stored history.
            Reload saved board only re-reads the latest saved data from the backend.
          </p>
        </section>
      </section>

      {error ? (
        <section className="panel notice-panel notice-error">
          <span className="section-kicker">API Message</span>
          <p>{error}</p>
        </section>
      ) : null}

      {!run ? (
        <section className="panel empty-panel">
          <span className="section-kicker">No Analysis Yet</span>
          <h2>Refresh the board to seed the first stored run.</h2>
          <p>
            The shell is ready, but there is no completed analysis payload for the
            selected ticker yet.
          </p>
          <div className="empty-grid">
            <article className="empty-step">
              <strong>1. Confirm backend reachability</strong>
              <p>
                The health badge above should say the API is online if the browser can
                reach <code>{API_BASE_URL}</code>.
              </p>
            </article>
            <article className="empty-step">
              <strong>2. Generate a run</strong>
              <p>
                Use <span className="inline-chip">Refresh board</span> to create the first
                persisted result for NVDA.
              </p>
            </article>
            <article className="empty-step">
              <strong>3. Review the storytelling layer</strong>
              <p>
                Once a run lands, the memo, chart, and article cards will populate
                automatically.
              </p>
            </article>
          </div>
        </section>
      ) : (
        <>
          <section className="score-grid">
            <ScoreCard
              eyebrow="Master Signal"
              title="Discrepancy score"
              value={formatScore(run.final_assessment.discrepancy_score)}
              subtitle={titleCaseLabel(run.final_assessment.stance)}
              detail={`Confidence ${formatConfidence(
                run.final_assessment.confidence,
              )} • ${historyLabel}`}
              meterValue={run.final_assessment.discrepancy_score}
              tone={getLabelTone(run.final_assessment.stance)}
              featured
            />
            <ScoreCard
              eyebrow="Technical"
              title="Momentum stack"
              value={formatScore(run.technical.score)}
              subtitle={titleCaseLabel(run.technical.label)}
              detail={`Short MA ${formatScore(run.technical.short_ma)} / Long MA ${formatScore(
                run.technical.long_ma,
              )} • RSI ${formatScore(run.technical.rsi)} • ${run.technical.price_points} price points`}
              meterValue={run.technical.score}
              tone={getLabelTone(run.technical.label)}
            />
            <ScoreCard
              eyebrow="Sentiment"
              title="News pressure"
              value={formatScore(run.sentiment.score)}
              subtitle={titleCaseLabel(run.sentiment.label)}
              detail={catalystLabel}
              meterValue={run.sentiment.score}
              tone={getLabelTone(run.sentiment.label)}
            />
            <ScoreCard
              eyebrow="Historical"
              title="Pattern match"
              value={formatScore(run.historical.score)}
              subtitle={titleCaseLabel(run.historical.label)}
              detail={titleCaseLabel(run.historical.matched_pattern)}
              meterValue={run.historical.score}
              tone={getLabelTone(run.historical.label)}
            />
            <ScoreCard
              eyebrow="Confidence"
              title="Decision quality"
              value={formatConfidence(run.final_assessment.confidence)}
              subtitle="Memo confidence"
              detail={`${titleCaseLabel(run.technical.data_quality)} technical data • ${sourceSummary}`}
              meterValue={run.final_assessment.confidence * 100}
              tone={getScoreTone(run.final_assessment.discrepancy_score)}
            />
          </section>

          <section className="diagnostics-grid">
            <article className="panel diagnostic-panel">
              <span className="section-kicker">Run diagnostics</span>
              <h2>Confidence inputs</h2>
              <dl className="diagnostic-list">
                <div>
                  <dt>Technical data quality</dt>
                  <dd>{titleCaseLabel(run.diagnostics.technical_data_quality)}</dd>
                </div>
                <div>
                  <dt>Price points</dt>
                  <dd>{run.diagnostics.price_point_count}</dd>
                </div>
                <div>
                  <dt>Sentiment mode</dt>
                  <dd>{titleCaseLabel(run.diagnostics.sentiment_mode)}</dd>
                </div>
                <div>
                  <dt>Memo mode</dt>
                  <dd>{titleCaseLabel(run.diagnostics.memo_mode)}</dd>
                </div>
              </dl>
              {run.diagnostics.fallback_reason ? (
                <p className="diagnostic-note">
                  Fallback reason: {titleCaseLabel(run.diagnostics.fallback_reason)}
                </p>
              ) : null}
            </article>

            <article className="panel diagnostic-panel">
              <span className="section-kicker">TinyFish sources</span>
              <h2>Collection status</h2>
              <div className="source-run-list">
                {run.source_runs.map((sourceRun) => (
                  <article
                    key={`${sourceRun.source_name}-${sourceRun.status}-${sourceRun.started_at ?? "na"}`}
                    className="source-run-card"
                    data-status={sourceRun.status}
                  >
                    <div className="source-run-topline">
                      <strong>{titleCaseLabel(sourceRun.source_name)}</strong>
                      <span>{titleCaseLabel(sourceRun.status)}</span>
                    </div>
                    <p>
                      {sourceRun.article_count} articles • {sourceRun.price_point_count} price
                      points
                    </p>
                    <p>
                      {sourceRun.finished_at
                        ? `Completed ${formatRelativeTime(sourceRun.finished_at)}`
                        : "No completion timestamp"}
                    </p>
                    {sourceRun.error_message ? (
                      <p className="source-run-error">{sourceRun.error_message}</p>
                    ) : null}
                  </article>
                ))}
              </div>
            </article>
          </section>

          <section className="insight-grid">
            <article
              className="panel insight-card"
              data-tone={getLabelTone(run.final_assessment.stance)}
            >
              <span className="section-kicker">Current stance</span>
              <h2>{titleCaseLabel(run.final_assessment.stance)}</h2>
              <p>{run.memo.final_verdict}</p>
            </article>
            <article className="panel insight-card">
              <span className="section-kicker">Catalyst radar</span>
              <h2>{formatList(run.sentiment.top_catalysts)}</h2>
              <p>{run.memo.news_sentiment_view}</p>
            </article>
            <article className="panel insight-card">
              <span className="section-kicker">Historical setup</span>
              <h2>{titleCaseLabel(run.historical.matched_pattern)}</h2>
              <p>{run.historical.rationale}</p>
            </article>
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

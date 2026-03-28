export function MemoPanel({ memo }) {
  const sections = [
    { title: "Thesis", body: memo.thesis },
    { title: "Technical View", body: memo.technical_view },
    { title: "News Sentiment View", body: memo.news_sentiment_view },
    { title: "Historical Pattern View", body: memo.historical_pattern_view },
    { title: "Risks", body: memo.risks },
    { title: "Final Verdict", body: memo.final_verdict },
  ];

  return (
    <section className="panel memo-panel">
      <div className="section-heading">
        <div>
          <span className="section-kicker">Analyst Memo</span>
          <h2>Reasoning trace</h2>
        </div>
        <p>Every run carries an explainable narrative instead of a bare score.</p>
      </div>
      <div className="memo-grid">
        {sections.map((section) => (
          <article key={section.title} className="memo-section">
            <h3>{section.title}</h3>
            <p>{section.body || "Narrative unavailable for this run."}</p>
          </article>
        ))}
      </div>
    </section>
  );
}

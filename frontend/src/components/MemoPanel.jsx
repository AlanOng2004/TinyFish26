export function MemoPanel({ memo }) {
  return (
    <section className="panel memo-panel">
      <h2>Analyst Memo</h2>
      <div>
        <h3>Thesis</h3>
        <p>{memo.thesis}</p>
      </div>
      <div>
        <h3>Technical View</h3>
        <p>{memo.technical_view}</p>
      </div>
      <div>
        <h3>News Sentiment View</h3>
        <p>{memo.news_sentiment_view}</p>
      </div>
      <div>
        <h3>Historical Pattern View</h3>
        <p>{memo.historical_pattern_view}</p>
      </div>
      <div>
        <h3>Risks</h3>
        <p>{memo.risks}</p>
      </div>
      <div>
        <h3>Final Verdict</h3>
        <p>{memo.final_verdict}</p>
      </div>
    </section>
  );
}

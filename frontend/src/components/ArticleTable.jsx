import {
  formatRelativeTime,
  formatScore,
  formatTimestamp,
  getLabelTone,
  titleCaseLabel,
} from "../lib/formatters";

export function ArticleTable({ articles }) {
  if (!articles.length) {
    return (
      <section className="panel article-panel">
        <div className="section-heading">
          <div>
            <span className="section-kicker">News Deck</span>
            <h2>Top analyzed articles</h2>
          </div>
          <p>No article-level context has been stored for this run yet.</p>
        </div>
      </section>
    );
  }

  return (
    <section className="panel article-panel">
      <div className="section-heading">
        <div>
          <span className="section-kicker">News Deck</span>
          <h2>Top analyzed articles</h2>
        </div>
        <p>{articles.length} ranked items carried into the run-level thesis.</p>
      </div>
      <div className="article-list">
        {articles.map((article) => (
          <article
            key={`${article.title}-${article.published_at}`}
            className="article-card"
            data-tone={getLabelTone(article.sentiment)}
          >
            <div className="badge-row">
              <span className={`badge badge-${getLabelTone(article.sentiment)}`}>
                {titleCaseLabel(article.sentiment)}
              </span>
              <span className="badge badge-outline">
                {titleCaseLabel(article.catalyst_type)}
              </span>
            </div>
            <div className="article-card-head">
              <div>
                <span className="article-source">{article.source}</span>
                <h3>{article.title}</h3>
              </div>
              <span className="article-time">
                {formatRelativeTime(article.published_at)}
              </span>
            </div>
            <p>{article.summary}</p>
            <div className="article-meta">
              <span>Published {formatTimestamp(article.published_at, "full")}</span>
              <span>Relevance {formatScore(article.relevance_score)}</span>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

export function ArticleTable({ articles }) {
  return (
    <section className="panel">
      <h2>Top Articles</h2>
      <table className="article-table">
        <thead>
          <tr>
            <th>Title</th>
            <th>Source</th>
            <th>Sentiment</th>
            <th>Catalyst</th>
          </tr>
        </thead>
        <tbody>
          {articles.map((article) => (
            <tr key={`${article.title}-${article.published_at}`}>
              <td>{article.title}</td>
              <td>{article.source}</td>
              <td>{article.sentiment}</td>
              <td>{article.catalyst_type}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}

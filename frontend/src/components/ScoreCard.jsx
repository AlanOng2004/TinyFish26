export function ScoreCard({ title, value, subtitle }) {
  return (
    <article className="panel score-card">
      <span className="label">{title}</span>
      <strong>{value}</strong>
      <p>{subtitle}</p>
    </article>
  );
}

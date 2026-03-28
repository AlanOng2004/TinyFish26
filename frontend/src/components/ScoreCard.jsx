export function ScoreCard({
  eyebrow,
  title,
  value,
  subtitle,
  detail,
  meterValue,
  tone = "neutral",
  featured = false,
}) {
  const clampedMeter =
    typeof meterValue === "number" && Number.isFinite(meterValue)
      ? Math.max(0, Math.min(100, meterValue))
      : 0;

  return (
    <article
      className={`panel score-card ${featured ? "score-card-featured" : ""}`}
      data-tone={tone}
    >
      <div className="score-card-header">
        <div>
          <span className="score-kicker">{eyebrow}</span>
          <h2>{title}</h2>
        </div>
        <span className="score-orb" aria-hidden="true" />
      </div>
      <strong className="score-value">{value}</strong>
      <p className="score-subtitle">{subtitle}</p>
      {detail ? <p className="score-detail">{detail}</p> : null}
      <div className="score-meter" aria-hidden="true">
        <span style={{ width: `${clampedMeter}%` }} />
      </div>
    </article>
  );
}

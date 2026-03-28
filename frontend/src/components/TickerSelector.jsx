const ENABLED_TICKERS = ["NVDA"];

export function TickerSelector({ value, onChange, disabled = false }) {
  return (
    <label className="panel control-card">
      <span className="field-label">Ticker</span>
      <select
        value={value}
        onChange={(event) => onChange(event.target.value)}
        disabled={disabled}
      >
        {ENABLED_TICKERS.map((ticker) => (
          <option key={ticker} value={ticker}>
            {ticker}
          </option>
        ))}
      </select>
      <span className="field-hint">
        Pilot mode is locked to NVDA while the backend contract settles.
      </span>
    </label>
  );
}

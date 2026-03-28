const ENABLED_TICKERS = ["NVDA"];

export function TickerSelector({ value, onChange }) {
  return (
    <label className="panel">
      <span className="label">Ticker</span>
      <select value={value} onChange={(event) => onChange(event.target.value)}>
        {ENABLED_TICKERS.map((ticker) => (
          <option key={ticker} value={ticker}>
            {ticker}
          </option>
        ))}
      </select>
    </label>
  );
}

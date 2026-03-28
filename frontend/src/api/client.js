const demoRun = {
  id: 1,
  ticker: "NVDA",
  run_timestamp: new Date().toISOString(),
  technical: {
    short_ma: 110.32,
    long_ma: 107.74,
    rsi: 64.2,
    score: 76,
    label: "bullish",
  },
  sentiment: {
    score: 72,
    label: "bullish",
    top_catalysts: ["ai_demand", "valuation_pressure"],
  },
  historical: {
    matched_pattern: "bullish_trend_positive_catalyst_cluster",
    score: 74,
    label: "bullish",
    rationale:
      "Recent setups with trend support and positive catalysts tended to resolve upward over 1 to 2 weeks.",
  },
  final_assessment: {
    discrepancy_score: 74.2,
    stance: "undervalued",
    confidence: 0.91,
  },
  memo: {
    thesis:
      "NVDA shows an undervalued setup over the next 1 to 2 weeks based on combined market, news, and pattern signals.",
    technical_view:
      "Short MA is above long MA and RSI remains below extreme overbought conditions.",
    news_sentiment_view:
      "Recent article flow is net bullish, led by AI demand and partnership themes.",
    historical_pattern_view:
      "The setup resembles prior bullish trend plus catalyst clusters that resolved positively.",
    risks:
      "Valuation compression, macro risk, or incomplete scraped context may weaken the current thesis.",
    final_verdict:
      "The system currently flags NVDA as likely undervalued on a 1 to 2 week horizon.",
  },
  articles: [
    {
      title: "NVDA expands AI partnerships",
      source: "MarketWire",
      published_at: new Date().toISOString(),
      summary: "Recent partnership headlines reinforce demand expectations.",
      sentiment: "bullish",
      relevance_score: 0.88,
      catalyst_type: "ai_demand",
    },
    {
      title: "NVDA faces valuation debate ahead of earnings",
      source: "Finance Daily",
      published_at: new Date().toISOString(),
      summary: "Analysts remain divided on near-term upside versus rich multiples.",
      sentiment: "bearish",
      relevance_score: 0.78,
      catalyst_type: "valuation_pressure",
    },
  ],
};

const demoHistory = [
  { run_id: 1, ticker: "NVDA", run_timestamp: "2026-03-28T00:00:00Z", discrepancy_score: 61.5, stance: "mildly_undervalued" },
  { run_id: 2, ticker: "NVDA", run_timestamp: "2026-03-28T06:00:00Z", discrepancy_score: 67.8, stance: "mildly_undervalued" },
  { run_id: 3, ticker: "NVDA", run_timestamp: "2026-03-28T12:00:00Z", discrepancy_score: 74.2, stance: "undervalued" },
];

export async function fetchLatestRun() {
  return demoRun;
}

export async function fetchRunHistory() {
  return demoHistory;
}

export async function triggerRun(ticker) {
  return { ...demoRun, ticker };
}

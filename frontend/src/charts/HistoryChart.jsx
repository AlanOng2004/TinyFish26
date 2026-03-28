import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import {
  formatAxisTick,
  formatRelativeTime,
  formatScore,
  formatTimestamp,
  titleCaseLabel,
} from "../lib/formatters";

function HistoryTooltip({ active, payload }) {
  if (!active || !payload?.length) {
    return null;
  }

  const point = payload[0].payload;

  return (
    <div className="chart-tooltip">
      <strong>{formatScore(point.discrepancy_score)}</strong>
      <span>{titleCaseLabel(point.stance)}</span>
      <p>{formatTimestamp(point.run_timestamp, "full")}</p>
      <p>{formatRelativeTime(point.run_timestamp)}</p>
    </div>
  );
}

export function HistoryChart({ data }) {
  if (!data.length) {
    return (
      <section className="panel chart-panel">
        <div className="section-heading">
          <div>
            <span className="section-kicker">Score History</span>
            <h2>Run trendline</h2>
          </div>
          <p>History appears after the first completed analysis run.</p>
        </div>
        <div className="chart-empty">
          <p>No historical points yet.</p>
        </div>
      </section>
    );
  }

  return (
    <section className="panel chart-panel">
      <div className="section-heading">
        <div>
          <span className="section-kicker">Score History</span>
          <h2>Run trendline</h2>
        </div>
        <p>{data.length} completed runs currently shape this series.</p>
      </div>
      <div className="chart-wrap">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 12, right: 10, left: -16, bottom: 0 }}>
            <defs>
              <linearGradient id="historyGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#0f6d73" stopOpacity={0.42} />
                <stop offset="100%" stopColor="#0f6d73" stopOpacity={0.02} />
              </linearGradient>
            </defs>
            <CartesianGrid vertical={false} strokeDasharray="4 4" stroke="#d5e1dd" />
            <XAxis
              dataKey="run_timestamp"
              tickFormatter={formatAxisTick}
              tick={{ fontSize: 12, fill: "#5f7382" }}
              tickLine={false}
              axisLine={false}
              minTickGap={24}
            />
            <YAxis
              domain={[0, 100]}
              tick={{ fontSize: 12, fill: "#5f7382" }}
              tickLine={false}
              axisLine={false}
              width={34}
            />
            <Tooltip content={<HistoryTooltip />} />
            <Area
              type="monotone"
              dataKey="discrepancy_score"
              stroke="#0f6d73"
              fill="url(#historyGradient)"
              strokeWidth={3}
              activeDot={{ r: 5, fill: "#0f6d73", stroke: "#f6fbf9", strokeWidth: 2 }}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
}

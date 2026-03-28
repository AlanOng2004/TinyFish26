import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

export function HistoryChart({ data }) {
  return (
    <section className="panel chart-panel">
      <h2>Score History</h2>
      <div className="chart-wrap">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#d8d2c4" />
            <XAxis dataKey="run_timestamp" tick={{ fontSize: 12 }} />
            <YAxis domain={[0, 100]} tick={{ fontSize: 12 }} />
            <Tooltip />
            <Line type="monotone" dataKey="discrepancy_score" stroke="#124559" strokeWidth={3} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
}

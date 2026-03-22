import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

export default function IterationChart({ data }) {
  if (!data || data.length === 0) {
    return (
      <div style={styles.empty}>No iteration data yet. Run the agent loop to see results.</div>
    );
  }

  const chartData = data.map((entry) => ({
    iteration: entry.iteration,
    accuracy: Math.round(entry.accuracy * 1000) / 10,
  }));

  return (
    <div style={styles.chartContainer}>
      <ResponsiveContainer width="100%" height={350}>
        <LineChart data={chartData} margin={{ top: 10, right: 30, left: 10, bottom: 10 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#222" />
          <XAxis
            dataKey="iteration"
            stroke="#666"
            tick={{ fill: "#888", fontSize: 12 }}
            label={{ value: "Iteration", position: "insideBottom", offset: -5, fill: "#888" }}
          />
          <YAxis
            stroke="#666"
            tick={{ fill: "#888", fontSize: 12 }}
            domain={[0, 100]}
            label={{
              value: "Accuracy %",
              angle: -90,
              position: "insideLeft",
              offset: 10,
              fill: "#888",
            }}
          />
          <Tooltip
            contentStyle={{
              background: "#1a1a1a",
              border: "1px solid #333",
              borderRadius: 8,
              color: "#eee",
            }}
            formatter={(value) => [`${value}%`, "Accuracy"]}
          />
          <Line
            type="monotone"
            dataKey="accuracy"
            stroke="#00d4ff"
            strokeWidth={2}
            dot={{ fill: "#00d4ff", r: 3 }}
            activeDot={{ r: 6, fill: "#7c3aed" }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

const styles = {
  chartContainer: {
    background: "#111",
    border: "1px solid #222",
    borderRadius: 12,
    padding: "20px 10px",
  },
  empty: {
    textAlign: "center",
    padding: 60,
    color: "#555",
    background: "#111",
    borderRadius: 12,
    border: "1px solid #222",
  },
};

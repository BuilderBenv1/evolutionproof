export default function LogViewer({ logs }) {
  if (!logs || logs.length === 0) {
    return (
      <div style={styles.empty}>No logs yet.</div>
    );
  }

  return (
    <div style={styles.container}>
      <table style={styles.table}>
        <thead>
          <tr>
            <th style={styles.th}>Iter</th>
            <th style={styles.th}>Accuracy</th>
            <th style={styles.th}>Decision</th>
            <th style={styles.th}>Filecoin CID</th>
            <th style={styles.th}>TX Hash</th>
            <th style={styles.th}>Time</th>
          </tr>
        </thead>
        <tbody>
          {logs.map((log, i) => (
            <tr key={log.iteration ?? i} style={i % 2 === 0 ? styles.rowEven : styles.rowOdd}>
              <td style={styles.td}>{log.iteration}</td>
              <td style={styles.td}>
                <span style={styles.accuracy}>
                  {(log.accuracy * 100).toFixed(1)}%
                </span>
              </td>
              <td style={styles.td}>
                <span style={{
                  ...styles.badge,
                  background: log.decision === "prompt_updated" ? "#0d3320" : "#1a1a2e",
                  color: log.decision === "prompt_updated" ? "#4ade80" : "#888",
                }}>
                  {log.decision === "prompt_updated" ? "Updated" : "Kept"}
                </span>
              </td>
              <td style={styles.td}>
                {log.filecoin_cid ? (
                  <span style={styles.mono}>
                    {log.filecoin_cid.substring(0, 16)}...
                  </span>
                ) : (
                  <span style={styles.muted}>-</span>
                )}
              </td>
              <td style={styles.td}>
                {log.tx_hash ? (
                  <a
                    href={`https://celoscan.io/tx/${log.tx_hash}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    style={styles.link}
                  >
                    {log.tx_hash.substring(0, 10)}...
                  </a>
                ) : (
                  <span style={styles.muted}>-</span>
                )}
              </td>
              <td style={styles.td}>
                <span style={styles.muted}>
                  {log.elapsed_seconds ? `${log.elapsed_seconds}s` : "-"}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

const styles = {
  container: {
    overflowX: "auto",
    background: "#111",
    border: "1px solid #222",
    borderRadius: 12,
  },
  table: {
    width: "100%",
    borderCollapse: "collapse",
    fontSize: 13,
  },
  th: {
    textAlign: "left",
    padding: "12px 14px",
    borderBottom: "1px solid #222",
    color: "#888",
    fontWeight: 500,
    fontSize: 12,
    textTransform: "uppercase",
    letterSpacing: "0.5px",
  },
  td: {
    padding: "10px 14px",
    borderBottom: "1px solid #1a1a1a",
  },
  rowEven: {},
  rowOdd: {
    background: "#0d0d0d",
  },
  accuracy: {
    fontWeight: 600,
    color: "#00d4ff",
  },
  badge: {
    padding: "2px 8px",
    borderRadius: 10,
    fontSize: 11,
    fontWeight: 500,
  },
  mono: {
    fontFamily: "'JetBrains Mono', monospace",
    fontSize: 11,
    color: "#aaa",
  },
  link: {
    color: "#7c3aed",
    textDecoration: "none",
    fontFamily: "'JetBrains Mono', monospace",
    fontSize: 11,
  },
  muted: {
    color: "#444",
  },
  empty: {
    textAlign: "center",
    padding: 40,
    color: "#555",
    background: "#111",
    borderRadius: 12,
    border: "1px solid #222",
  },
};

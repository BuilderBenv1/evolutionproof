import { useState, useEffect } from "react";
import Head from "next/head";
import IterationChart from "../components/IterationChart";
import LogViewer from "../components/LogViewer";

const ENS_NAME = process.env.NEXT_PUBLIC_ENS_NAME || "evolutionproof.eth";

export default function Home() {
  const [agentLog, setAgentLog] = useState([]);
  const [agentState, setAgentState] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const [logRes, stateRes] = await Promise.all([
          fetch("/api/log"),
          fetch("/api/state"),
        ]);
        if (logRes.ok) setAgentLog(await logRes.json());
        if (stateRes.ok) setAgentState(await stateRes.json());
      } catch (err) {
        console.error("Failed to load data:", err);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
    const interval = setInterval(fetchData, 10000);
    return () => clearInterval(interval);
  }, []);

  const latestAccuracy = agentLog.length
    ? agentLog[agentLog.length - 1].accuracy
    : 0;
  const bestAccuracy = agentState?.best_accuracy ?? latestAccuracy;
  const totalIterations = agentState?.iteration ?? agentLog.length;

  return (
    <>
      <Head>
        <title>EvolutionProof Dashboard</title>
        <meta name="description" content="Self-improving agent trust screener with on-chain verification" />
      </Head>

      <div style={styles.container}>
        <header style={styles.header}>
          <h1 style={styles.title}>EvolutionProof</h1>
          <p style={styles.subtitle}>
            Self-Improving Agent Trust Screener
          </p>
          <span style={styles.ens}>{ENS_NAME}</span>
        </header>

        {loading ? (
          <div style={styles.loading}>Loading agent data...</div>
        ) : (
          <>
            <div style={styles.statsRow}>
              <StatCard
                label="Current Accuracy"
                value={`${(latestAccuracy * 100).toFixed(1)}%`}
              />
              <StatCard
                label="Best Accuracy"
                value={`${(bestAccuracy * 100).toFixed(1)}%`}
              />
              <StatCard
                label="Iterations"
                value={totalIterations.toString()}
              />
              <StatCard
                label="On-Chain Logs"
                value={agentLog.filter((l) => l.filecoin_cid).length.toString()}
              />
            </div>

            <section style={styles.section}>
              <h2 style={styles.sectionTitle}>Accuracy Over Iterations</h2>
              <IterationChart data={agentLog} />
            </section>

            <section style={styles.section}>
              <h2 style={styles.sectionTitle}>Recent Iteration Logs</h2>
              <LogViewer logs={agentLog.slice(-10).reverse()} />
            </section>
          </>
        )}

        <footer style={styles.footer}>
          <p>
            Powered by Anthropic API | Stored on Filecoin | Verified via ERC-8004 | Running on Celo
          </p>
        </footer>
      </div>
    </>
  );
}

function StatCard({ label, value }) {
  return (
    <div style={styles.statCard}>
      <div style={styles.statValue}>{value}</div>
      <div style={styles.statLabel}>{label}</div>
    </div>
  );
}

const styles = {
  container: {
    maxWidth: 1000,
    margin: "0 auto",
    padding: "20px",
    fontFamily: "'Inter', -apple-system, sans-serif",
    color: "#e0e0e0",
    background: "#0a0a0a",
    minHeight: "100vh",
  },
  header: {
    textAlign: "center",
    marginBottom: 40,
    paddingTop: 20,
  },
  title: {
    fontSize: 42,
    fontWeight: 700,
    margin: 0,
    background: "linear-gradient(135deg, #00d4ff, #7c3aed)",
    WebkitBackgroundClip: "text",
    WebkitTextFillColor: "transparent",
  },
  subtitle: {
    fontSize: 16,
    color: "#888",
    marginTop: 8,
  },
  ens: {
    display: "inline-block",
    marginTop: 8,
    padding: "4px 12px",
    background: "#1a1a2e",
    borderRadius: 20,
    fontSize: 13,
    color: "#00d4ff",
    border: "1px solid #00d4ff33",
  },
  statsRow: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
    gap: 16,
    marginBottom: 40,
  },
  statCard: {
    background: "#111",
    border: "1px solid #222",
    borderRadius: 12,
    padding: "20px 16px",
    textAlign: "center",
  },
  statValue: {
    fontSize: 32,
    fontWeight: 700,
    color: "#fff",
  },
  statLabel: {
    fontSize: 13,
    color: "#888",
    marginTop: 4,
  },
  section: {
    marginBottom: 40,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 600,
    marginBottom: 16,
    color: "#ccc",
  },
  loading: {
    textAlign: "center",
    padding: 60,
    color: "#666",
    fontSize: 16,
  },
  footer: {
    textAlign: "center",
    padding: "40px 0 20px",
    color: "#444",
    fontSize: 12,
  },
};

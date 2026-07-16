import { useState } from "react";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

const styles = {
  app: {
    minHeight: "100vh",
    background: "#060e1a",
    color: "#e0e6ed",
    fontFamily: "'Segoe UI', sans-serif",
    padding: "0 0 40px 0",
  },
  header: {
    background: "linear-gradient(90deg, #0d1b2a, #1a2a4a)",
    borderBottom: "1px solid #1e3a5f",
    padding: "20px 40px",
    display: "flex",
    alignItems: "center",
    gap: "14px",
  },
  accent: {
    width: "5px",
    height: "36px",
    background: "linear-gradient(180deg, #00d2ff, #3a7bd5)",
    borderRadius: "3px",
  },
  title: { margin: 0, color: "#00d2ff", fontSize: "1.6rem", fontWeight: 800 },
  subtitle: { margin: 0, color: "#7eb8d4", fontSize: "0.82rem" },
  main: { maxWidth: "1100px", margin: "0 auto", padding: "32px 20px" },
  inputSection: {
    background: "#0d1b2a",
    border: "1px solid #1e3a5f",
    borderRadius: "16px",
    padding: "28px",
    marginBottom: "28px",
  },
  inputGrid: { display: "grid", gridTemplateColumns: "1fr 2fr auto", gap: "16px", alignItems: "end" },
  label: { color: "#7eb8d4", fontSize: "0.78rem", textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: "6px", display: "block" },
  input: {
    width: "100%",
    background: "#060e1a",
    border: "1px solid #1e3a5f",
    borderRadius: "10px",
    padding: "12px 14px",
    color: "#e0e6ed",
    fontSize: "0.95rem",
    outline: "none",
    boxSizing: "border-box",
  },
  textarea: {
    width: "100%",
    background: "#060e1a",
    border: "1px solid #1e3a5f",
    borderRadius: "10px",
    padding: "12px 14px",
    color: "#e0e6ed",
    fontSize: "0.95rem",
    outline: "none",
    resize: "vertical",
    minHeight: "80px",
    boxSizing: "border-box",
  },
  btn: {
    background: "linear-gradient(90deg, #00d2ff, #3a7bd5)",
    color: "#060e1a",
    border: "none",
    borderRadius: "10px",
    padding: "12px 28px",
    fontWeight: 700,
    fontSize: "1rem",
    cursor: "pointer",
    whiteSpace: "nowrap",
  },
  tabRow: { display: "flex", gap: "8px", marginBottom: "20px" },
  tab: {
    padding: "10px 22px",
    borderRadius: "8px",
    border: "1px solid #1e3a5f",
    background: "transparent",
    color: "#7eb8d4",
    cursor: "pointer",
    fontWeight: 600,
    fontSize: "0.88rem",
  },
  activeTab: {
    padding: "10px 22px",
    borderRadius: "8px",
    border: "1px solid #00d2ff",
    background: "#0d1b2a",
    color: "#00d2ff",
    cursor: "pointer",
    fontWeight: 600,
    fontSize: "0.88rem",
  },
  card: {
    background: "#0d1b2a",
    border: "1px solid #1e3a5f",
    borderRadius: "16px",
    padding: "28px",
  },
  cardTitle: { color: "#00d2ff", fontSize: "0.88rem", textTransform: "uppercase", letterSpacing: "0.1em", margin: "0 0 20px 0" },
  bigPrice: { color: "#00d2ff", fontSize: "2.4rem", fontWeight: 800, margin: "0 0 20px 0" },
  grid2: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: "20px" },
  metaLabel: { color: "#7eb8d4", fontSize: "0.75rem", textTransform: "uppercase", letterSpacing: "0.08em", margin: "0 0 4px 0" },
  metaValue: { color: "#fff", fontSize: "1.1rem", fontWeight: 600, margin: "0 0 6px 0" },
  badge: (color) => ({
    display: "inline-block",
    padding: "4px 12px",
    borderRadius: "20px",
    fontSize: "0.78rem",
    fontWeight: 700,
    background: color + "22",
    color: color,
  }),
  divider: { borderTop: "1px solid #1e3a5f", margin: "20px 0" },
  rangeBar: { height: "6px", borderRadius: "3px", background: "linear-gradient(90deg, #ff6b6b, #51cf66)", margin: "10px 0" },
  sentBig: (color) => ({ color, fontSize: "2.8rem", fontWeight: 800, textAlign: "center", margin: "16px 0 4px" }),
  scoreBar: (pct, color) => ({
    height: "8px", borderRadius: "4px",
    background: `linear-gradient(90deg, ${color} ${pct}%, #1e3a5f ${pct}%)`,
    margin: "10px 0",
  }),
  error: {
    background: "#1a0a0a", border: "1px solid #ff6b6b", borderRadius: "12px",
    padding: "20px", color: "#ff6b6b", marginTop: "20px",
  },
  placeholder: { color: "#1e3a5f", textAlign: "center", padding: "60px 20px", fontSize: "0.95rem" },
};

export default function App() {
  const [company, setCompany] = useState("Apple");
  const [headlines, setHeadlines] = useState(
    "Apple reports record breaking revenue this quarter\nApple faces antitrust lawsuit from European regulators"
  );
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState("technical");

  const handleAnalyze = async () => {
    setLoading(true);
    setError(null);
    setReport(null);
    try {
      const res = await axios.post(`${API_URL}/analyze`, {
        company,
        headlines: headlines.split("\n").filter((l) => l.trim()),
      });
      setReport(res.data);
      setActiveTab("technical");
    } catch (err) {
      setError(err.response?.data?.detail || "Something went wrong!");
    } finally {
      setLoading(false);
    }
  };

  const getCurrencySymbol = (code) =>
    ({ USD: "$", INR: "₹", EUR: "€", GBP: "£" }[code] || code + " ");

  const renderTechnical = () => {
    const t = report.technical_analysis;
    const c = getCurrencySymbol(report.fundamental_analysis.currency);
    const rsiColor = t.rsi.signal.includes("Sell") ? "#ff6b6b" : "#51cf66";
    return (
      <div style={styles.card}>
        <p style={styles.cardTitle}>📈 Technical Analysis — {report.symbol}</p>
        <p style={{ ...styles.metaLabel }}>Current Price</p>
        <p style={styles.bigPrice}>{c}{t.current_price.toFixed(2)}</p>
        <div style={styles.divider} />
        <div style={styles.grid2}>
          <div>
            <p style={styles.metaLabel}>RSI (14)</p>
            <p style={styles.metaValue}>{t.rsi.value.toFixed(2)}</p>
            <span style={styles.badge(rsiColor)}>{t.rsi.signal}</span>
          </div>
          <div>
            <p style={styles.metaLabel}>SMA (20)</p>
            <p style={styles.metaValue}>{t.sma.value.toFixed(2)}</p>
            <span style={styles.badge("#51cf66")}>{t.sma.signal}</span>
          </div>
        </div>
        <div style={styles.divider} />
        <p style={styles.metaLabel}>MACD</p>
        <p style={styles.metaValue}>Line: {t.macd.macd_line.toFixed(2)} &nbsp;|&nbsp; Signal: {t.macd.signal_line.toFixed(2)}</p>
        <span style={styles.badge("#00d2ff")}>{t.macd.signal}</span>
      </div>
    );
  };

  const renderFundamental = () => {
    const f = report.fundamental_analysis;
    const c = getCurrencySymbol(f.currency);
    const revColor = f.revenue_growth_pct >= 0 ? "#51cf66" : "#ff6b6b";
    return (
      <div style={styles.card}>
        <p style={styles.cardTitle}>📊 Fundamental Analysis</p>
        <div style={styles.grid2}>
          <div>
            <p style={styles.metaLabel}>Market Cap</p>
            <p style={styles.metaValue}>{c}{f.market_cap.toLocaleString()}B</p>
          </div>
          <div>
            <p style={styles.metaLabel}>Revenue Growth (YoY)</p>
            <p style={{ ...styles.metaValue, color: revColor }}>
              {f.revenue_growth_pct >= 0 ? "▲" : "▼"} {Math.abs(f.revenue_growth_pct).toFixed(2)}%
            </p>
          </div>
        </div>
        <div style={styles.divider} />
        <p style={styles.metaLabel}>52-Week Range</p>
        <div style={styles.rangeBar} />
        <div style={{ display: "flex", justifyContent: "space-between" }}>
          <span style={{ color: "#ff6b6b", fontWeight: 600 }}>Low: {c}{f["52_week_low"].toFixed(2)}</span>
          <span style={{ color: "#51cf66", fontWeight: 600 }}>High: {c}{f["52_week_high"].toFixed(2)}</span>
        </div>
      </div>
    );
  };

  const renderSentiment = () => {
    const s = report.sentiment_analysis;
    const color = s.sentiment === "Positive" ? "#51cf66" : s.sentiment === "Negative" ? "#ff6b6b" : "#ffd43b";
    const icon = s.sentiment === "Positive" ? "▲" : s.sentiment === "Negative" ? "▼" : "●";
    const pct = Math.max(0, Math.min(100, Math.round((s.average_score + 1) * 50)));
    return (
      <div style={styles.card}>
        <p style={styles.cardTitle}>📰 Sentiment Analysis</p>
        <div style={{ textAlign: "center", padding: "10px 0" }}>
          <p style={styles.sentBig(color)}>{icon} {s.sentiment.toUpperCase()}</p>
          <p style={{ color: "#7eb8d4", margin: 0 }}>Based on {s.headlines_analyzed} headlines</p>
        </div>
        <div style={styles.divider} />
        <p style={styles.metaLabel}>Sentiment Score</p>
        <div style={styles.scoreBar(pct, color)} />
        <div style={{ display: "flex", justifyContent: "space-between", color: "#7eb8d4", fontSize: "0.75rem" }}>
          <span>Bearish -1.0</span>
          <span style={{ color, fontWeight: 700 }}>{s.average_score.toFixed(3)}</span>
          <span>Bullish +1.0</span>
        </div>
      </div>
    );
  };

  return (
    <div style={styles.app}>
      <div style={styles.header}>
        <div style={styles.accent} />
        <div>
          <h1 style={styles.title}>FinSight</h1>
          <p style={styles.subtitle}>Multi-Agent Financial Research Analyst</p>
        </div>
      </div>

      <div style={styles.main}>
        <div style={styles.inputSection}>
          <div style={styles.inputGrid}>
            <div>
              <label style={styles.label}>Company Name / Ticker</label>
              <input
                style={styles.input}
                value={company}
                onChange={(e) => setCompany(e.target.value)}
                placeholder="Apple, Tesla, RELIANCE.NS..."
              />
            </div>
            <div>
              <label style={styles.label}>Recent Headlines (one per line)</label>
              <textarea
                style={styles.textarea}
                value={headlines}
                onChange={(e) => setHeadlines(e.target.value)}
                placeholder="Paste news headlines here..."
              />
            </div>
            <button style={styles.btn} onClick={handleAnalyze} disabled={loading}>
              {loading ? "Analyzing..." : "Run Analysis →"}
            </button>
          </div>
        </div>

        {error && <div style={styles.error}><b>Error:</b> {error}</div>}

        {report && (
          <>
            <div style={styles.tabRow}>
              {["technical", "fundamental", "sentiment"].map((tab) => (
                <button
                  key={tab}
                  style={activeTab === tab ? styles.activeTab : styles.tab}
                  onClick={() => setActiveTab(tab)}
                >
                  {tab === "technical" ? "📈 Technical" : tab === "fundamental" ? "📊 Fundamental" : "📰 Sentiment"}
                </button>
              ))}
            </div>
            {activeTab === "technical" && renderTechnical()}
            {activeTab === "fundamental" && renderFundamental()}
            {activeTab === "sentiment" && renderSentiment()}
          </>
        )}

        {!report && !loading && !error && (
          <div style={styles.placeholder}>Enter a company name and click Run Analysis to get started</div>
        )}
      </div>
    </div>
  );
}
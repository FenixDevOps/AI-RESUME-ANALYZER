import React, { useEffect, useState } from "react";

// ── Animated Progress Bar ───────────────────────────────────────────────────
const MatchProgressBar = ({ percent }) => {
  const [width, setWidth] = useState(0);
  useEffect(() => {
    const t = setTimeout(() => setWidth(percent), 100);
    return () => clearTimeout(t);
  }, [percent]);

  const color =
    percent >= 75 ? "linear-gradient(90deg,#4ade80,#22d3ee)"
    : percent >= 50 ? "linear-gradient(90deg,#fbbf24,#f97316)"
    : "linear-gradient(90deg,#f87171,#fb923c)";

  return (
    <div className="match-progress-wrap">
      <div className="match-progress-track">
        <div
          className="match-progress-fill"
          style={{
            width: `${width}%`,
            background: color,
            transition: "width 1.3s cubic-bezier(0.4,0,0.2,1)",
          }}
        />
      </div>
      <span className="match-progress-label">{percent}% match</span>
    </div>
  );
};

// ── Keyword Chip ────────────────────────────────────────────────────────────
const Chip = ({ label, type }) => (
  <span className={`keyword-chip chip-${type}`}>{label}</span>
);

// ── Stat Badge ──────────────────────────────────────────────────────────────
const StatBadge = ({ value, label, color }) => (
  <div className="stat-badge" style={{ borderColor: color }}>
    <div className="stat-badge-value" style={{ color }}>{value}</div>
    <div className="stat-badge-label">{label}</div>
  </div>
);

// ── Main JDMatch Component ──────────────────────────────────────────────────
const JDMatch = ({ jdMatch }) => {
  if (!jdMatch) return null;

  const { match_percent = 0, matched_keywords = [], missing_keywords = [], total_jd_keywords = 0 } = jdMatch;

  const matchColor =
    match_percent >= 75 ? "#4ade80"
    : match_percent >= 50 ? "#fbbf24"
    : "#f87171";

  return (
    <div className="jd-match-section">
      {/* Header */}
      <div className="jd-match-header">
        <h3 className="jd-match-title">
          <span className="jd-match-icon">🎯</span> JD Match Analysis
        </h3>
        <div
          className="match-percent-badge"
          style={{
            background: `conic-gradient(${matchColor} ${match_percent * 3.6}deg, rgba(255,255,255,0.07) 0deg)`,
          }}
        >
          <div className="match-percent-inner">
            <span className="match-percent-value" style={{ color: matchColor }}>{match_percent}%</span>
            <span className="match-percent-sub">Match</span>
          </div>
        </div>
      </div>

      {/* Progress Bar */}
      <MatchProgressBar percent={match_percent} />

      {/* Stats Row */}
      <div className="jd-stats-row">
        <StatBadge value={total_jd_keywords} label="JD Keywords"    color="#818cf8" />
        <StatBadge value={matched_keywords.length} label="Matched"  color="#4ade80" />
        <StatBadge value={missing_keywords.length} label="Missing"  color="#f87171" />
      </div>

      {/* Keywords Side-by-Side */}
      <div className="keywords-grid">
        {matched_keywords.length > 0 && (
          <div className="keywords-panel">
            <h4 className="keywords-panel-title matched-title">✅ Matched Keywords</h4>
            <div className="chips-wrap">
              {matched_keywords.map((kw, i) => (
                <Chip key={i} label={kw} type="matched" />
              ))}
            </div>
          </div>
        )}
        {missing_keywords.length > 0 && (
          <div className="keywords-panel">
            <h4 className="keywords-panel-title missing-title">❌ Missing Keywords</h4>
            <div className="chips-wrap">
              {missing_keywords.map((kw, i) => (
                <Chip key={i} label={kw} type="missing" />
              ))}
            </div>
          </div>
        )}
      </div>

      {matched_keywords.length === 0 && missing_keywords.length === 0 && (
        <p className="no-keywords-msg">No keywords extracted. Try a more detailed job description.</p>
      )}
    </div>
  );
};

export default JDMatch;

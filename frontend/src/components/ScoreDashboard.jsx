import React, { useEffect, useState } from "react";

// ── Circular SVG Gauge ──────────────────────────────────────────────────────
const CircularGauge = ({ score, maxScore = 100, label, size = 160 }) => {
  const [animated, setAnimated] = useState(0);
  const pct = Math.min(Math.max(score || 0, 0), maxScore) / maxScore;
  const radius = (size - 24) / 2;
  const circumference = 2 * Math.PI * radius;
  const strokeDash = circumference * pct;

  const color =
    pct >= 0.8 ? "#4ade80"
    : pct >= 0.6 ? "#fbbf24"
    : "#f87171";
  const status =
    pct >= 0.8 ? "Excellent" : pct >= 0.6 ? "Good" : "Needs Work";
  const glowColor =
    pct >= 0.8 ? "rgba(74,222,128,0.35)"
    : pct >= 0.6 ? "rgba(251,191,36,0.35)"
    : "rgba(248,113,113,0.35)";

  useEffect(() => {
    const timer = setTimeout(() => setAnimated(strokeDash), 80);
    return () => clearTimeout(timer);
  }, [strokeDash]);

  const cx = size / 2;
  const cy = size / 2;

  return (
    <div className="gauge-wrapper">
      <svg
        width={size}
        height={size}
        className="gauge-svg"
        style={{ filter: `drop-shadow(0 0 14px ${glowColor})` }}
      >
        <circle
          cx={cx} cy={cy} r={radius}
          fill="none"
          stroke="rgba(255,255,255,0.07)"
          strokeWidth={14}
        />
        <circle
          cx={cx} cy={cy} r={radius}
          fill="none"
          stroke={color}
          strokeWidth={14}
          strokeLinecap="round"
          strokeDasharray={`${animated} ${circumference}`}
          strokeDashoffset={0}
          transform={`rotate(-90 ${cx} ${cy})`}
          style={{ transition: "stroke-dasharray 1.2s cubic-bezier(0.4,0,0.2,1)" }}
        />
        <text x={cx} y={cy - 8} textAnchor="middle" fill="#fff" fontSize="28" fontWeight="700" fontFamily="Inter,sans-serif">
          {score != null ? score : "--"}
        </text>
        <text x={cx} y={cy + 14} textAnchor="middle" fill="rgba(255,255,255,0.4)" fontSize="11" fontFamily="Inter,sans-serif">
          / {maxScore}
        </text>
      </svg>
      <div className="gauge-label">{label}</div>
      <div className="gauge-status" style={{ color }}>{status}</div>
    </div>
  );
};

// ── Animated Metric Bar ─────────────────────────────────────────────────────
const MetricBar = ({ label, value, color }) => {
  const [width, setWidth] = useState(0);
  useEffect(() => {
    const t = setTimeout(() => setWidth(value), 150);
    return () => clearTimeout(t);
  }, [value]);
  return (
    <div className="metric-bar-row">
      <div className="metric-bar-label">{label}</div>
      <div className="metric-bar-track">
        <div
          className="metric-bar-fill"
          style={{
            width: `${width}%`,
            background: color,
            transition: "width 1.1s cubic-bezier(0.4,0,0.2,1)",
          }}
        />
      </div>
      <span className="metric-bar-value">{value}%</span>
    </div>
  );
};

// ── Main ScoreDashboard ─────────────────────────────────────────────────────
const ScoreDashboard = ({ resumeScore, atsScore, strengths = [], weaknesses = [] }) => {
  const readability = Math.round(((resumeScore ?? 0) + (atsScore ?? 0)) / 2);

  return (
    <div className="score-dashboard">
      {/* Gauges */}
      <div className="gauges-section">
        <div className="gauges-row">
          <CircularGauge score={resumeScore} label="Resume Score" size={160} />
          <CircularGauge score={atsScore}    label="ATS Score"    size={160} />
        </div>
      </div>

      {/* Metric Bars */}
      <div className="dashboard-card metrics-card">
        <h4 className="card-section-title">📊 Score Breakdown</h4>
        <MetricBar label="Overall Quality"  value={resumeScore ?? 0} color="linear-gradient(90deg,#4ade80,#22d3ee)" />
        <MetricBar label="ATS Optimization" value={atsScore ?? 0}   color="linear-gradient(90deg,#a78bfa,#818cf8)" />
        <MetricBar label="Readability"      value={readability}      color="linear-gradient(90deg,#fbbf24,#fb923c)" />
      </div>

      {/* Strengths & Weaknesses */}
      {(strengths.length > 0 || weaknesses.length > 0) && (
        <div className="sw-grid">
          {strengths.length > 0 && (
            <div className="dashboard-card sw-card strength-card">
              <h4 className="card-section-title strength-title">✅ Strengths</h4>
              <ul className="sw-list">
                {strengths.map((s, i) => (
                  <li key={i} className="sw-item strength-item">{s}</li>
                ))}
              </ul>
            </div>
          )}
          {weaknesses.length > 0 && (
            <div className="dashboard-card sw-card weakness-card">
              <h4 className="card-section-title weakness-title">⚠️ Areas to Improve</h4>
              <ul className="sw-list">
                {weaknesses.map((w, i) => (
                  <li key={i} className="sw-item weakness-item">{w}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ScoreDashboard;

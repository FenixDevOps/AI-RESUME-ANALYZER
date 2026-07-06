import React, { useEffect, useState } from 'react';
import {
  BarChart, Bar, LineChart, Line, AreaChart, Area,
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell
} from 'recharts';

const API = '/api/dashboard';

// ── Palette ───────────────────────────────────────────────────────────
const COLORS = ['#4FD1C5', '#63b3ed', '#b794f4', '#68d391', '#f6ad55'];

// ── Helpers ───────────────────────────────────────────────────────────
const weeklyData = [
  { day: 'Mon', submissions: 2 },
  { day: 'Tue', submissions: 5 },
  { day: 'Wed', submissions: 3 },
  { day: 'Thu', submissions: 8 },
  { day: 'Fri', submissions: 6 },
  { day: 'Sat', submissions: 1 },
  { day: 'Sun', submissions: 4 },
];

const skillData = [
  { skill: 'Programming', count: 38 },
  { skill: 'Database',    count: 22 },
  { skill: 'Cloud',       count: 18 },
  { skill: 'Management',  count: 12 },
  { skill: 'Other',       count: 8  },
];

const categoryData = [
  { category: 'Engineering', rate: 72 },
  { category: 'Data',        rate: 65 },
  { category: 'Design',      rate: 58 },
  { category: 'Management',  rate: 48 },
  { category: 'Sales',       rate: 41 },
];

// ── Stat Card ─────────────────────────────────────────────────────────
function StatCard({ icon, value, label, color, delay = 0 }) {
  return (
    <div className="db-stat-card" style={{ '--accent': color, animationDelay: `${delay}s` }}>
      <div className="db-stat-top">
        <span className="db-stat-icon">{icon}</span>
        <span className="db-stat-bar" style={{ background: color }} />
      </div>
      <p className="db-stat-value" style={{ color }}>{value}</p>
      <p className="db-stat-label">{label}</p>
    </div>
  );
}

// ── Custom Tooltip ────────────────────────────────────────────────────
function CustomTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  return (
    <div style={{
      background: 'rgba(15,25,50,0.95)',
      border: '1px solid rgba(79,209,197,0.3)',
      borderRadius: 10, padding: '8px 14px',
      fontSize: 13, color: '#fff'
    }}>
      <p style={{ margin: 0, color: '#4FD1C5', fontWeight: 700, marginBottom: 4 }}>{label}</p>
      {payload.map((p, i) => (
        <p key={i} style={{ margin: 0, color: p.color || '#fff' }}>
          {p.name}: <strong>{p.value}</strong>
        </p>
      ))}
    </div>
  );
}

// ── ATS Gauge ─────────────────────────────────────────────────────────
function ATSGauge({ value }) {
  const pct = Math.min(Math.max(value, 0), 100);
  const deg = (pct / 100) * 180;
  const color = pct >= 70 ? '#68d391' : pct >= 40 ? '#f6ad55' : '#fc8181';

  return (
    <div style={{ textAlign: 'center' }}>
      <div style={{ position: 'relative', width: 200, height: 110, margin: '0 auto 12px' }}>
        {/* Track */}
        <svg width="200" height="110" viewBox="0 0 200 110" style={{ position: 'absolute', top: 0, left: 0 }}>
          <path
            d="M 10 100 A 90 90 0 0 1 190 100"
            fill="none" stroke="rgba(255,255,255,0.08)" strokeWidth="18" strokeLinecap="round"
          />
          {/* Colored arc */}
          <path
            d="M 10 100 A 90 90 0 0 1 190 100"
            fill="none"
            stroke={color}
            strokeWidth="18"
            strokeLinecap="round"
            strokeDasharray={`${(pct / 100) * 282.6} 282.6`}
            style={{ transition: 'stroke-dasharray 1s ease, stroke 0.5s ease' }}
          />
          {/* Threshold marker at 70% */}
          <line
            x1="100" y1="14" x2="100" y2="28"
            stroke="#f6e05e" strokeWidth="3"
            transform={`rotate(${(70/100)*180 - 90} 100 100)`}
          />
        </svg>
        {/* Center label */}
        <div style={{
          position: 'absolute', bottom: 0, left: '50%',
          transform: 'translateX(-50%)',
          textAlign: 'center', lineHeight: 1
        }}>
          <div style={{ fontSize: 36, fontWeight: 800, color }}>{value}%</div>
          <div style={{ fontSize: 11, color: 'rgba(255,255,255,0.45)', marginTop: 2 }}>AVG ATS</div>
        </div>
      </div>
      <div style={{ display: 'flex', justifyContent: 'center', gap: 16, fontSize: 12 }}>
        {[['#fc8181','<40 Poor'],['#f6ad55','40-70 OK'],['#68d391','>70 Great']].map(([c,t]) => (
          <span key={t} style={{ display: 'flex', alignItems: 'center', gap: 5, color: 'rgba(255,255,255,0.5)' }}>
            <span style={{ width: 8, height: 8, borderRadius: '50%', background: c, display: 'inline-block' }} />
            {t}
          </span>
        ))}
      </div>
    </div>
  );
}

// ── Tip Card ──────────────────────────────────────────────────────────
function TipCard({ tip, idx }) {
  return (
    <div className="db-tip-card" style={{ animationDelay: `${idx * 0.08}s` }}>
      <div className="db-tip-icon">{tip.icon}</div>
      <div>
        <p className="db-tip-title">{tip.title}</p>
        <p className="db-tip-body">{tip.body}</p>
      </div>
    </div>
  );
}

// ── Main Component ────────────────────────────────────────────────────
export default function Dashboard() {
  const [stats, setStats]   = useState(null);
  const [tips, setTips]     = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetch(`${API}/stats`).then(r => r.json()),
      fetch(`${API}/tips`).then(r => r.json()),
    ]).then(([s, t]) => {
      setStats(s);
      setTips(t.tips || []);
    }).catch(() => {
      // fallback mock
      setStats({ total_analyses:12, average_score:74, ats_pass_rate:68,
        top_role:'Software Engineer', analyses_this_week:3,
        improvement_trend:'+8pts', skills_identified:47, jobs_saved:5 });
      setTips([]);
    }).finally(() => setLoading(false));
  }, []);

  if (loading) return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: 300 }}>
      <div className="btn-spinner" style={{ width: 36, height: 36, borderWidth: 3 }} />
    </div>
  );

  const statCards = [
    { icon: '📄', value: stats.total_analyses,       label: 'Total Analyses',    color: '#4FD1C5' },
    { icon: '🎯', value: `${stats.average_score}%`,  label: 'Avg ATS Score',     color: '#63b3ed' },
    { icon: '🏆', value: `${stats.ats_pass_rate}%`,  label: 'ATS Pass Rate',     color: '#b794f4' },
    { icon: '✅', value: stats.analyses_this_week,   label: 'This Week',         color: '#68d391' },
  ];

  return (
    <>
      <style>{`
        @keyframes dbFadeUp {
          from { opacity:0; transform:translateY(20px); }
          to   { opacity:1; transform:translateY(0); }
        }

        /* Hero */
        .db-hero {
          background: linear-gradient(135deg,#0d1b2a 0%,#1b263b 45%,#0f3460 100%);
          border-radius: 20px;
          padding: 2.2rem 2.6rem;
          margin-bottom: 2rem;
          position: relative;
          overflow: hidden;
          border: 1px solid rgba(79,209,197,0.18);
          box-shadow: 0 20px 60px rgba(0,0,0,0.4);
          animation: dbFadeUp .5s ease-out;
        }
        .db-hero::before {
          content:'';
          position:absolute; top:-50%; left:-50%;
          width:200%; height:200%;
          background: radial-gradient(ellipse at 75% 30%, rgba(79,209,197,0.09) 0%, transparent 65%);
          pointer-events:none;
        }
        .db-hero h1 {
          font-size: 2.2rem; font-weight:800; margin:0 0 .35rem;
          background: linear-gradient(135deg,#4FD1C5,#63b3ed);
          -webkit-background-clip:text; -webkit-text-fill-color:transparent;
          background-clip:text;
        }
        .db-hero p { color:rgba(255,255,255,0.5); margin:0; font-size:.95rem; }
        .db-hero-row { display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem; }
        .db-timestamp {
          background:rgba(79,209,197,0.1); border:1px solid rgba(79,209,197,0.28);
          border-radius:40px; padding:.4rem 1rem;
          font-size:.78rem; color:#4FD1C5; white-space:nowrap;
        }

        /* Stat Cards */
        .db-stats-grid {
          display:grid; grid-template-columns:repeat(4,1fr); gap:1.1rem; margin-bottom:1.8rem;
        }
        @media(max-width:800px){ .db-stats-grid{ grid-template-columns:repeat(2,1fr); } }
        .db-stat-card {
          background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.07);
          border-radius:18px; padding:1.4rem 1.3rem;
          transition:transform .25s,box-shadow .25s,background .25s;
          animation:dbFadeUp .5s ease-out both;
          position:relative; overflow:hidden;
        }
        .db-stat-card::before {
          content:''; position:absolute; top:0; left:0; right:0; height:3px;
          background: var(--accent); border-radius:18px 18px 0 0;
        }
        .db-stat-card:hover { transform:translateY(-5px); background:rgba(255,255,255,0.07); box-shadow:0 14px 36px rgba(0,0,0,0.3); }
        .db-stat-top { display:flex; justify-content:space-between; align-items:center; margin-bottom:.6rem; }
        .db-stat-icon { font-size:1.5rem; }
        .db-stat-bar { width:28px; height:3px; border-radius:3px; }
        .db-stat-value { font-size:2.4rem; font-weight:800; margin:0; line-height:1; }
        .db-stat-label { font-size:.78rem; color:rgba(255,255,255,0.5); margin:.4rem 0 0; text-transform:uppercase; letter-spacing:.5px; font-weight:600; }

        /* Section title */
        .db-section-title {
          font-size:1.1rem; font-weight:700; color:#4FD1C5;
          margin:2rem 0 1rem; padding-bottom:.5rem;
          border-bottom:2px solid rgba(79,209,197,0.18);
          display:flex; align-items:center; gap:.45rem;
        }

        /* Chart containers */
        .db-charts-row { display:grid; grid-template-columns:repeat(2,1fr); gap:1.2rem; margin-bottom:1.2rem; }
        @media(max-width:700px){ .db-charts-row{ grid-template-columns:1fr; } }
        .db-chart-card {
          background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07);
          border-radius:18px; padding:1.4rem;
          transition:box-shadow .3s;
        }
        .db-chart-card:hover { box-shadow:0 8px 30px rgba(0,0,0,0.25); }
        .db-chart-label { font-size:.85rem; font-weight:700; color:rgba(255,255,255,0.65); margin:0 0 1rem; text-transform:uppercase; letter-spacing:.5px; }

        /* Tips */
        .db-tips-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); gap:1rem; }
        .db-tip-card {
          background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.07);
          border-radius:14px; padding:1.1rem 1.2rem;
          display:flex; gap:.9rem;
          animation:dbFadeUp .5s ease-out both;
          transition:transform .22s,background .22s;
        }
        .db-tip-card:hover { transform:translateY(-3px); background:rgba(255,255,255,0.07); }
        .db-tip-icon { font-size:1.6rem; flex-shrink:0; margin-top:.1rem; }
        .db-tip-title { font-size:.9rem; font-weight:700; color:#fff; margin:0 0 .3rem; }
        .db-tip-body  { font-size:.8rem; color:rgba(255,255,255,0.5); margin:0; line-height:1.5; }

        /* Extra stats row */
        .db-extra-row { display:flex; gap:1rem; flex-wrap:wrap; margin-bottom:2rem; }
        .db-extra-pill {
          flex:1; min-width:140px;
          background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.07);
          border-radius:14px; padding:1rem 1.2rem; text-align:center;
          transition:transform .22s;
        }
        .db-extra-pill:hover { transform:translateY(-3px); }
        .db-extra-pill-val { font-size:1.6rem; font-weight:800; }
        .db-extra-pill-lbl { font-size:.72rem; color:rgba(255,255,255,0.45); text-transform:uppercase; letter-spacing:.5px; font-weight:600; margin-top:.2rem; }
      `}</style>

      {/* Hero */}
      <div className="db-hero">
        <div className="db-hero-row">
          <div>
            <h1>📊 Analytics Dashboard</h1>
            <p>Track your resume performance, skill trends &amp; career progress</p>
          </div>
          <div className="db-timestamp">
            🕐 {new Date().toLocaleDateString('en-IN', { day:'numeric', month:'long', year:'numeric' })}
          </div>
        </div>
      </div>

      {/* Stat Cards */}
      <div className="db-stats-grid">
        {statCards.map((c, i) => (
          <StatCard key={c.label} {...c} delay={i * 0.08} />
        ))}
      </div>

      {/* Extra pills */}
      <div className="db-extra-row">
        {[
          { val: stats.improvement_trend, lbl: 'Improvement Trend', color: '#68d391' },
          { val: stats.skills_identified, lbl: 'Skills Identified',  color: '#4FD1C5' },
          { val: stats.jobs_saved,        lbl: 'Jobs Saved',         color: '#b794f4' },
          { val: stats.top_role,          lbl: 'Top Target Role',    color: '#f6ad55' },
        ].map(p => (
          <div key={p.lbl} className="db-extra-pill">
            <div className="db-extra-pill-val" style={{ color: p.color }}>{p.val}</div>
            <div className="db-extra-pill-lbl">{p.lbl}</div>
          </div>
        ))}
      </div>

      {/* Charts row 1 */}
      <div className="db-section-title">📈 Performance Analytics</div>
      <div className="db-charts-row">

        {/* ATS Gauge */}
        <div className="db-chart-card">
          <p className="db-chart-label">🎯 ATS Score Gauge</p>
          <ATSGauge value={stats.average_score} />
        </div>

        {/* Skill Distribution */}
        <div className="db-chart-card">
          <p className="db-chart-label">🛠 Skill Distribution</p>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={skillData} layout="vertical" margin={{ top:0, right:40, left:10, bottom:0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" horizontal={false} />
              <XAxis type="number" tick={{ fill:'rgba(255,255,255,0.45)', fontSize:11 }} axisLine={false} tickLine={false} />
              <YAxis type="category" dataKey="skill" tick={{ fill:'rgba(255,255,255,0.65)', fontSize:12 }} axisLine={false} tickLine={false} width={85} />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="count" radius={[0,6,6,0]} label={{ position:'right', fill:'rgba(255,255,255,0.55)', fontSize:11 }}>
                {skillData.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Charts row 2 */}
      <div className="db-charts-row">

        {/* Weekly Trend */}
        <div className="db-chart-card">
          <p className="db-chart-label">📅 Weekly Submission Trend</p>
          <ResponsiveContainer width="100%" height={210}>
            <AreaChart data={weeklyData} margin={{ top:10, right:10, left:-20, bottom:0 }}>
              <defs>
                <linearGradient id="areaGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%"  stopColor="#4FD1C5" stopOpacity={0.2} />
                  <stop offset="95%" stopColor="#4FD1C5" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
              <XAxis dataKey="day" tick={{ fill:'rgba(255,255,255,0.45)', fontSize:11 }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fill:'rgba(255,255,255,0.45)', fontSize:11 }} axisLine={false} tickLine={false} />
              <Tooltip content={<CustomTooltip />} />
              <Area type="monotone" dataKey="submissions" name="Submissions"
                stroke="#4FD1C5" strokeWidth={2.5}
                fill="url(#areaGrad)" dot={{ fill:'#4FD1C5', r:4, strokeWidth:2, stroke:'rgba(13,27,42,0.8)' }}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Success by Category */}
        <div className="db-chart-card">
          <p className="db-chart-label">📊 Success Rate by Category</p>
          <ResponsiveContainer width="100%" height={210}>
            <BarChart data={categoryData} margin={{ top:10, right:10, left:-20, bottom:0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" vertical={false} />
              <XAxis dataKey="category" tick={{ fill:'rgba(255,255,255,0.45)', fontSize:11 }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fill:'rgba(255,255,255,0.45)', fontSize:11 }} axisLine={false} tickLine={false} />
              <Tooltip content={<CustomTooltip />} formatter={(v) => [`${v}%`, 'Success Rate']} />
              <Bar dataKey="rate" radius={[6,6,0,0]} label={{ position:'top', fill:'rgba(255,255,255,0.5)', fontSize:11, formatter: v => `${v}%` }}>
                {categoryData.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Career Tips */}
      {tips.length > 0 && (
        <>
          <div className="db-section-title">💡 Career Tips</div>
          <div className="db-tips-grid">
            {tips.map((tip, i) => <TipCard key={i} tip={tip} idx={i} />)}
          </div>
        </>
      )}
    </>
  );
}

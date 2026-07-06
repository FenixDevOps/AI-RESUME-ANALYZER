import React, { useState } from 'react';

// ── Static data (would come from API) ─────────────────────────────────
const TRENDING_SKILLS = [
  { name: 'Python',          growth: 45, emoji: '🐍' },
  { name: 'React / Next.js', growth: 62, emoji: '⚛️' },
  { name: 'AWS / Cloud',     growth: 58, emoji: '☁️' },
  { name: 'Machine Learning',growth: 71, emoji: '🤖' },
  { name: 'TypeScript',      growth: 54, emoji: '📘' },
  { name: 'DevOps / CI-CD',  growth: 49, emoji: '🔧' },
];

const TOP_LOCATIONS = [
  { name: 'Bengaluru',   jobs: '1,40,000+', emoji: '🏙️' },
  { name: 'Hyderabad',   jobs: '95,000+',   emoji: '🌆' },
  { name: 'Pune',        jobs: '72,000+',   emoji: '🏛️' },
  { name: 'Mumbai',      jobs: '65,000+',   emoji: '🌊' },
  { name: 'Delhi NCR',   jobs: '88,000+',   emoji: '🗺️' },
  { name: 'Remote',      jobs: '50,000+',   emoji: '🌐' },
];

const SALARY_INSIGHTS = [
  { role: 'Software Engineer',  range: '6–24 LPA',  exp: '0–5 yrs',  fill: 55 },
  { role: 'Data Scientist',     range: '8–28 LPA',  exp: '1–6 yrs',  fill: 62 },
  { role: 'Product Manager',    range: '12–40 LPA', exp: '3–8 yrs',  fill: 70 },
  { role: 'DevOps Engineer',    range: '8–25 LPA',  exp: '1–5 yrs',  fill: 58 },
  { role: 'UI/UX Designer',     range: '5–18 LPA',  exp: '0–4 yrs',  fill: 48 },
];

const FEATURED_COMPANIES = [
  { name:'Google',       desc:'Search, Cloud & AI innovation',       cats:['AI','Cloud','Search'],       url:'https://careers.google.com',       emoji:'🟦', banner:'linear-gradient(90deg,#4FD1C5,#63b3ed)' },
  { name:'Microsoft',    desc:'Enterprise software & Azure cloud',   cats:['Cloud','Enterprise','AI'],   url:'https://careers.microsoft.com',    emoji:'🪟', banner:'linear-gradient(90deg,#63b3ed,#4299e1)' },
  { name:'Amazon',       desc:'E-commerce, AWS & logistics',         cats:['Cloud','E-comm','Logistics'],url:'https://amazon.jobs',              emoji:'📦', banner:'linear-gradient(90deg,#f6ad55,#ed8936)' },
  { name:'Infosys',      desc:'IT services & consulting giant',      cats:['IT','Consulting','BPO'],     url:'https://www.infosys.com/careers/', emoji:'🔷', banner:'linear-gradient(90deg,#4FD1C5,#38b2ac)' },
  { name:'TCS',          desc:'India\'s largest IT services firm',   cats:['IT','Services','Global'],    url:'https://ibegin.tcs.com',           emoji:'🏢', banner:'linear-gradient(90deg,#b794f4,#9f7aea)' },
  { name:'Wipro',        desc:'Digital transformation & consulting', cats:['Digital','IT','Cloud'],      url:'https://careers.wipro.com',        emoji:'🌐', banner:'linear-gradient(90deg,#68d391,#48bb78)' },
];

const PORTALS = [
  { name:'LinkedIn',  color:'#0A66C2', emoji:'💼', url: q => `https://www.linkedin.com/jobs/search/?keywords=${encodeURIComponent(q)}`,  desc:'World\'s largest professional network' },
  { name:'Indeed',    color:'#003A9B', emoji:'🔍', url: q => `https://in.indeed.com/jobs?q=${encodeURIComponent(q)}`,                    desc:'Millions of listings worldwide' },
  { name:'Naukri',    color:'#4FD1C5', emoji:'📋', url: q => `https://www.naukri.com/${encodeURIComponent(q.replace(/ /g,'-'))}-jobs`,   desc:'India\'s #1 job portal' },
  { name:'Foundit',   color:'#b794f4', emoji:'🚀', url: q => `https://www.foundit.in/srp/results?query=${encodeURIComponent(q)}`,        desc:'Fast-growing tech job board' },
  { name:'Glassdoor', color:'#0CAA41', emoji:'🌟', url: q => `https://www.glassdoor.co.in/Job/jobs.htm?sc.keyword=${encodeURIComponent(q)}`, desc:'Jobs with salary & culture insights' },
];

const EXP_LEVELS  = ['Any','Fresher','0-1 yrs','1-3 yrs','3-5 yrs','5-7 yrs','7+ yrs'];
const JOB_TYPES   = ['Any','Full Time','Part Time','Contract','Remote','Internship'];
const SALARY_OPTS = ['Any','0-3 LPA','3-6 LPA','6-10 LPA','10-15 LPA','15+ LPA'];
const ACCENT      = ['#4FD1C5','#63b3ed','#b794f4','#68d391','#f6ad55'];

// ── Skill row ─────────────────────────────────────────────────────────
function SkillRow({ s, i }) {
  return (
    <div className="js-skill-row">
      <span className="js-skill-emoji">{s.emoji}</span>
      <div className="js-skill-info">
        <p className="js-skill-name">{s.name}</p>
        <div className="js-skill-track">
          <div className="js-skill-fill" style={{ width:`${s.growth}%` }} />
        </div>
      </div>
      <span className="js-skill-growth">↑ {s.growth}%</span>
    </div>
  );
}

// ── Location row ──────────────────────────────────────────────────────
function LocationRow({ l }) {
  return (
    <div className="js-loc-row">
      <div style={{ display:'flex', alignItems:'center', gap:10 }}>
        <span style={{ fontSize:'1.4rem' }}>{l.emoji}</span>
        <p style={{ margin:0, fontWeight:600, color:'#fff', fontSize:'.92rem' }}>{l.name}</p>
      </div>
      <span className="js-loc-badge">{l.jobs}</span>
    </div>
  );
}

// ── Salary row ────────────────────────────────────────────────────────
function SalaryRow({ s, i }) {
  return (
    <div className="js-salary-card" style={{ borderLeftColor: ACCENT[i % ACCENT.length] }}>
      <div className="js-salary-top">
        <div>
          <p className="js-salary-role">{s.role}</p>
          <span className="js-salary-exp">⏱ {s.exp}</span>
        </div>
        <span className="js-salary-amt" style={{ color: ACCENT[i % ACCENT.length] }}>₹ {s.range}</span>
      </div>
      <div className="js-salary-bar-row">
        <span className="js-salary-min">Entry</span>
        <div className="js-salary-track"><div className="js-salary-fill" style={{ width:`${s.fill}%` }} /></div>
        <span className="js-salary-max">Senior</span>
      </div>
    </div>
  );
}

// ── Company card ──────────────────────────────────────────────────────
function CompanyCard({ c }) {
  return (
    <a href={c.url} target="_blank" rel="noreferrer" className="js-company-card" style={{ textDecoration:'none', color:'inherit' }}>
      <div className="js-company-banner" style={{ background: c.banner }} />
      <div className="js-company-body">
        <div className="js-company-header">
          <span className="js-company-emoji">{c.emoji}</span>
          <p className="js-company-name">{c.name}</p>
        </div>
        <p className="js-company-desc">{c.desc}</p>
        <div className="js-company-tags">
          {c.cats.map(t => <span key={t} className="js-company-tag">{t}</span>)}
        </div>
        <span className="js-company-cta">View Careers →</span>
      </div>
    </a>
  );
}

// ── Portal result card ────────────────────────────────────────────────
function PortalResultCard({ p, query }) {
  return (
    <a href={p.url(query)} target="_blank" rel="noreferrer" className="js-result-card" style={{ textDecoration:'none', color:'inherit' }}>
      <div className="js-result-dot" style={{ background: p.color }} />
      <div style={{ flex:1 }}>
        <p className="js-result-portal" style={{ color: p.color }}>{p.emoji} {p.name}</p>
        <p className="js-result-desc">{p.desc}</p>
      </div>
      <div className="js-result-cta" style={{ background: p.color }}>Search →</div>
    </a>
  );
}

// ── Main Component ────────────────────────────────────────────────────
export default function Jobs() {
  const [query,    setQuery]    = useState('');
  const [location, setLocation] = useState('');
  const [exp,      setExp]      = useState('Any');
  const [jobType,  setJobType]  = useState('Any');
  const [salary,   setSalary]   = useState('Any');
  const [searched, setSearched] = useState(false);
  const [insightTab, setInsightTab] = useState(0);

  const handleSearch = (e) => {
    e.preventDefault();
    if (query.trim()) setSearched(true);
  };

  return (
    <>
      <style>{`
        @keyframes jsFadeUp {
          from { opacity:0; transform:translateY(18px); }
          to   { opacity:1; transform:translateY(0); }
        }

        /* Hero */
        .js-hero {
          background: linear-gradient(135deg,#0d1b2a 0%,#0f3460 60%,#16213e 100%);
          border-radius:20px; padding:2.2rem 2.6rem; margin-bottom:1.8rem;
          position:relative; overflow:hidden;
          border:1px solid rgba(79,209,197,0.16);
          box-shadow:0 20px 60px rgba(0,0,0,0.4);
          animation:jsFadeUp .5s ease-out;
        }
        .js-hero::before {
          content:''; position:absolute; top:-60%; right:-10%;
          width:55%; height:240%;
          background:radial-gradient(ellipse,rgba(79,209,197,0.1) 0%,transparent 65%);
          pointer-events:none;
        }
        .js-hero h1 {
          font-size:2.1rem; font-weight:800; margin:0 0 .35rem;
          background:linear-gradient(135deg,#4FD1C5,#63b3ed);
          -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
        }
        .js-hero p { color:rgba(255,255,255,0.5); margin:0; font-size:.92rem; }
        .js-hero-badges { display:flex; gap:.6rem; flex-wrap:wrap; margin-top:.9rem; }
        .js-badge {
          background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.12);
          border-radius:20px; padding:.28rem .75rem; font-size:.75rem; color:rgba(255,255,255,0.6);
        }

        /* Insight tabs */
        .js-insight-tabs { display:flex; gap:.5rem; margin-bottom:1rem; }
        .js-insight-tab {
          padding:.45rem 1.1rem; border-radius:10px; font-size:.82rem; font-weight:600;
          border:1px solid rgba(255,255,255,0.1); background:transparent; color:rgba(255,255,255,0.5);
          cursor:pointer; transition:all .2s;
        }
        .js-insight-tab.active { background:#4FD1C5; color:#0d1b2a; border-color:#4FD1C5; }

        /* Skill rows */
        .js-skill-row {
          display:flex; align-items:center; gap:1rem;
          background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.07);
          border-radius:13px; padding:.9rem 1.1rem; margin-bottom:.6rem;
          transition:background .2s,transform .2s;
        }
        .js-skill-row:hover { background:rgba(255,255,255,0.07); transform:translateX(4px); }
        .js-skill-emoji { font-size:1.6rem; min-width:2.2rem; text-align:center; }
        .js-skill-info { flex:1; }
        .js-skill-name { font-size:.9rem; font-weight:700; color:#fff; margin:0 0 .35rem; }
        .js-skill-track { background:rgba(255,255,255,0.1); border-radius:20px; height:6px; overflow:hidden; }
        .js-skill-fill { height:6px; border-radius:20px; background:linear-gradient(90deg,#4FD1C5,#63b3ed); transition:width .8s ease; }
        .js-skill-growth { font-size:.78rem; font-weight:700; color:#68d391; white-space:nowrap; }

        /* Location rows */
        .js-loc-row {
          display:flex; justify-content:space-between; align-items:center;
          background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.07);
          border-radius:13px; padding:.9rem 1.1rem; margin-bottom:.6rem;
          transition:background .2s,transform .2s;
        }
        .js-loc-row:hover { background:rgba(255,255,255,0.07); transform:translateX(4px); }
        .js-loc-badge {
          background:rgba(79,209,197,0.12); border:1px solid rgba(79,209,197,0.28);
          color:#4FD1C5; font-size:.75rem; font-weight:700;
          padding:.18rem .65rem; border-radius:20px;
        }

        /* Salary */
        .js-salary-card {
          background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.07);
          border-radius:14px; padding:1.1rem 1.2rem; margin-bottom:.65rem;
          border-left:4px solid #4FD1C5; transition:background .2s,transform .2s;
        }
        .js-salary-card:hover { background:rgba(255,255,255,0.07); transform:translateX(5px); }
        .js-salary-top { display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:.6rem; }
        .js-salary-role { font-size:.92rem; font-weight:700; color:#fff; margin:0 0 .2rem; }
        .js-salary-exp  { font-size:.72rem; color:rgba(255,255,255,0.45); }
        .js-salary-amt  { font-size:1.05rem; font-weight:800; white-space:nowrap; }
        .js-salary-bar-row { display:flex; align-items:center; gap:.6rem; }
        .js-salary-track { flex:1; background:rgba(255,255,255,0.09); border-radius:20px; height:5px; overflow:hidden; }
        .js-salary-fill  { height:5px; border-radius:20px; background:linear-gradient(90deg,#4FD1C5,#68d391); }
        .js-salary-min, .js-salary-max { font-size:.7rem; color:rgba(255,255,255,0.4); white-space:nowrap; }

        /* Search container */
        .js-search-box {
          background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.08);
          border-radius:18px; padding:1.6rem 1.8rem; margin-bottom:1.8rem;
          animation:jsFadeUp .5s ease-out .1s both;
        }
        .js-search-row { display:grid; grid-template-columns:2fr 1fr; gap:1rem; margin-bottom:1rem; }
        @media(max-width:600px){ .js-search-row{ grid-template-columns:1fr; } }
        .js-search-label { font-size:.75rem; font-weight:700; color:rgba(255,255,255,0.5); text-transform:uppercase; letter-spacing:.5px; margin-bottom:.4rem; }
        .js-filter-row { display:grid; grid-template-columns:repeat(3,1fr); gap:.8rem; margin-bottom:1.2rem; }
        @media(max-width:600px){ .js-filter-row{ grid-template-columns:1fr; } }
        .js-select {
          width:100%; background:rgba(30,30,50,0.9); border:1px solid rgba(255,255,255,0.12);
          border-radius:10px; padding:.65rem .9rem; color:#fff; font-size:.85rem;
          font-family:inherit; cursor:pointer; outline:none; transition:border-color .2s;
        }
        .js-select:focus { border-color:#4FD1C5; }
        .js-search-btn {
          width:100%; padding:.85rem; border-radius:12px; border:none;
          background:linear-gradient(135deg,#4FD1C5,#38b2ac);
          color:#0d1b2a; font-size:1rem; font-weight:800; cursor:pointer;
          transition:all .22s; box-shadow:0 4px 20px rgba(79,209,197,0.28);
        }
        .js-search-btn:hover { transform:translateY(-2px); box-shadow:0 8px 28px rgba(79,209,197,0.45); }
        .js-search-btn:disabled { opacity:.5; cursor:not-allowed; transform:none; }

        /* Result cards */
        .js-result-card {
          display:flex; align-items:center; gap:1rem;
          background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.07);
          border-radius:15px; padding:1.1rem 1.3rem; margin-bottom:.75rem;
          transition:transform .22s,background .22s,box-shadow .22s;
        }
        .js-result-card:hover { transform:translateX(5px); background:rgba(255,255,255,0.08); box-shadow:0 8px 26px rgba(0,0,0,0.28); }
        .js-result-dot { width:4px; min-height:55px; border-radius:4px; flex-shrink:0; }
        .js-result-portal { font-size:.75rem; font-weight:800; text-transform:uppercase; letter-spacing:.7px; margin:0 0 .2rem; }
        .js-result-desc   { font-size:.85rem; color:rgba(255,255,255,0.55); margin:0; }
        .js-result-cta {
          padding:.42rem 1rem; border-radius:9px; font-size:.78rem; font-weight:700;
          color:#0d1b2a; white-space:nowrap; transition:opacity .18s,transform .18s;
        }
        .js-result-cta:hover { opacity:.85; }

        /* Company grid */
        .js-company-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(250px,1fr)); gap:1.1rem; }
        .js-company-card {
          background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.07);
          border-radius:16px; overflow:hidden; transition:transform .25s,box-shadow .25s,background .25s;
        }
        .js-company-card:hover { transform:translateY(-6px); background:rgba(255,255,255,0.07); box-shadow:0 14px 36px rgba(0,0,0,0.35); }
        .js-company-banner { height:6px; }
        .js-company-body   { padding:1.1rem 1.2rem; }
        .js-company-header { display:flex; align-items:center; gap:.7rem; margin-bottom:.5rem; }
        .js-company-emoji  { font-size:1.6rem; }
        .js-company-name   { font-size:1rem; font-weight:700; color:#fff; margin:0; }
        .js-company-desc   { font-size:.8rem; color:rgba(255,255,255,0.5); margin:0 0 .7rem; line-height:1.45; }
        .js-company-tags   { display:flex; flex-wrap:wrap; gap:.35rem; margin-bottom:.75rem; }
        .js-company-tag {
          background:rgba(79,209,197,0.1); color:#4FD1C5;
          border:1px solid rgba(79,209,197,0.25); border-radius:20px;
          font-size:.72rem; font-weight:500; padding:.15rem .5rem;
        }
        .js-company-cta { font-size:.78rem; font-weight:600; color:rgba(255,255,255,0.55); }
        .js-company-card:hover .js-company-cta { color:#4FD1C5; }

        /* Section title */
        .js-section-title {
          font-size:1.1rem; font-weight:700; color:#4FD1C5;
          margin:2rem 0 1rem; padding-bottom:.5rem;
          border-bottom:2px solid rgba(79,209,197,0.18);
          display:flex; align-items:center; gap:.45rem;
        }
      `}</style>

      {/* ── Hero ── */}
      <div className="js-hero">
        <h1>🔍 Smart Job Search</h1>
        <p>Discover curated opportunities across India's top hiring platforms</p>
        <div className="js-hero-badges">
          {['🌐 LinkedIn','💼 Indeed','📋 Naukri','🚀 Foundit','🌟 Glassdoor','🤖 AI-Matched'].map(b => (
            <span key={b} className="js-badge">{b}</span>
          ))}
        </div>
      </div>

      {/* ── Market Insights ── */}
      <div className="js-section-title">📊 Job Market Insights</div>
      <div className="js-insight-tabs">
        {['🔥 Trending Skills','📍 Top Locations','💰 Salary Insights'].map((t,i) => (
          <button key={t} className={`js-insight-tab${insightTab===i?' active':''}`} onClick={() => setInsightTab(i)}>{t}</button>
        ))}
      </div>

      {insightTab === 0 && TRENDING_SKILLS.map((s,i) => <SkillRow key={s.name} s={s} i={i} />)}
      {insightTab === 1 && TOP_LOCATIONS.map((l,i) => <LocationRow key={l.name} l={l} i={i} />)}
      {insightTab === 2 && SALARY_INSIGHTS.map((s,i) => <SalaryRow key={s.role} s={s} i={i} />)}

      {/* ── Search ── */}
      <div className="js-section-title">🔎 Search Jobs</div>
      <div className="js-search-box">
        <form onSubmit={handleSearch}>
          <div className="js-search-row">
            <div>
              <p className="js-search-label">Job Title / Skills</p>
              <input
                className="form-input"
                placeholder="e.g. Software Engineer, Data Scientist"
                value={query}
                onChange={e => { setQuery(e.target.value); setSearched(false); }}
              />
            </div>
            <div>
              <p className="js-search-label">Location</p>
              <input
                className="form-input"
                placeholder="e.g. Bangalore, Remote"
                value={location}
                onChange={e => setLocation(e.target.value)}
              />
            </div>
          </div>

          <div className="js-filter-row">
            <div>
              <p className="js-search-label">Experience</p>
              <select className="js-select" value={exp} onChange={e => setExp(e.target.value)}>
                {EXP_LEVELS.map(l => <option key={l}>{l}</option>)}
              </select>
            </div>
            <div>
              <p className="js-search-label">Job Type</p>
              <select className="js-select" value={jobType} onChange={e => setJobType(e.target.value)}>
                {JOB_TYPES.map(l => <option key={l}>{l}</option>)}
              </select>
            </div>
            <div>
              <p className="js-search-label">Salary Range</p>
              <select className="js-select" value={salary} onChange={e => setSalary(e.target.value)}>
                {SALARY_OPTS.map(l => <option key={l}>{l}</option>)}
              </select>
            </div>
          </div>

          <button type="submit" className="js-search-btn" disabled={!query.trim()}>
            🔍 SEARCH JOBS
          </button>
        </form>

        {/* ── Results ── */}
        {searched && query.trim() && (
          <div style={{ marginTop:'1.5rem' }}>
            <p style={{ color:'rgba(255,255,255,0.55)', fontSize:'.82rem', margin:'0 0 .9rem' }}>
              Showing results for <strong style={{ color:'#4FD1C5' }}>"{query}"</strong>
              {location && <> in <strong style={{ color:'#4FD1C5' }}>{location}</strong></>} across {PORTALS.length} platforms
            </p>
            {PORTALS.map(p => <PortalResultCard key={p.name} p={p} query={`${query} ${location}`.trim()} />)}
          </div>
        )}
      </div>

      {/* ── Featured Companies ── */}
      <div className="js-section-title">🏢 Featured Companies</div>
      <div className="js-company-grid">
        {FEATURED_COMPANIES.map(c => <CompanyCard key={c.name} c={c} />)}
      </div>
    </>
  );
}

import React from 'react';
import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom';
import './styles/global.css';
import Analyzer from './components/Analyzer';
import Builder from './components/Builder';
import Dashboard from './components/Dashboard';
import Jobs from './components/Jobs';

// Placeholder for Pages
const Home = () => (
  <div className="glass-surface" style={{textAlign: 'center', padding: '4rem 2rem'}}>
    <h1 className="text-gradient" style={{fontSize: '3rem', marginBottom: '1rem'}}>Smart Resume AI</h1>
    <p style={{color: 'var(--text-muted)', fontSize: '1.2rem', marginBottom: '2rem'}}>
      Elevate your career with AI-powered resume analysis and beautiful modern templates.
    </p>
    <div style={{display: 'flex', gap: '1rem', justifyContent: 'center'}}>
      <NavLink to="/analyzer" className="btn-primary">Analyze Resume</NavLink>
      <NavLink to="/builder" className="btn-primary" style={{background: 'transparent', border: '1px solid var(--primary)'}}>Build Resume</NavLink>
    </div>
  </div>
);

function App() {
  return (
    <BrowserRouter>
      <div className="app-container">
        <header className="nav-header">
          <h2 style={{margin: 0, color: 'var(--primary)'}}>SmartResume AI</h2>
          <nav className="nav-links">
            <NavLink to="/" className={({isActive}) => isActive ? 'nav-link active' : 'nav-link'}>Home</NavLink>
            <NavLink to="/analyzer" className={({isActive}) => isActive ? 'nav-link active' : 'nav-link'}>Analyzer</NavLink>
            <NavLink to="/builder" className={({isActive}) => isActive ? 'nav-link active' : 'nav-link'}>Builder</NavLink>
            <NavLink to="/dashboard" className={({isActive}) => isActive ? 'nav-link active' : 'nav-link'}>Dashboard</NavLink>
            <NavLink to="/jobs" className={({isActive}) => isActive ? 'nav-link active' : 'nav-link'}>Jobs</NavLink>
          </nav>
        </header>

        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/analyzer" element={<Analyzer />} />
            <Route path="/builder" element={<Builder />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/jobs" element={<Jobs />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;

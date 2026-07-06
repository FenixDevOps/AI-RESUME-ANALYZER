import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import ScoreDashboard from './ScoreDashboard';
import JDMatch from './JDMatch';

const Analyzer = () => {
  const [file, setFile] = useState(null);
  const [jobRole, setJobRole] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [resultData, setResultData] = useState(null); // full parsed response
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  const handleAnalyze = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a resume file (PDF or DOCX).');
      return;
    }

    setLoading(true);
    setError('');
    setResultData(null);

    const formData = new FormData();
    formData.append('file', file);
    if (jobRole) formData.append('job_role', jobRole);
    if (jobDescription) formData.append('job_description', jobDescription);

    try {
      const response = await fetch('/api/analyzer/analyze', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to analyze resume');
      }

      const data = await response.json();
      // data = { analysis: { analysis, resume_score, ats_score, strengths, weaknesses }, jd_match }
      setResultData(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Derive sub-fields safely
  const analysisObj  = resultData?.analysis ?? {};
  const markdownText = typeof analysisObj === 'object' ? (analysisObj.analysis ?? '') : String(analysisObj);
  const resumeScore  = analysisObj.resume_score ?? null;
  const atsScore     = analysisObj.ats_score    ?? null;
  const strengths    = analysisObj.strengths    ?? [];
  const weaknesses   = analysisObj.weaknesses   ?? [];
  const jdMatch      = resultData?.jd_match     ?? null;

  return (
    <div className="analyzer-root">
      {/* ── Upload Form Card ── */}
      <div className="glass-surface analyzer-form-card">
        <h2 className="text-gradient analyzer-heading">
          <span className="analyzer-heading-icon">🔍</span> Resume Analyzer
        </h2>
        <p className="analyzer-subtext">
          Upload your resume and optionally provide a job role and description for AI-powered feedback.
        </p>

        <form onSubmit={handleAnalyze} className="analyzer-form">
          {/* File Upload */}
          <div className="form-group">
            <label className="form-label">Resume File (PDF / DOCX)</label>
            <label className="file-drop-zone" htmlFor="resume-file-input">
              <span className="file-drop-icon">📄</span>
              <span className="file-drop-text">
                {file ? file.name : 'Click to choose or drag & drop your resume'}
              </span>
              <input
                id="resume-file-input"
                type="file"
                accept=".pdf,.docx"
                onChange={handleFileChange}
                style={{ display: 'none' }}
              />
            </label>
          </div>

          {/* Job Role */}
          <div className="form-group">
            <label className="form-label" htmlFor="job-role-input">Target Job Role <span className="optional-badge">optional</span></label>
            <input
              id="job-role-input"
              type="text"
              value={jobRole}
              onChange={(e) => setJobRole(e.target.value)}
              placeholder="e.g. Software Engineer, Data Scientist…"
              className="form-input"
            />
          </div>

          {/* Job Description */}
          <div className="form-group">
            <label className="form-label" htmlFor="jd-textarea">Job Description <span className="optional-badge">optional — enables JD Match</span></label>
            <textarea
              id="jd-textarea"
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder="Paste the full job description here to see keyword match analysis…"
              rows={5}
              className="form-input"
              style={{ resize: 'vertical' }}
            />
          </div>

          <button
            type="submit"
            id="analyze-btn"
            className="btn-primary analyze-btn"
            disabled={loading || !file}
          >
            {loading ? (
              <>
                <span className="btn-spinner" /> Analyzing…
              </>
            ) : (
              <>🚀 Analyze Resume</>
            )}
          </button>
        </form>

        {error && (
          <div className="error-banner">
            ⚠️ {error}
          </div>
        )}
      </div>

      {/* ── Results ── */}
      {resultData && (
        <div className="results-section">
          {/* Score Dashboard — always shown after analysis */}
          <ScoreDashboard
            resumeScore={resumeScore}
            atsScore={atsScore}
            strengths={strengths}
            weaknesses={weaknesses}
          />

          {/* JD Match — only if a job description was provided */}
          {jdMatch && <JDMatch jdMatch={jdMatch} />}

          {/* Markdown Analysis */}
          {markdownText && (
            <div className="glass-surface analysis-markdown-card">
              <h3 className="analysis-markdown-title">📋 Detailed Analysis</h3>
              <div className="markdown-body">
                <ReactMarkdown>{markdownText}</ReactMarkdown>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Analyzer;

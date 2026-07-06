import React, { useState } from 'react';

const Builder = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  // Base State
  const [template, setTemplate] = useState('Modern');
  const [personalInfo, setPersonalInfo] = useState({
    full_name: '', email: '', phone: '', location: '', linkedin: '', portfolio: '', title: ''
  });
  const [summary, setSummary] = useState('');
  
  // Dynamic Lists State
  const [experience, setExperience] = useState([{ company: '', title: '', dates: '', description: '' }]);
  const [education, setEducation] = useState([{ school: '', degree: '', dates: '', gpa: '' }]);
  const [skills, setSkills] = useState(['']);
  const [projects, setProjects] = useState([{ name: '', dates: '', description: '' }]);

  // Handlers for dynamic lists
  const addExperience = () => setExperience([...experience, { company: '', title: '', dates: '', description: '' }]);
  const updateExperience = (index, field, value) => {
    const newExp = [...experience];
    newExp[index][field] = value;
    setExperience(newExp);
  };

  const addEducation = () => setEducation([...education, { school: '', degree: '', dates: '', gpa: '' }]);
  const updateEducation = (index, field, value) => {
    const newEdu = [...education];
    newEdu[index][field] = value;
    setEducation(newEdu);
  };

  const addSkill = () => setSkills([...skills, '']);
  const updateSkill = (index, value) => {
    const newSkills = [...skills];
    newSkills[index] = value;
    setSkills(newSkills);
  };

  const addProject = () => setProjects([...projects, { name: '', dates: '', description: '' }]);
  const updateProject = (index, field, value) => {
    const newProj = [...projects];
    newProj[index][field] = value;
    setProjects(newProj);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    // Clean up empty data
    const cleanExperience = experience.filter(exp => exp.company || exp.title);
    const cleanEducation = education.filter(edu => edu.school || edu.degree);
    const cleanSkills = skills.filter(skill => skill.trim() !== '');
    const cleanProjects = projects.filter(proj => proj.name);

    const payload = {
      template,
      personal_info: personalInfo,
      summary,
      experience: cleanExperience.length > 0 ? cleanExperience : undefined,
      education: cleanEducation.length > 0 ? cleanEducation : undefined,
      skills: cleanSkills.length > 0 ? cleanSkills : undefined,
      projects: cleanProjects.length > 0 ? cleanProjects : undefined
    };

    try {
      const response = await fetch('/api/builder/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to generate resume');
      }

      // Handle file download
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${personalInfo.full_name.replace(/ /g, '_')}_resume.docx` || 'resume.docx';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      a.remove();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-surface" style={{ maxWidth: '900px', margin: '0 auto', padding: '2rem' }}>
      <h2 className="text-gradient">Resume Builder</h2>
      <p style={{ color: 'var(--text-muted)', marginBottom: '2rem' }}>
        Fill out your details to instantly generate a professionally formatted DOCX resume.
      </p>

      {error && (
        <div style={{ marginBottom: '2rem', padding: '1rem', background: 'rgba(231, 76, 60, 0.1)', borderLeft: '4px solid #e74c3c', color: '#e74c3c' }}>
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
        
        {/* Template Selection */}
        <div style={{ padding: '1.5rem', background: 'var(--surface-light)', borderRadius: '8px', border: '1px solid var(--border)' }}>
          <h3 style={{ marginBottom: '1rem' }}>Template</h3>
          <select 
            value={template} 
            onChange={(e) => setTemplate(e.target.value)}
            style={{ width: '100%', padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border)', background: 'var(--surface)', color: 'var(--text)' }}
          >
            <option value="Modern">Modern</option>
            <option value="Professional">Professional</option>
            <option value="Minimal">Minimal</option>
            <option value="Creative">Creative</option>
          </select>
        </div>

        {/* Personal Info */}
        <div style={{ padding: '1.5rem', background: 'var(--surface-light)', borderRadius: '8px', border: '1px solid var(--border)' }}>
          <h3 style={{ marginBottom: '1rem' }}>Personal Information</h3>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
            <input type="text" placeholder="Full Name *" required value={personalInfo.full_name} onChange={e => setPersonalInfo({...personalInfo, full_name: e.target.value})} style={inputStyle} />
            <input type="text" placeholder="Professional Title" value={personalInfo.title} onChange={e => setPersonalInfo({...personalInfo, title: e.target.value})} style={inputStyle} />
            <input type="email" placeholder="Email *" required value={personalInfo.email} onChange={e => setPersonalInfo({...personalInfo, email: e.target.value})} style={inputStyle} />
            <input type="text" placeholder="Phone" value={personalInfo.phone} onChange={e => setPersonalInfo({...personalInfo, phone: e.target.value})} style={inputStyle} />
            <input type="text" placeholder="Location" value={personalInfo.location} onChange={e => setPersonalInfo({...personalInfo, location: e.target.value})} style={inputStyle} />
            <input type="text" placeholder="LinkedIn URL" value={personalInfo.linkedin} onChange={e => setPersonalInfo({...personalInfo, linkedin: e.target.value})} style={inputStyle} />
            <input type="text" placeholder="Portfolio/Website" value={personalInfo.portfolio} onChange={e => setPersonalInfo({...personalInfo, portfolio: e.target.value})} style={inputStyle} />
          </div>
        </div>

        {/* Summary */}
        <div style={{ padding: '1.5rem', background: 'var(--surface-light)', borderRadius: '8px', border: '1px solid var(--border)' }}>
          <h3 style={{ marginBottom: '1rem' }}>Professional Summary</h3>
          <textarea 
            placeholder="A brief summary of your professional background..." 
            value={summary} 
            onChange={e => setSummary(e.target.value)} 
            rows={4}
            style={{ width: '100%', padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border)', background: 'var(--surface)', color: 'var(--text)', resize: 'vertical' }}
          />
        </div>

        {/* Experience */}
        <div style={{ padding: '1.5rem', background: 'var(--surface-light)', borderRadius: '8px', border: '1px solid var(--border)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <h3 style={{ margin: 0 }}>Experience</h3>
            <button type="button" onClick={addExperience} className="btn-primary" style={{ padding: '0.4rem 0.8rem', fontSize: '0.9rem' }}>+ Add</button>
          </div>
          {experience.map((exp, index) => (
            <div key={index} style={{ display: 'flex', flexDirection: 'column', gap: '0.8rem', marginBottom: '1.5rem', paddingBottom: '1.5rem', borderBottom: index < experience.length - 1 ? '1px dashed var(--border)' : 'none' }}>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                <input type="text" placeholder="Company Name" value={exp.company} onChange={e => updateExperience(index, 'company', e.target.value)} style={inputStyle} />
                <input type="text" placeholder="Job Title" value={exp.title} onChange={e => updateExperience(index, 'title', e.target.value)} style={inputStyle} />
              </div>
              <input type="text" placeholder="Dates (e.g. Jan 2020 - Present)" value={exp.dates} onChange={e => updateExperience(index, 'dates', e.target.value)} style={inputStyle} />
              <textarea placeholder="Description / Accomplishments (bullet points)" value={exp.description} onChange={e => updateExperience(index, 'description', e.target.value)} rows={3} style={{ width: '100%', padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border)', background: 'var(--surface)', color: 'var(--text)', resize: 'vertical' }} />
            </div>
          ))}
        </div>

        {/* Education */}
        <div style={{ padding: '1.5rem', background: 'var(--surface-light)', borderRadius: '8px', border: '1px solid var(--border)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <h3 style={{ margin: 0 }}>Education</h3>
            <button type="button" onClick={addEducation} className="btn-primary" style={{ padding: '0.4rem 0.8rem', fontSize: '0.9rem' }}>+ Add</button>
          </div>
          {education.map((edu, index) => (
            <div key={index} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1rem' }}>
              <input type="text" placeholder="School/University" value={edu.school} onChange={e => updateEducation(index, 'school', e.target.value)} style={inputStyle} />
              <input type="text" placeholder="Degree" value={edu.degree} onChange={e => updateEducation(index, 'degree', e.target.value)} style={inputStyle} />
              <input type="text" placeholder="Dates" value={edu.dates} onChange={e => updateEducation(index, 'dates', e.target.value)} style={inputStyle} />
              <input type="text" placeholder="GPA (optional)" value={edu.gpa} onChange={e => updateEducation(index, 'gpa', e.target.value)} style={inputStyle} />
            </div>
          ))}
        </div>

        {/* Skills */}
        <div style={{ padding: '1.5rem', background: 'var(--surface-light)', borderRadius: '8px', border: '1px solid var(--border)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <h3 style={{ margin: 0 }}>Skills</h3>
            <button type="button" onClick={addSkill} className="btn-primary" style={{ padding: '0.4rem 0.8rem', fontSize: '0.9rem' }}>+ Add</button>
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
            {skills.map((skill, index) => (
              <input key={index} type="text" placeholder="Skill" value={skill} onChange={e => updateSkill(index, e.target.value)} style={{ ...inputStyle, width: 'auto', flex: '1 1 150px' }} />
            ))}
          </div>
        </div>

        {/* Projects */}
        <div style={{ padding: '1.5rem', background: 'var(--surface-light)', borderRadius: '8px', border: '1px solid var(--border)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <h3 style={{ margin: 0 }}>Projects</h3>
            <button type="button" onClick={addProject} className="btn-primary" style={{ padding: '0.4rem 0.8rem', fontSize: '0.9rem' }}>+ Add</button>
          </div>
          {projects.map((proj, index) => (
            <div key={index} style={{ display: 'flex', flexDirection: 'column', gap: '0.8rem', marginBottom: '1rem' }}>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                <input type="text" placeholder="Project Name" value={proj.name} onChange={e => updateProject(index, 'name', e.target.value)} style={inputStyle} />
                <input type="text" placeholder="Dates (optional)" value={proj.dates} onChange={e => updateProject(index, 'dates', e.target.value)} style={inputStyle} />
              </div>
              <textarea placeholder="Description" value={proj.description} onChange={e => updateProject(index, 'description', e.target.value)} rows={2} style={{ width: '100%', padding: '0.75rem', borderRadius: '4px', border: '1px solid var(--border)', background: 'var(--surface)', color: 'var(--text)', resize: 'vertical' }} />
            </div>
          ))}
        </div>

        <button type="submit" className="btn-primary" disabled={loading} style={{ alignSelf: 'center', padding: '1rem 3rem', fontSize: '1.1rem', marginTop: '1rem' }}>
          {loading ? 'Generating...' : 'Generate & Download Resume'}
        </button>

      </form>
    </div>
  );
};

const inputStyle = {
  width: '100%', 
  padding: '0.75rem', 
  borderRadius: '4px', 
  border: '1px solid var(--border)', 
  background: 'var(--surface)', 
  color: 'var(--text)'
};

export default Builder;

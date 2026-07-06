# 🚀 Smart AI Resume Analyzer

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![React](https://img.shields.io/badge/Frontend-React-61DAFB)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688)
![AI](https://img.shields.io/badge/AI-NLP-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Project-Active-success)

An **AI-powered Resume Analysis Platform** that evaluates resumes, predicts ATS compatibility scores, detects missing skills, provides actionable recommendations to improve job readiness, and offers built-in job search capabilities.

The system leverages **Natural Language Processing (NLP)**, **Generative AI**, and **machine learning techniques** to help candidates optimize resumes for modern recruitment systems.

---

# 🌐 Live Demo
https://ai-resume-analyzer-v43d.onrender.com/

---

# 📸 Project Preview

## Resume Analyzer Dashboard

*(Add screenshot of the dashboard here)*

Example:

![Dashboard](docs/dashboard.png)

---

# 🎥 Demo

*(Add a short GIF demonstrating how the app works)*

Example:

![Demo](docs/demo.gif)

---

# 📌 Key Features

### 📄 Resume Parsing
Upload resumes (PDF/DOCX) and automatically extract:
* Skills
* Education
* Work experience
* Projects

### 📊 ATS Score Prediction
The system calculates an **ATS compatibility score** based on:
* Resume structure
* Keyword optimization
* Section completeness
* Skill relevance

### 🧠 Skill Gap Detection & AI Analysis
Identify missing skills required for modern job roles and receive AI-driven improvement suggestions using Google Generative AI (Gemini).

### 📈 Resume Analytics Dashboard
Interactive visualization including:
* Skill distribution
* Resume strength indicators
* Resume improvement insights

### 🧰 Resume Builder
Generate structured, professional resumes easily directly from the platform and export them to PDF or DOCX.

### 🎯 Job Search
Built-in job search capabilities that recommend relevant jobs based on your role and skills.

### 💬 Feedback System & Admin Dashboard
Integrated user feedback collection and an admin dashboard to monitor application usage and insights.

---

# 🧠 AI Concepts Used

* Generative AI (LLM integration)
* Natural Language Processing (NLP)
* Named Entity Recognition (NER)
* Resume skill extraction & text preprocessing
* Resume scoring algorithms
* Data visualization

---

# 🏗 System Architecture

```text
User Upload Resume (React Frontend)
        │
        ▼
Resume Parsing Engine (FastAPI Backend)
        │
        ▼
Skill Extraction Module (SpaCy/NLTK)
        │
        ▼
AI Analysis & ATS Scoring (Generative AI)
        │
        ▼
Recommendation & Job Search Engine
        │
        ▼
Analytics Dashboard & Resume Builder
```

---

# 🛠 Tech Stack

### Frontend
* React
* Vite
* Lucide React
* Recharts

### Backend
* FastAPI (Python 3.10+)
* SQLite (Database)

### Data Processing & Visualization
* Pandas
* NumPy

### AI & NLP
* Google Generative AI (Gemini)
* SpaCy
* NLTK
* Scikit-learn

### Document Processing
* PyPDF2 / pdfminer.six / pdfplumber
* python-docx
* pytesseract / pdf2image

---

# 📂 Project Structure

```text
Smart_AI_Resume_Analyzer
│
├── frontend/               # React frontend source code
│   ├── src/                # React components and assets
│   └── package.json        # Frontend dependencies
│
├── backend/                # FastAPI backend source code
│   ├── api/                # API route definitions
│   └── main.py             # FastAPI entry point
│
├── config/                 # Configuration files and database setup
├── utils/                  # Helper modules (AI analyzer, builder, etc.)
├── poppler/                # PDF processing binaries (for Windows)
├── Dockerfile              # Docker containerization configuration
├── requirements.txt        # Python backend dependencies
└── README.md
```

---

# ⚙️ Installation

## Prerequisites
- Node.js & npm (for the frontend)
- Python 3.10+ (for the backend)
- Poppler (for PDF rendering/processing, included for Windows users)
- Tesseract OCR (optional, for advanced PDF parsing)

## Clone the repository

```bash
git clone https://github.com/FenixDevOps/Smart_AI_Resume_Analyzer.git
cd Smart_AI_Resume_Analyzer
```

## Set up Environment Variables
Create a `.env` file in the backend directory and add your API keys (e.g., Google Generative AI API key):
```env
GOOGLE_API_KEY=your_google_api_key_here
```

## Run the Application (Local Development)

### 1. Start the Backend (FastAPI)
```bash
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000
```

### 2. Start the Frontend (React)
Open a new terminal window:
```bash
cd frontend
npm install
npm run dev
```
The frontend will typically run on `http://localhost:5173`.

## Docker Installation
You can also run the application using Docker:
```bash
docker build -t smart-resume-analyzer .
docker run -p 8000:8000 smart-resume-analyzer
```

---

# 📊 Application Workflow

1️⃣ **Upload resume**: User uploads their resume in PDF or DOCX format.
2️⃣ **AI extracts resume information**: The system parses out contact info, skills, education, etc.
3️⃣ **Resume is analyzed for structure and keywords**: Checks against job roles and industry standards.
4️⃣ **ATS score is calculated**: An overall compatibility score is generated.
5️⃣ **Missing skills and improvements are suggested**: Get actionable feedback and AI-driven recommendations.
6️⃣ **Job Search (Optional)**: Explore current job listings that match your skills.

---

# 🔮 Future Improvements

* Resume vs Specific Job Description Matching
* Enhanced Candidate Ranking System
* AI Interview Preparation Assistant
* Advanced Resume Optimization using Generative AI
* Multi-language support

---

# 👨‍💻 Author

**Bathini Manikanta**

GitHub: [FenixDevOps](https://github.com/FenixDevOps)

---

# ⭐ Support

If you find this project useful, consider giving it a ⭐ on GitHub.

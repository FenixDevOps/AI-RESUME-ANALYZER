# Deployment Guide: Smart AI Resume Analyzer

The Smart AI Resume Analyzer features a modern **React (Vite) + FastAPI** architecture. 
Because the application relies on system-level libraries for OCR and PDF processing (`tesseract-ocr`, `poppler-utils`), **Docker is the recommended deployment method.**

---

## 🚀 Recommended Approach: Unified Docker Container

We have configured the backend to serve the frontend statically. This allows you to build the entire application into a **single Docker container** that can be deployed anywhere (Render, Railway, Heroku, AWS, DigitalOcean, etc.).

### Step 1: Build the Docker Image
From the root of the project, run:
```bash
docker build -t smart-resume-ai .
```
*Note: This utilizes a multi-stage Dockerfile. It will first use Node.js to compile the React frontend, and then use Python to install system dependencies, backend requirements, and bundle everything together.*

### Step 2: Run the Docker Container
```bash
docker run -p 8000:8000 smart-resume-ai
```
The application will now be available at `http://localhost:8000`.

### Deploying to Render / Railway
1. Connect your GitHub repository to your Render or Railway account.
2. Create a new **Web Service**.
3. Select **Docker** as the environment/build type.
4. The platform will automatically read the `Dockerfile`, build the multi-stage image, and expose it on the required port.

---

## 🛠 Alternative Approach: Separate Frontend & Backend

If you prefer to deploy the frontend to a CDN (like Vercel or Netlify) and host the backend separately, follow these steps.

### 1. Deploy the Backend (FastAPI)
Deploy the backend to a provider that supports Docker (due to `tesseract` and `poppler`). 
* **Environment Variables:** Set `CORS_ORIGINS` (if configured) to allow requests from your frontend URL.
* **Build:** Use the existing `Dockerfile`, but you can optionally remove the Node.js frontend build stages to save build time.

### 2. Deploy the Frontend (Vercel / Netlify)
Deploy the `frontend/` directory to Vercel or Netlify.
* **Build Command:** `npm run build`
* **Output Directory:** `dist`
* **Environment Variables:** You must configure the frontend to point to your live backend API URL. 
  * Update the API base URL in your React components (e.g., replace `http://localhost:8000` with `https://your-backend-url.onrender.com`).

---

## 💻 Local Development

To run the application locally for development purposes, you should run both servers simultaneously.

### 1. Start the Backend
Open a terminal in the root directory:
```bash
# Install dependencies
pip install -r requirements.txt

# Start FastAPI server
python -m uvicorn backend.main:app --reload --port 8000
```

### 2. Start the Frontend
Open a second terminal in the `frontend/` directory:
```bash
# Install dependencies
npm install

# Start Vite dev server
npm run dev
```
Access the application at `http://localhost:5173`.
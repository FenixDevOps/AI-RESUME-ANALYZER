# ==========================================
# Stage 1: Build the React Frontend
# ==========================================
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend

# Copy frontend package files
COPY frontend/package*.json ./
RUN npm install

# Copy frontend source code and build
COPY frontend/ .
RUN npm run build


# ==========================================
# Stage 2: Build the FastAPI Backend
# ==========================================
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies including Tesseract OCR and Poppler
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    poppler-utils \
    libpoppler-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend application code
COPY . .

# Copy the built React frontend from Stage 1 to the backend's expected path
COPY --from=frontend-builder /app/frontend/dist /app/frontend/dist

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PORT=8000

# Expose the port Uvicorn will run on
EXPOSE 8000

# Command to run the unified application
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
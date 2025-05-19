# Use Python base image
FROM python:3.10-slim as backend

WORKDIR /app

# Install backend dependencies
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy backend code
COPY backend ./backend

# Copy models
COPY backend/models ./backend/models

# --- Frontend build ---
FROM node:18 as frontend
WORKDIR /frontend
COPY frontend ./
RUN npm install && npm run build

# --- Final image ---
FROM python:3.10-slim
WORKDIR /app

# Copy backend and install dependencies
COPY --from=backend /app/backend /app/backend
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Copy frontend build to backend static directory
COPY --from=frontend /frontend/dist /app/backend/static

# Set environment variable for Hugging Face token
ENV HF_TOKEN=your_hf_token_here

# Expose port
EXPOSE 8000

# Start FastAPI app
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"] 
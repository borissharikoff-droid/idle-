FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run FastAPI server (bot runs separately or in background)
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}

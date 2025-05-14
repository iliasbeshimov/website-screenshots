FROM python:3.9-slim

# Install system dependencies for Chromium
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Set environment variables for Chromium
ENV CHROMIUM_FLAGS="--no-sandbox --disable-gpu"

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "app:app"]

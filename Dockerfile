FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for wkhtmltoimage
RUN apt-get update && apt-get install -y \
    wkhtmltopdf \
    libx11-6 \
    libxrender1 \
    libxext6 \
    libssl-dev \
    libjpeg-dev \
    libpng-dev \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app.py .

# Run the app with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "--workers", "1", "--timeout", "300", "app:app"]

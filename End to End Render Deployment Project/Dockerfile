FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependency list and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Train the model at build time so the container is self-contained
RUN python src/train.py

# Expose Flask port
EXPOSE 5000

# Set Flask env variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Run with gunicorn in production
CMD gunicorn -b 0.0.0.0:${PORT:-5000} app:app

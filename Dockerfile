# Using a slim Python base
FROM python:3.9-slim

# Install OS-level build tools for any native deps
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential git && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY app.py model_utils.py expected_answers.json ./

# Expose port and default command
EXPOSE 5000
CMD ["python", "app.py"]

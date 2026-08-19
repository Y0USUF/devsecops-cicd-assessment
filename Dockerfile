FROM python:3.11-slim

WORKDIR /app

# Install curl for internal container health-checks
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ /app/

EXPOSE 5000

CMD ["python", "app.py"]

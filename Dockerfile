FROM python:3.11-alpine

WORKDIR /app

# Install curl safely using Alpine's package manager
RUN apk add --no-cache curl

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ /app/

EXPOSE 5000

CMD ["python", "app.py"]

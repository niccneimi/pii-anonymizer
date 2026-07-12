FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/models && chmod 755 /app/models
COPY src/ src/
COPY data/ data/

RUN mkdir -p /app/logs && chmod 775 /app/logs

EXPOSE 8000

ENV PYTHONPATH=/app

CMD ["python", "-m", "src.api.main"]
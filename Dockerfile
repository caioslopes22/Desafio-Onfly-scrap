
FROM python:3.11-slim

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY src /app/src
COPY run.py /app/run.py

RUN mkdir -p /app/outputs

ENV PYTHONPATH=/app/src

CMD ["python", "/app/run.py"]

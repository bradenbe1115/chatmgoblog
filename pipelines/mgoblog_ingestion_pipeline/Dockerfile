FROM python:3.10-slim-bookworm

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

WORKDIR /app

RUN mkdir -p /src
COPY src/ /src/
RUN pip install -e /src

COPY requirements.txt .
RUN pip install -r requirements.txt 

COPY pipelines/mgoblog_ingestion_pipeline/mgoblog_ingestion_pipeline.py .

ENTRYPOINT ["python","mgoblog_ingestion_pipeline.py"]
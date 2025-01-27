FROM python:3.10-slim-bookworm

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

WORKDIR /app

RUN mkdir -p /src
COPY src/ /src/
RUN pip install -e /src

COPY requirements.txt .
RUN pip install -r requirements.txt 

COPY pipelines/incremental_mgoblog_embedding_pipeline/incremental_mgoblog_embedding_pipeline.py .

ENTRYPOINT ["python","incremental_mgoblog_embedding_pipeline.py"]
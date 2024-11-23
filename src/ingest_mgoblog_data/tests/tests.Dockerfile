FROM python:3.11-slim-buster

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

WORKDIR /app

# Copy over packages and install
COPY src/ingest_mgoblog_data ingest_mgoblog_data
RUN pip3 install -r ingest_mgoblog_data/requirements.txt

ENV PYTHONPATH="/app/ingest_mgoblog_data:${PYTHONPATH}"

RUN pip install pytest

ENTRYPOINT ["pytest","-s","ingest_mgoblog_data/tests"]
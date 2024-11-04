FROM python:3.11-slim-buster

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

# Copy over packages and install
COPY src/ /src/
RUN pip install -e /src

CMD ["python", "src/ingest_mgoblog_data/scrape_mgoblog_data/scrape_mgoblog_data.py"]
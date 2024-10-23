FROM python:3.11-slim-buster

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

# Create directories
RUN mkdir -p common tests

# Copy over common modules and install requirements
COPY ./src/mgoblog_data/common common
RUN pip install --no-cache-dir -r /common/requirements.txt

COPY ./src/mgoblog_data/tests/test_web_scraper.py test_web_scraper.py
COPY ./src/mgoblog_data/tests/requirements.txt /tests/requirements.txt
RUN pip install --no-cache-dir -r /tests/requirements.txt

ENTRYPOINT ["pytest","-s","test_web_scraper.py"]
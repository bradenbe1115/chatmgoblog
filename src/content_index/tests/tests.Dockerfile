FROM python:3.10-slim-bookworm

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

WORKDIR /app

# Install requirements up here for caching when making changes
COPY src/content_index/requirements.txt .
RUN pip3 install -r requirements.txt

COPY src/content_index content_index

ENV PYTHONPATH="/app/content_index:${PYTHONPATH}"

RUN pip install pytest

ENTRYPOINT ["pytest","-s","content_index/tests"]
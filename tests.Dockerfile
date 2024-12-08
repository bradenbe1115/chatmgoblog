FROM python:3.10-slim-bookworm

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

WORKDIR /app

RUN mkdir -p /src
COPY src/ /src/
RUN pip install -e /src

COPY tests/ /tests/
RUN pip install pytest

ENTRYPOINT ["pytest","-s","/tests/unit", "/tests/integration"]
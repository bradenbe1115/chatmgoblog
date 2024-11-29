FROM python:3.10-slim-bookworm

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

WORKDIR /app

# Copy over packages and install
COPY src/embed embed
RUN pip3 install -r embed/requirements.txt

ENV PYTHONPATH="/app/embed:${PYTHONPATH}"

RUN pip install pytest

ENTRYPOINT ["pytest","-s","embed/tests"]
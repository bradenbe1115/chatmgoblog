FROM python:3.10-slim-bookworm

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

WORKDIR /app

# Copy over packages and install
COPY src/index_content index_content
RUN pip3 install -r index_content/requirements.txt

ENV PYTHONPATH="/app/index_content:${PYTHONPATH}"

RUN pip install pytest

ENTRYPOINT ["pytest","-s","index_content/tests"]
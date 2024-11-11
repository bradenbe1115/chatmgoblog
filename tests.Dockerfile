FROM python:3.10-slim-bookworm

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

# Create directories
RUN mkdir -p /src tests

# Copy over common modules and install requirements
COPY src/ /src/
RUN pip install -e /src

COPY tests/ /tests/
RUN pip install --no-cache-dir -r /tests/requirements.txt

ENTRYPOINT ["pytest","-s","tests"]
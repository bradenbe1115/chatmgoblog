FROM python:3.10-slim-bookworm

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

# Copy over modules and install requirements
COPY src/ /src/
RUN pip install -e /src

# Create directories
RUN mkdir -p /src tests

COPY tests/ /tests/
RUN pip install --no-cache-dir -r /tests/requirements.txt

ENTRYPOINT ["pytest","-s","tests"]
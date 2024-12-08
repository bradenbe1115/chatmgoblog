FROM python:3.10-slim-bookworm

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt 

RUN mkdir -p /src
COPY src/ /src/
RUN pip install -e /src

COPY pipelines/user_query/user_query.py .

ENTRYPOINT ["python","user_query.py"]
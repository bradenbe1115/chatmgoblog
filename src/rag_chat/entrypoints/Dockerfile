FROM python:3.10-slim-bookworm

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install flask

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt 

RUN mkdir -p /src
COPY src/ /src/
RUN pip install -e /src

WORKDIR /src/rag_chat/entrypoints

CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]
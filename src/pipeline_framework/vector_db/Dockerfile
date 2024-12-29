FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

RUN pip install chromadb

EXPOSE 6333

CMD ["chroma", "run", "--host", "0.0.0.0", "--port", "6333", "--path", "/db_path"]
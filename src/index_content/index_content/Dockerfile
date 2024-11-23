FROM python:3.11-slim-buster

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY ./src/chatmgoblog/chatmgoblog_requirements.txt .
RUN pip3 install -r chatmgoblog_requirements.txt
COPY src/chatmgoblog /chatmgoblog/

COPY src/index_content/common /common/
COPY src/index_content/index_content/index_content.py .

COPY src/index_content/index_content/requirements.txt .
RUN pip3 install -r requirements.txt

CMD ["python", "index_content.py"]
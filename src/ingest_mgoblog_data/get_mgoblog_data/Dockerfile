FROM python:3.11-slim-buster

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

# Copy landing db interface module
COPY ./src/utils/landing_db_interface utils/landing_db_interface 
COPY ./src/utils/requirements.txt utils_requirements.txt
RUN pip install --no-cache-dir -r utils_requirements.txt

# Copy over common modules and install requirements
COPY ./src/mgoblog_data/common common
RUN pip install --no-cache-dir -r /common/requirements.txt

COPY ./src/mgoblog_data/get_mgoblog_data/get_mgoblog_data.py get_mgoblog_data.py

CMD ["python", "get_mgoblog_data.py"]
FROM python:3.10-slim
RUN apt-get update
RUN apt-get -y install libpq-dev gcc

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt --no-cache-dir

COPY . /app

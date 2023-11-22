
FROM python:3.9
RUN apt-get update
RUN apt-get -y install libpq-dev gcc

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt --no-cache-dir

COPY . /app

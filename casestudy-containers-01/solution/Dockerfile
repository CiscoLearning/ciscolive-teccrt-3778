FROM python:3.9-slim

RUN mkdir -p /app
COPY app /app
RUN pip install -r /app/requirements.txt

EXPOSE 80

VOLUME /app/db

ENV STORAGE_DB_API=./storage.db

WORKDIR /app

CMD ./storage-status.py

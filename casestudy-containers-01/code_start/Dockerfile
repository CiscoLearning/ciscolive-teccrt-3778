FROM python:3.9-slim

RUN mkdir -p /app
COPY app /app
RUN pip install -r /app/requirements.txt
# TODO:
#   * Indicate that the app will use tcp/80
#   * Indicate the app requires a volume, /app/db
#   * Indicate the app uses an environment variable, STORAGE_API_DB

WORKDIR /app

CMD ./storage-status.py

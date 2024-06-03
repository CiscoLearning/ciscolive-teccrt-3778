FROM python:3.9-slim

RUN mkdir -p /app
COPY app /app
RUN pip install -r /app/requirements.txt

# TODO: Indicate that the app will use tcp/80
# This is done with the EXPOSE command.  This is only informative to the
# Docker user that this port is eligible for mapping.
EXPOSE 80

# TODO: Indicate the app requires a volume, /app/db
# This is done with the VOLUME command.  This is only informative to the
# Docker user that this container will use this mount point.
VOLUME /app/db

# TODO: Indicate the app uses an environment variable, STORAGE_API_DB
# NOTE: We have a constraint in the question that the default needs to be ./storage.db
# The ENV command indicates which environment variables are available for user configuration.
ENV STORAGE_API_DB=./storage.db

WORKDIR /app

CMD ./storage-status.py

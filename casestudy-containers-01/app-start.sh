#!/bin/bash

if [ -z "${DB_FILE}" ]; then
    echo "ERROR: Set the environment variable DB_FILE to the path to the SQLite database prior to running."
    exit 1
fi

if [ -z "${APP_PORT}" ]; then
    echo "ERROR: Set the environment variable APP_PORT to the TCP port to use for the app prior to running."
    exit 1
fi

NAME=storage-status
IMAGE=${NAME}

docker build -t ${IMAGE} -f Dockerfile .
docker stop ${NAME}
docker rm ${NAME}

# TODO
#   Uncomment and then flesh out the `docker run` command below such that:
#   * The ./db directory is mounted at /app/db in the container
#   * The value of the DB_FILE environment variable is passed as STORAGE_API_DB in the container
#   * The port specified in the environment variable APP_PORT is mapped to the app's tcp/80
#   * The container's image can be referenced as ${IMAGE}

#docker run -itd --restart unless-stopped --name ${NAME}

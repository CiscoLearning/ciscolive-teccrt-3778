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
docker stop ${NAME} 2>/dev/null
docker rm ${NAME} 2>/dev/null

docker run -itd --restart unless-stopped --name ${NAME} -v $(realpath ./db):/app/db \
    -e STORAGE_API_DB=${DB_FILE} -p ${APP_PORT}:80 ${IMAGE}

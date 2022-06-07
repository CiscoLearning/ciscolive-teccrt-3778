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

# TODO
#   Uncomment and then flesh out the `docker run` command below such that:
#   * The ./db directory is mounted at /app/db in the container
#   * The value of the DB_FILE environment variable is passed as STORAGE_API_DB to the container
#   * The port specified in the environment variable APP_PORT is mapped to the app's tcp/80
#   * The container's image can be referenced as ${IMAGE}
#
# The `-v $(realpath ./db):/app/db`` arguments (or --volume ...) maps HOST_PATH:CONTAINER_PATH.
#  The realpath command is used to create a fully-qualified host path.
#
# The `-e STORAGE_API_DB=${DB_FILE}` arguments (or --env) sets environment variables in the running
#  container.  In this case, the STORAGE_API_DB variable that our container accepts is set to the
#  ${DB_FILE} environment variable from the host.
#
# The `-p ${APP_PORT}:80` arguments (or --port) maps HOST_PORT:CONTAINER_PORT.
#  While you could just to `-p 8080:80`, this wouldn't be flexible enough to satisfy the question
#  constraints.
docker run -itd --restart unless-stopped --name ${NAME} -v $(realpath ./db):/app/db \
    -e STORAGE_API_DB=${DB_FILE} -p ${APP_PORT}:80 ${IMAGE}

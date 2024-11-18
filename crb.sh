#!/bin/bash

# Set container name
CONTAINER_NAME="cdxgen-container"

# Stop and remove the container if it exists
docker stop "$CONTAINER_NAME" 2> /dev/null
docker rm "$CONTAINER_NAME" 2> /dev/null

# Pull the latest image
docker pull ghcr.io/cyclonedx/cdxgen

# Start the container in detached mode
# docker run -d --name "$CONTAINER_NAME" ghcr.io/cyclonedx/cdxgen
docker run -d --name "$CONTAINER_NAME" --rm -v /tmp:/tmp -p 9090:9090 -v $(pwd):/app:rw -t ghcr.io/cyclonedx/cdxgen -r /app --server --server-host 0.0.0.0


# copy files for docker cannot be done inside of docker
docker cp -r sharing "$CONTAINER_NAME":/home/cyclonedx


# Open a shell in the container
docker exec -i "$CONTAINER_NAME" /bin/bash < crb-com.sh


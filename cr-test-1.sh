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

# Open a shell in the container
docker exec -it "$CONTAINER_NAME" /bin/bash

# move into the /home/appthreat folder
cd /home/appthreat/

# Run git clone and git pull commands (replace with your actual repository)
# git clone project
# cd project
# install or setup the project
git clone https://github.com/CycloneDX/cdxgen.git 
cd cdxgen


# Run other commands in the container
# ...

# Exit the container shell
exit
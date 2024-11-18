from subprocess import run
import os
import sqlite3
from argparse import ArgumentParser

# git clone http://github.com/owner/project
# cdxgen -t language /path/to/project --arguments
# sbom compare
parser = ArgumentParser(
    prog="cdxgen-test-script",
    description="Run cdxgen quickly to generate SBOM",
)
parser.add_argument(
    '-c', '--container-name',
    dest="c",
    default="ghcr.io/cyclonedx/cdxgen",
    help="Name of the CDXGEN container that needs to be pulled"
)
parser.add_argument(
    "-g", "--github-repo",
    dest="g",
    help="Github repo link you want to be scanned"
)
parser.add_argument(
    "-e", "--environment-setup",
    dest="e",
    help="Add a script here that can be used for environment setup"
)
parser.add_argument(
    "-n", "--name",
    dest="n",
    help="Name your test something inorder to remember it"
)
parser.add_argument(
    "-a", "--arguments",
    dest="a",
    default="",  # Default to empty string if no arguments are provided
    help="Arguments for cdxgen"
)
parser.add_argument(
    "-r", "--run",
    dest="r",
    help="Command to run inside the project repo"
)
args, unkown = parser.parse_known_args()
args = vars(args)

# TODO: remove this
print(unkown)

with open("temp.sh", "w") as f:
    
    bash_commands = f"""
        cd /home/cyclonedx/
        source ~/.bashrc

        {args.get("e", "")}

        git clone https://github.com/CycloneDX/cdxgen.git 
        cd cdxgen

        corepack enable pnpm 
        pnpm install
        
        cd ..

        git clone --filter=blob:none {args['g']}  # Use --filter=blob:none for faster cloning
        cd $(basename {args['g']} .git)  # cd into the cloned repo directory

        {args.get("r", "")}  # Run the command inside the repo

        cd ..  # cd back to the previous directory

        

        node cdxgen/bin/cdxgen.js {args.get("a", "")} ./$(basename {args['g']} .git) # Run cdxgen with provided arguments
    """
    f.write(bash_commands)


bash_starter = f"""
CONTAINER_NAME="cdxgen-container"

# Stop and remove the container if it exists
docker stop "$CONTAINER_NAME" 2> /dev/null
docker rm "$CONTAINER_NAME" 2> /dev/null

# Pull the latest image
docker pull {args['c']}

# Start the container in detached mode
docker run -d --name "$CONTAINER_NAME" --rm -v /tmp:/tmp -p 9090:9090 -v $(pwd):/app:rw -t ghcr.io/cyclonedx/cdxgen -r /app --server --server-host 0.0.0.0

# copy files for docker cannot be done inside of docker
docker cp ./sharing "$CONTAINER_NAME":/home/cyclonedx

# Open a shell in the container
docker exec -i "$CONTAINER_NAME" /bin/bash < temp.sh

# Copy the bom.json file from the container to the results folder
docker cp "$CONTAINER_NAME":/home/cyclonedx/bom.json results/
"""

os.system(bash_starter)

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('results/cdxgen_results.db')
cursor = conn.cursor()

# Create a table to store the results (using JSON for the bom data)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        github_repo TEXT,
        cdxgen_args TEXT,
        run_command TEXT,
        bom_data JSON
    )
''')

# Read the bom.json file
with open("results/bom.json", "r") as f:
    bom_data = json.load(f)

# Store the values in the database (including the bom data as JSON)
cursor.execute('''
    INSERT INTO results (name, github_repo, cdxgen_args, run_command, bom_data)
    VALUES (?, ?, ?, ?, ?)
''', (args.get("n"), args.get("g"), args.get("a"), args.get("r"), json.dumps(bom_data)))

conn.commit()
conn.close()
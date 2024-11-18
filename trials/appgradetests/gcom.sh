# move into the /home/appthreat folder
cd /home/cyclonedx/

# environment setup
sdk install java 17.0.13-tem

# Run git clone and git pull commands (replace with your actual repository)
# git clone project
# cd project
# install or setup the project
git clone https://github.com/CycloneDX/cdxgen.git 
cd cdxgen

# Install the project dependencies
corepack enable pnpm 
pnpm install

# get files to test




# Run other commands in the container
# ...

# Exit the container shell
# exit
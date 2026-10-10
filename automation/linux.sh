#! /bin/bash

# This bash script is used to execute a scraping job automatically

# First change directory the project root, where the compose file is located
script_parent_dir="$(dirname "$(dirname "$BASH_SOURCE")")"
cd $script_parent_dir

# Run the docker commands to perform a scraping job and clean up afterwards
# Containers need to run in the background so they don't block further command execution
docker compose up -d
docker compose wait scraper
docker compose down
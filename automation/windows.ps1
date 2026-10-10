# This powershell script is used to execute a scraping job automatically

# First change directory the project root, where the compose file is located
$ProjectRoot = Split-Path $PSScriptRoot -Parent 
Set-Location $ProjectRoot

# Run the docker commands to perform a scraping job and clean up afterwards
# Containers need to run in the background so they don't block further command execution
docker compose up -d
docker compose wait scraper
docker compose down
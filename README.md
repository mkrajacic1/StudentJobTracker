# StudentJobTracker

An automated student job posting tracking service.

## Description

StudentJobTracker is a **Python**-based service that monitors student job postings
using a reverse-engineered public backend API as its data source.
It incorporates request throttling to ensure responsible data collection.

The service notifies users via **Telegram Bot API** about new and modified job opportunities
within their selected tracked categories. It uses **PostgreSQL** for data persistence
and **Docker** for containerized deployment.

### Main features

- Automated execution through **Windows Task Scheduler** or **cron**
- CLI for managing tracked job categories
- Telegram notifications for new and modified jobs, as well as system status alerts
- Docker-based deployment for portability across different environments
- Centralized logging and error handling for easier troubleshooting

### Planned features

I am planning to eventually add the following features:

- LLM integration for more accurate job classification  
  and the ability to define custom tailored job preferences
- Data analytics and job trends dashboard
- Incorporate additional job posting data sources
- Enable alternative notification mechanisms

## Installation and setup

#### Requirements

- **git**
- **Docker**
- **Telegram** app

#### Registering a Telegram Bot

1. To get started, open [@BotFather](https://t.me/botfather) on Telegram
2. Follow the instructions to create your bot
3. Save the received **authentication token** which will be added to the project's **.env** file

#### Clone the repository

```bash
git clone https://github.com/mkrajacic1/StudentJobTracker
```

#### Environment file setup

Create the **.env** file inside the project directory.

```bash
cd StudentJobTracker
cp .env.example .env
```

Store your bot **authentication token** in .env.

```env
TELEGRAM_BOT_TOKEN=<your-bot-token-goes-here>
```

Optionally edit the database environment variables.

#### Get the Telegram chat id

To get your Telegram bot **chat id** you can use docker to run the **_get_chat_id_** service container.

```bash
docker compose run --rm get_chat_id
```

Save the chat id to .env.

```env
TELEGRAM_CHAT_ID=<your-chat_id-goes-here>
```

#### Choose categories to track

Run the **_manage_categories_** service container.  
If the categories haven't yet been stored they will first have to be scraped.

```bash
docker compose run --rm manage_categories
```

#### Optional: run the main service

You can manually start the scraper service container, to run once:

```bash
docker compose run --rm scraper
```

## Automate container execution

The service is intended to be scheduled to run in the background with minimal user interaction.

PostgreSQL data is stored in a persistent Docker volume, ensuring that database contents are preserved across container restarts and removals.

### Windows Task Scheduler

To automate the service execution on **Windows** my preferred approach is scheduling a **.bat**
script execution using the **Task Scheduler**.
The .bat script executes docker commands to start the service containers and stop them after task execution.

```bat
REM The contents of the .bat script

REM Execute commands from the project directory
cd C:\path\to\StudentJobTracker

REM Build and start the main containers
docker compose up -d

REM Wait for the scraper container to finish execution
docker compose wait scraper

REM Stop and remove the containers
docker compose down
```

### Linux cron job

To automate execution on Linux, I recommend scheduling a **.sh** script using `cron`.
The script executes the scraper container, waits for it to finish, and removes
the containers afterward.

Create a script named run_scraper.sh:

```shell
#!/bin/bash

# Execute commands from the project directory
cd /path/to/StudentJobTracker || exit 1

# Build and start the main containers
docker compose up -d

# Wait for the scraper container to finish execution
docker compose wait scraper

# Stop and remove the containers
docker compose down
```

Make the script executable:

```bash
chmod +x /path/to/StudentJobTracker/run_scraper.sh
```

Open the crontab editor:

```bash
crontab -e
```

Add an entry to schedule the scraper. For example, to execute it every day at 16:00:

```bash
0 8 \* \* \* /path/to/StudentJobTracker/run_scraper.sh >> /path/to/StudentJobTracker/logs/cron.log 2>&1
```

The output of scheduled executions will be appended to cron.log.

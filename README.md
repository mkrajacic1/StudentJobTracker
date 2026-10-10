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
If the available categories haven't been fetched yet, they will be retrieved automatically.

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

Disclaimer: the Docker engine must be running for scheduled tasks to work.

### Linux cron job

To schedule automated execution on Linux, create a `cron` job which executes the `automation/linux.sh` script.
Make sure the script has a valid shebang and that the user running the cron job has permission to execute the script.

Example crontab entry which executes the script Mon-Fri at 16:00:

```bash
0 16 * * 1-5 /path/to/project/automation/linux.sh
```

### Windows Task Scheduler

To schedule automated execution on Windows, use **Task Scheduler**.

Task Action configuration:

- Action: Start a program
- Program/script: powershell.exe
- Add argument: C:\path\to\project\automation\windows.ps1

**Tip**: In task General settings, under Security Options select the task to run wheter the user is logged on or not.
This will run the task in the background so no terminal window pops up.

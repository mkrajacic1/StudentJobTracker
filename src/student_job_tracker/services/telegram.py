import dotenv
import os
import requests

from student_job_tracker.models.job import JobPosting

dotenv.load_dotenv()
BOT_TOKEN = os.environ["telegram-bot-token"]
CHAT_ID = os.environ["telegram-chat-id"]

UPDATES_API = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
SEND_MESSAGE_API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

SC_BASE_LINK = "https://www.sczg.unizg.hr/poslovi"


def new_jobs_notify(se: requests.Session, new_jobs: list[JobPosting]) -> None:
    for job in new_jobs:
        link = f"{SC_BASE_LINK}/{job.slug}"
        message_text = f"NOVI OGLAS!\n\n{job.company_name}\n\n{job.job_title}\n\nSatnica: {job.hourly_rate}\n\nPredviđeni početak rada: {job.work_start}\n\n{link}"
        params = {"chat_id": CHAT_ID, "text": message_text}
        se.post(SEND_MESSAGE_API, params=params)


def modified_jobs_notify(se: requests.Session, modified_jobs: list[JobPosting]) -> None:
    for job in modified_jobs:
        link = f"{SC_BASE_LINK}/{job.slug}"
        message_text = f"Promijenjen oglas!\n\n{job.company_name}\n\n{job.job_title}\n\nSatnica: {job.hourly_rate}\n\nPredviđeni početak rada: {job.work_start}\n\n{link}"
        params = {"chat_id": CHAT_ID, "text": message_text}
        se.post(SEND_MESSAGE_API, params=params)


def jobs_updates_notify(new_jobs: list[JobPosting], modified_jobs: list[JobPosting]) -> None:
    with requests.Session() as se:
        new_jobs_notify(se, new_jobs)
        modified_jobs_notify(se, modified_jobs)


def alert_notify(alert_message: str) -> None:
    alert_message = f"Upozorenje!\n\n{alert_message}"
    params = {"chat_id": CHAT_ID, "text": alert_message}
    requests.post(SEND_MESSAGE_API, params=params)
    

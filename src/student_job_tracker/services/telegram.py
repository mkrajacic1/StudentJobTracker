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


def new_jobs_notify(se: requests.Session, new_jobs: list[JobPosting]):
    for job in new_jobs:
        link = f"{SC_BASE_LINK}/{job.slug}"
        message_text = f"NOVI OGLAS!\n\n{job.company_name}\n\n{job.job_title}\n\nsatnica: {job.hourly_rate}\n\nPredviđeni početak rada: {job.work_start}\n\n{link}"
        params = {"chat_id": CHAT_ID, "text": message_text}
        status = se.post(SEND_MESSAGE_API, params=params)
        print(f"Message status: {"Success" if status.json()["ok"] else "Failure"}")


def modified_jobs_notify(se: requests.Session, modified_jobs: list[JobPosting]):
    for job in modified_jobs:
        link = f"{SC_BASE_LINK}/{job.slug}"
        message_text = f"Promijenjen oglas:\n\n{job.company_name}\n\n{job.job_title}\n\nsatnica: {job.hourly_rate}\n\nPredviđeni početak rada: {job.work_start}\n\n{link}"
        params = {"chat_id": CHAT_ID, "text": message_text}
        status = se.post(SEND_MESSAGE_API, params=params)
        print(f"Message status: {"Success" if status.json()["ok"] else "Failure"}")
    

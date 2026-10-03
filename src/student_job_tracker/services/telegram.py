import requests
from requests import RequestException, JSONDecodeError

from typing import Any

from student_job_tracker.core.config import TELEGRAM_BOT_CHAT_ID, TELEGRAM_BOT_TOKEN
from student_job_tracker.models.job import JobPosting


UPDATES_API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
SEND_MESSAGE_API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

SC_BASE_LINK = "https://www.sczg.unizg.hr/poslovi"

TIMEOUT_DURATION = 5


class TelegramError(Exception):
    """General class for Telegram bot related exceptions"""

# raises a TelegramError exception if the message wasn't sent properly
def check_response_status(response_json: Any) -> None:
    status = response_json["ok"]
    if not status:
        failure_description = response_json["description"]
        exc = TelegramError("Unsuccessful Telegram message")
        exc.add_note(failure_description)
        raise exc


def send_notification(se: requests.Session, message_text: str) -> None:
    data = {"chat_id": TELEGRAM_BOT_CHAT_ID, "text": message_text}
    response = se.post(SEND_MESSAGE_API, json=data, timeout=TIMEOUT_DURATION)
    response.raise_for_status()
    check_response_status(response.json())


def new_jobs_notify(se: requests.Session, new_jobs: list[JobPosting]) -> None:
    for job in new_jobs:
        link = f"{SC_BASE_LINK}/{job.slug}"
        message_text = f"⚡ NOVI OGLAS!\n\n{job.company_name}\n\n{job.job_title}\n\nSatnica: {job.hourly_rate}\n\nPredviđeni početak rada: {job.work_start}\n\n{link}"
        send_notification(se, message_text)


def modified_jobs_notify(se: requests.Session, modified_jobs: list[JobPosting]) -> None:
    for job in modified_jobs:
        link = f"{SC_BASE_LINK}/{job.slug}"
        message_text = f"🔄 Promijenjen oglas!\n\n{job.company_name}\n\n{job.job_title}\n\nSatnica: {job.hourly_rate}\n\nPredviđeni početak rada: {job.work_start}\n\n{link}"
        send_notification(se, message_text)

# message data is sent via JSON in the request body
def jobs_updates_notify(new_jobs: list[JobPosting], modified_jobs: list[JobPosting]) -> None:
    try:
        with requests.Session() as se:
            new_jobs_notify(se, new_jobs)
            modified_jobs_notify(se, modified_jobs)
    except JSONDecodeError as exc:
        raise TelegramError("Error occurred trying to decode Telegram response body for notification") from exc
    except RequestException as exc:
        raise TelegramError("An error occurred attempting to send a notification via Telegram bot") from exc


def alert_notify(alert_message: str) -> None:
    alert_message = f"⚠️ Upozorenje!\n\n{alert_message}"
    data = {"chat_id": TELEGRAM_BOT_CHAT_ID, "text": alert_message}
    try:
        response = requests.post(SEND_MESSAGE_API, json=data, timeout=TIMEOUT_DURATION)
        response.raise_for_status()
        check_response_status(response.json())
    except JSONDecodeError as exc:
        raise TelegramError("Error occurred trying to decode Telegram response body for warning message") from exc
    except RequestException as exc:
        raise TelegramError("Error occurred attempting to send a warning message") from exc


def success_notify() -> None:
    success_message = "🟢 Uspješno obavljen pregled oglasa!"
    data = {"chat_id": TELEGRAM_BOT_CHAT_ID, "text": success_message}
    try:
        response = requests.post(SEND_MESSAGE_API, json=data, timeout=TIMEOUT_DURATION)
        response.raise_for_status()
        check_response_status(response.json())
    except JSONDecodeError as exc:
        raise TelegramError("Error occurred trying to decode Telegram response body for success message") from exc
    except RequestException as exc:
        raise TelegramError("Error occurred attempting to send a success message") from exc
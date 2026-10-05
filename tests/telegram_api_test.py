import pytest
import requests

from student_job_tracker.services.telegram import send_notification


def test_send_valid_notification():
    message_text = f"⚡ NEW JOB POSTING!\n\nTech Company d.o.o.\n\nSoftware Engineer\n\nHourly wage: 6,56 EUR\n\nStart Date: 2026-10-10 \n\nhttps://github.com/mkrajacic1/StudentJobTracker"
    with requests.Session() as se:
        send_notification(se, message_text)


def test_missing_text_notification():
    message_text = ""
    with requests.Session() as se:
        with pytest.raises(requests.HTTPError):
            send_notification(se, message_text)

    
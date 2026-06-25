import time
from datetime import datetime
from dataclasses import dataclass
import requests

import text_from_html


REFERER = "https://www.sczg.unizg.hr/"
INITIAL_JOBS_URL = "https://www.sczg.unizg.hr/_next/data/WlD2U-ISgimZiMr1mvQa5/poslovi.json"
SUBSEQUENT_PAGES = "https://www.sczg.unizg.hr/wp-json/wp/v2/jobs"
TIMEOUT_DURATION = 5
JOB_BASE_URL = "https://www.sczg.unizg.hr/poslovi/"


@dataclass
class JobPosting:
    id: int
    published_timestamp: datetime
    last_modified_timestamp: datetime
    slug: str
    job_title: str
    category_id: int
    contact: str
    work_location: str
    work_start: str
    work_end: str
    hourly_rate: str
    work_hours: str
    job_description: str
    applicant_profile: str
    required_skills: str
    preferred_skills: str
    expires: datetime


def parse_job(job: dict) -> JobPosting:
    job_id = job["id"]
    published_timestamp = datetime.fromisoformat(job["date"].strip())
    last_modified_timestamp = datetime.fromisoformat(job["modified"].strip())
    slug = job["slug"].strip()

    meta_data = job["meta"]
    title = meta_data["title"].strip()
    category_id = meta_data["type"]
    contact = text_from_html.extract(meta_data["contact_student"].strip())
    location = meta_data["city"].strip()
    work_start = meta_data["work_start"].strip()
    work_end = meta_data["work_end"].strip()
    job_hourly_rate = meta_data["payment_rate"].strip()
    work_hours = meta_data["work_hours"].strip()
    description = text_from_html.extract(meta_data["description"].strip())
    applicant_profile = text_from_html.extract(meta_data["whyme"].strip())
    required_skills = meta_data["skills"].strip()
    preferred_skills = meta_data["labels"].strip()
    expires = datetime.fromisoformat(meta_data["active_until"].strip())

    return JobPosting(
        id=job_id,
        published_timestamp=published_timestamp,
        last_modified_timestamp=last_modified_timestamp,
        expires=expires,
        slug=slug,
        job_title=title,
        category_id=category_id,
        contact=contact,
        work_location=location,
        work_start=work_start,
        work_end=work_end,
        hourly_rate=job_hourly_rate,
        work_hours=work_hours,
        job_description=description,
        applicant_profile=applicant_profile,
        required_skills=required_skills,
        preferred_skills=preferred_skills,
    )


def process_jobs(jobs: list[dict]) -> list[JobPosting]:
    return [parse_job(job) for job in jobs]


def scrape_jobs() -> list[JobPosting]:
    all_jobs = []
    headers = {"Referer": REFERER}
    
    initial_jobs_response = requests.get(INITIAL_JOBS_URL, headers=headers, timeout=TIMEOUT_DURATION)
    initial_jobs_raw = initial_jobs_response.json()
    initial_jobs = initial_jobs_raw["pageProps"]["initialJobs"]
    all_jobs.extend(process_jobs(initial_jobs))

    total_pages = int(initial_jobs_raw["pageProps"]["totalPages"])
    page_params = {
        "per_page": 30,
        "allowed_sc": "true",
        "orderby": "modified",
        "filter_by_date": "true",
        "order": "desc"
    }
    for page_num in range(2, total_pages + 1):
        time_ms= round(time.time_ns() / 1000000)
        page_params["page"] = page_num
        page_params["timestamp"] = time_ms

        page_response = requests.get(SUBSEQUENT_PAGES, headers=headers, timeout=TIMEOUT_DURATION, params=page_params)
        page_jobs = page_response.json()
        all_jobs.extend(process_jobs(page_jobs))

    job_categories = {category["id"]: category["name"] for category in initial_jobs_raw["pageProps"]["categories"]}
    jobs_per_category = {}
    longest_title = 0
    for job in all_jobs:
        category_name = job_categories[job.category_id]
        jobs_per_category[category_name] = jobs_per_category.get(category_name, 0) + 1
        longest_title = max(longest_title, len(job.job_title))

    return all_jobs

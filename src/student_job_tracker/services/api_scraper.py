import requests

from datetime import datetime
import time
import unicodedata

from student_job_tracker.models.category import JobCategory
from student_job_tracker.models.html_parser import MyHTMLParser
from student_job_tracker.models.job import JobPosting


REFERER = "https://www.sczg.unizg.hr/"
INITIAL_JOBS_URL = "https://www.sczg.unizg.hr/_next/data/WlD2U-ISgimZiMr1mvQa5/poslovi.json"
SUBSEQUENT_PAGES = "https://www.sczg.unizg.hr/wp-json/wp/v2/jobs"
TIMEOUT_DURATION = 5
JOB_BASE_URL = "https://www.sczg.unizg.hr/poslovi/"


def text_from_html(html: str) -> str:
    parser = MyHTMLParser()
    parser.feed(html)
    text = parser.get_text()
    text = unicodedata.normalize("NFC", text)
    text = ' '.join(text.split())
    return text


def parse_job(job: dict) -> JobPosting:
    job_id = job["id"]
    published_at = datetime.fromisoformat(job["date"].strip())
    last_modified = datetime.fromisoformat(job["modified"].strip())
    slug = job["slug"].strip()

    meta_data = job["meta"]
    title = meta_data["title"].strip()
    category_id = meta_data["type"]
    contact = text_from_html(meta_data["contact_student"].strip())
    location = meta_data["city"].strip()
    work_start = meta_data["work_start"].strip()
    work_end = meta_data["work_end"].strip()
    job_hourly_rate = meta_data["payment_rate"].strip()
    work_hours = meta_data["work_hours"].strip()
    description = text_from_html(meta_data["description"].strip())
    applicant_profile = text_from_html(meta_data["whyme"].strip())
    required_skills = meta_data["skills"].strip()
    preferred_skills = meta_data["labels"].strip()
    expires = datetime.fromisoformat(meta_data["active_until"].strip())

    return JobPosting(
        job_id=job_id,
        published_at=published_at,
        last_modified=last_modified,
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


def parse_jobs(jobs: list[dict]) -> list[JobPosting]:
    return [parse_job(job) for job in jobs]


def parse_category(category: dict) -> JobCategory:
    category_id = category["id"]
    slug = category["slug"].strip()
    category_name = category["name"].strip()

    return JobCategory(
        category_id=category_id,
        slug=slug,
        category_name=category_name
    )


def parse_categories(categories: list[dict]) -> list[JobCategory]:
    return [parse_category(category) for category in categories]


def scrape_job_data() -> tuple[list[JobPosting], list[JobCategory]]:
    with requests.Session() as se:
        se.headers.update({"Referer": REFERER})
        
        initial_jobs_response = se.get(INITIAL_JOBS_URL, timeout=TIMEOUT_DURATION)
        initial_jobs_data = initial_jobs_response.json()
        time.sleep(1)

        total_pages = int(initial_jobs_data["pageProps"]["totalPages"])
        paginated_jobs = []
        for page_num in range(2, total_pages + 1):
            time_ms= round(time.time_ns() / 1000000)
            page_params = {
                "per_page": 30, 
                "page": page_num,
                "timestamp": time_ms,
                "allowed_sc": "true", 
                "orderby": "modified", 
                "filter_by_date": "true", 
                "order": "desc"
            }
            page_response = se.get(SUBSEQUENT_PAGES, timeout=TIMEOUT_DURATION, params=page_params)
            paginated_jobs.append(page_response.json())

            if page_num != total_pages:
                time.sleep(1)

    categories = initial_jobs_data["pageProps"]["categories"]
    all_categories = parse_categories(categories)

    initial_jobs = initial_jobs_data["pageProps"]["initialJobs"]
    paginated_jobs = [job for job_list in paginated_jobs for job in job_list]   # need to flatten the list
    all_jobs = []
    all_jobs.extend(parse_jobs(initial_jobs))
    all_jobs.extend(parse_jobs(paginated_jobs))
    
    return all_jobs, all_categories
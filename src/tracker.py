from repositories import jobs
from api_scraper import scrape_job_data


def populate_jobs_and_categories():
    job_postings, categories = scrape_job_data()
    jobs.populate_categories(categories)
    jobs.populate_jobs(job_postings)


def populate_jobs_table():
    job_postings, _ = scrape_job_data()
    jobs.populate_jobs(job_postings)


def reset_jobs_table():
    jobs.clear_jobs()
    populate_jobs_table()


def resest_jobs_and_categories():
    jobs.clear_jobs_and_categories()
    populate_jobs_and_categories()

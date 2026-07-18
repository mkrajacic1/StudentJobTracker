from psycopg.rows import DictRow
from psycopg_pool import ConnectionPool

from datetime import datetime

from student_job_tracker.models.job import JobPosting
from student_job_tracker.repositories import jobs
from student_job_tracker.services.api_scraper import scrape_job_data


def populate_jobs_and_categories(pool: ConnectionPool):
    job_postings, categories = scrape_job_data()
    with pool.connection() as conn:
        jobs.populate_categories(conn, categories)
        jobs.populate_jobs(conn, job_postings)


def populate_jobs_table(pool: ConnectionPool):
    job_postings, _ = scrape_job_data()
    with pool.connection() as conn:
        jobs.populate_jobs(conn, job_postings)
    
    
def reset_jobs_table(pool: ConnectionPool):
    with pool.connection() as conn:
        jobs.truncate_jobs(conn)
    populate_jobs_table(pool)


def resest_jobs_and_categories(pool: ConnectionPool):
    with pool.connection() as conn:
        jobs.truncate_jobs_and_categories(conn)
    populate_jobs_and_categories(pool)


def find_deleted_jobs(jobs_from_snapshot: list[DictRow], scraped_jobs: set[int]) -> list[int]:
    deleted_jobs = []
    for job in jobs_from_snapshot:
        job_id = job["job_id"]
        if job_id not in scraped_jobs:
            print(f"Job {job_id} not available, will be deleted.")
            deleted_jobs.append(job_id)

    return deleted_jobs


def find_new_and_modified_jobs(job_postings: list[JobPosting], snapshot_jobs_last_modified: dict[int, datetime]) -> tuple[list[JobPosting], list[JobPosting]]:
    new_jobs, modified_jobs = [], []
    for job in job_postings:
        if job.job_id not in snapshot_jobs_last_modified:
            print(f"New job: {job.job_id}")
            new_jobs.append(job)
        elif job.last_modified != snapshot_jobs_last_modified[job.job_id]:
            print(f"Modified job: {job.job_id}")
            modified_jobs.append(job)

    return new_jobs, modified_jobs


def scrape_and_update_jobs(pool: ConnectionPool):
    job_postings, _ = scrape_job_data()
    scraped_jobs_ids = {job.job_id for job in job_postings}

    with pool.connection() as conn:
        jobs_current_db_snapshot = jobs.fetch_jobs_modified_time(conn)
        snapshot_jobs_last_modified = {job["job_id"]: job["last_modified"] for job in jobs_current_db_snapshot}

        deleted_jobs = find_deleted_jobs(jobs_current_db_snapshot, scraped_jobs_ids)
        jobs.delete_jobs(conn, deleted_jobs)

        new_jobs, modified_jobs = find_new_and_modified_jobs(job_postings, snapshot_jobs_last_modified)
        jobs.insert_jobs(conn, new_jobs)
        jobs.modify_jobs(conn, modified_jobs)
    

def track_categories(pool: ConnectionPool):
    with pool.connection() as conn:
        available_categories = jobs.fetch_category_status(conn)
        for category in available_categories:
            print(f"{category["category_name"]}\tID:{category["category_id"]}\tCurrently tracking: {"yes" if category["tracked_status"] else "no"}")
        print()

        chosen_categories = input("Choose which categories to track, type category IDs separated by spaces: ")
        chosen_categories = chosen_categories.split()
        
        jobs.stop_tracking_all_categories(conn)
        jobs.start_tracking_categories(conn, chosen_categories)






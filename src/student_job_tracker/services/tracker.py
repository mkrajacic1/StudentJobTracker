from psycopg import DatabaseError
from psycopg.rows import DictRow
from psycopg_pool import ConnectionPool, PoolTimeout

from datetime import datetime

from student_job_tracker.models.category import JobCategory
from student_job_tracker.models.job import JobPosting
from student_job_tracker.repositories import jobs
from student_job_tracker.services.sc_api_scraper import scrape
from student_job_tracker.services import telegram


class DatabaseServiceError(Exception):
    """Exception class for database related errors"""


class TrackerError(Exception):
    """A general exception class for tracker service errors"""


def populate_jobs_and_categories(pool: ConnectionPool):
    job_postings, categories = scrape()
    try:
        with pool.connection() as conn:
            jobs.populate_categories(conn, categories)
            jobs.insert_jobs(conn, job_postings)
    except PoolTimeout as exc:
        raise DatabaseServiceError("Unable to get connection from the pool while populating the database") from exc
    except DatabaseError as exc:
        raise DatabaseServiceError("An error occurred trying to populate the database") from exc


def find_deleted_jobs(jobs_from_snapshot: list[DictRow], scraped_jobs: set[int]) -> list[int]:
    deleted_jobs = []
    for job in jobs_from_snapshot:
        job_id = job["job_id"]
        if job_id not in scraped_jobs:
            deleted_jobs.append(job_id)

    return deleted_jobs


def find_new_and_modified_jobs(job_postings: list[JobPosting], snapshot_jobs_last_modified: dict[int, datetime]) -> tuple[list[JobPosting], list[JobPosting]]:
    new_jobs, modified_jobs = [], []
    for job in job_postings:
        if job.job_id not in snapshot_jobs_last_modified:
            new_jobs.append(job)
        elif job.last_modified != snapshot_jobs_last_modified[job.job_id]:
            modified_jobs.append(job)

    return new_jobs, modified_jobs


def update_job_state(pool: ConnectionPool, scraped_jobs: list[JobPosting]) -> tuple[list[JobPosting], list[JobPosting]]:
    scraped_jobs_ids = {job.job_id for job in scraped_jobs}
    try:
        with pool.connection() as conn:
            db_snapshot_jobs = jobs.fetch_jobs_modified_time(conn)
            snapshot_jobs_last_modified = {job["job_id"]: job["last_modified"] for job in db_snapshot_jobs}

            deleted_jobs = find_deleted_jobs(db_snapshot_jobs, scraped_jobs_ids)
            jobs.delete_jobs(conn, deleted_jobs)

            new_jobs, modified_jobs = find_new_and_modified_jobs(scraped_jobs, snapshot_jobs_last_modified)
            jobs.modify_jobs(conn, modified_jobs)
            jobs.insert_jobs(conn, new_jobs)
    except PoolTimeout as exc:
        raise DatabaseServiceError("Unable to get connection from the pool while updating job state") from exc
    except DatabaseError as exc:
        raise DatabaseServiceError("A database error occurred trying to update job state") from exc

    return new_jobs, modified_jobs


def track_jobs(pool: ConnectionPool, job_postings: list[JobPosting]):
    try:
        with pool.connection() as conn:
            tracked_categories = jobs.fetch_categories_status(conn)
    except PoolTimeout as exc:
        raise DatabaseServiceError("Unable to get connection from the pool while fetching tracked categories") from exc
    except DatabaseError as exc:
        raise DatabaseServiceError("A database error occurred trying to fetch tracked categories") from exc
    
    tracked_categories = {category["category_id"] for category in tracked_categories if category["tracked_status"]}

    new_jobs, modified_jobs = update_job_state(pool, job_postings)
    tracked_new_jobs = [job for job in new_jobs if job.category_id in tracked_categories]
    tracked_modified_jobs = [job for job in modified_jobs if job.category_id in tracked_categories]
    telegram.jobs_updates_notify(tracked_new_jobs, tracked_modified_jobs)
    

def compare_categories(scraped_categories: list[JobCategory], db_categories: list[JobCategory]) -> list[JobCategory]:
    db_categories_by_id = {category.category_id: category for category in db_categories}
    scraped_categories_by_id = {category.category_id: category for category in scraped_categories}

    if db_categories_by_id.keys() != scraped_categories_by_id.keys():
        raise TrackerError("Job category IDs changed!")

    modified_categories = []
    for id, scraped_category in scraped_categories_by_id.items():
        db_category = db_categories_by_id[id]
        if scraped_category.slug != db_category.slug or scraped_category.category_name != db_category.category_name:
            modified_categories.append(scraped_category)

    return modified_categories


def monitor_categories(pool: ConnectionPool, scraped_categories: list[JobCategory]):
    try:
        with pool.connection() as conn:
            db_categories = jobs.fetch_categories(conn)
            modified_categories = compare_categories(scraped_categories, db_categories)
            if modified_categories:
                alert_message = f"Sljedeće kategorije poslova su promijenjene (ID): {", ".join([str(category.category_id) for category in modified_categories])}."
                telegram.alert_notify(alert_message)
                jobs.modify_categories(conn, modified_categories)
    except PoolTimeout as exc:
        raise DatabaseServiceError("Unable to get connection from the pool while monitoring job categories") from exc
    except DatabaseError as exc:
        raise DatabaseServiceError("A database error occurred trying to monitor possible category changes") from exc        
from connect import get_db_connection
from models.job import JobPosting
from models.category import JobCategory
from psycopg.rows import class_row, dict_row, DictRow
from datetime import datetime


INSERT_JOB_SQL = """
                INSERT INTO job_postings (
                    job_id,
                    published_at,
                    last_modified,
                    expires,
                    slug,
                    job_title,
                    category_id,
                    contact,
                    work_location,
                    work_start,
                    work_end,
                    hourly_rate,
                    work_hours,
                    job_description,
                    applicant_profile,
                    required_skills,
                    preferred_skills
                ) 
                VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s, %s, %s
                );
                """

def populate_jobs(jobs: list[JobPosting]) -> None:
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.executemany(INSERT_JOB_SQL, [job.to_db_row() for job in jobs])


def populate_categories(categories: list[JobCategory]) -> None:
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO job_categories (category_id, slug, category_name) VALUES (%s, %s, %s);",
                [category.to_db_row() for category in categories]
            )


def clear_jobs() -> None:
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE job_postings;")


def clear_jobs_and_categories() -> None:
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE job_postings, job_categories;")


def load_all_jobs() -> list[JobPosting]:
    with get_db_connection() as conn:
        with conn.cursor(row_factory=class_row(JobPosting)) as cur:
            cur.execute("SELECT * FROM job_postings;")
            return cur.fetchall()


def fetch_jobs_modified_time() -> list[DictRow]:
    with get_db_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT job_id, last_modified FROM job_postings;")
            return cur.fetchall()


def insert_jobs(jobs: list[JobPosting]) -> None:
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.executemany(INSERT_JOB_SQL, [job.to_db_row() for job in jobs])


def modify_jobs(jobs: list[JobPosting]) -> None:
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.executemany(
                """
                UPDATE job_postings
                SET (
                    job_id,
                    published_at,
                    last_modified,
                    expires,
                    slug,
                    job_title,
                    category_id,
                    contact,
                    work_location,
                    work_start,
                    work_end,
                    hourly_rate,
                    work_hours,
                    job_description,
                    applicant_profile,
                    required_skills,
                    preferred_skills
                ) = (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s, %s, %s
                )
                WHERE job_id = %s;
                """,
                [job.to_db_row() + [job.job_id] for job in jobs]
            )


def delete_jobs(jobs: list[int]) -> None:
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.executemany("DELETE FROM job_postings WHERE job_id = %s;", [[job_id] for job_id in jobs])

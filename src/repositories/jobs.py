from connect import get_db_connection
from models.job import JobPosting
from models.category import JobCategory

def populate_jobs(jobs: list[JobPosting]) -> None:
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.executemany(
                """
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
                """,
                [job.to_db_row() for job in jobs]
            )


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
from psycopg import Connection
from psycopg.rows import dict_row, DictRow, class_row

from student_job_tracker.models.category import JobCategory
from student_job_tracker.models.job import JobPosting


INSERT_JOB_SQL = """
                INSERT INTO job_postings (
                    job_id,
                    published_at,
                    last_modified,
                    expires,
                    slug,
                    job_title,
                    category_id,
                    company_name,
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
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s, %s, %s
                );
                """


def populate_jobs(conn: Connection, jobs: list[JobPosting]) -> None:
    with conn.cursor() as cur:
        cur.executemany(INSERT_JOB_SQL, [job.to_db_row() for job in jobs])


def fetch_jobs_modified_time(conn: Connection) -> list[DictRow]:
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute("SELECT job_id, last_modified FROM job_postings;")
        return cur.fetchall()


def insert_jobs(conn: Connection, jobs: list[JobPosting]) -> None:
    with conn.cursor() as cur:
        cur.executemany(INSERT_JOB_SQL, [job.to_db_row() for job in jobs])


def modify_jobs(conn: Connection, jobs: list[JobPosting]) -> None:
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
                company_name,
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
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s, %s, %s
            )
            WHERE job_id = %s;
            """,
            [job.to_db_row() + [job.job_id] for job in jobs]
        )


def delete_jobs(conn: Connection, jobs: list[int]) -> None:
    with conn.cursor() as cur:
        cur.execute("DELETE FROM job_postings WHERE job_id = ANY(%s);", [jobs])


def truncate_jobs_and_categories(conn: Connection) -> None:
    with conn.cursor() as cur:
        cur.execute("TRUNCATE job_postings, job_categories;")


def populate_categories(conn: Connection, categories: list[JobCategory]) -> None:
    with conn.cursor() as cur:
        cur.executemany(
            "INSERT INTO job_categories (category_id, slug, category_name) VALUES (%s, %s, %s);",
            [category.to_db_row() for category in categories]
        )


def fetch_categories(conn: Connection) -> list[JobCategory]:
    with conn.cursor(row_factory=class_row(JobCategory)) as cur:
        cur.execute("SELECT category_id, slug, category_name FROM job_categories;")
        return cur.fetchall()


def fetch_categories_status(conn: Connection) -> list[DictRow]:
    with conn.cursor(row_factory=dict_row) as cur:
        cur.execute("SELECT category_id, category_name, tracked_status FROM job_categories;")
        return cur.fetchall()


def modify_categories(conn: Connection, categories: list[JobCategory]) -> None:
    with conn.cursor() as cur:
        cur.executemany("UPDATE job_categories SET (slug, category_name) = (%s, %s) WHERE category_id = %s",
                        [[category.slug, category.category_name, category.category_id] for category in categories])


def start_tracking_categories(conn: Connection, category_IDs: list[str]) -> None:
    with conn.cursor() as cur:
        cur.execute("UPDATE job_categories SET tracked_status = true WHERE category_id = ANY(%s);", [category_IDs])


def stop_tracking_categories(conn: Connection, category_IDs: list[str]) -> None:
    with conn.cursor() as cur:
        cur.execute("UPDATE job_categories SET tracked_status = false WHERE category_id = ANY(%s);", [category_IDs])
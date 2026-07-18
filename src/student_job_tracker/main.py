from student_job_tracker.core import db
from student_job_tracker.services import tracker


def main():
    with db.get_connection_pool() as pool:
        tracker.scrape_and_update_jobs(pool)


if __name__ == "__main__":
    main()


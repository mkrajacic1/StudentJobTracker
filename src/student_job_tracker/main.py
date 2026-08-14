from student_job_tracker.core import db
from student_job_tracker.services import tracker
from student_job_tracker.services import api_scraper


def main():
    job_postings, categories = api_scraper.scrape()
    with db.get_connection_pool() as pool:
        tracker.monitor_categories(pool, categories)
        tracker.track_jobs(pool, job_postings)


if __name__ == "__main__":
    main()


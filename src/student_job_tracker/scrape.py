from student_job_tracker.core import db
from student_job_tracker.services import tracker
from student_job_tracker.services import sc_api_scraper


# Main entry point of the program
def main():
    try:
        job_postings, categories = sc_api_scraper.scrape()
        with db.get_connection_pool() as pool:
            tracker.monitor_categories(pool, categories)
            tracker.track_jobs(pool, job_postings)
    except Exception:
        print(Exception)

if __name__ == "__main__":
    main()


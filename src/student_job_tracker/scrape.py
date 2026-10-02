import logging
from logging.handlers import RotatingFileHandler
import os

from student_job_tracker.core import db
from student_job_tracker.core.config import ROOT_DIR
from student_job_tracker.services import tracker
from student_job_tracker.services import sc_api_scraper


logger = logging.getLogger("StudentJobTracker")
logger.setLevel(logging.DEBUG)

logs_file_path = os.path.join(ROOT_DIR, "logs", "scraper.log")
rfh = RotatingFileHandler(
    logs_file_path, 
    maxBytes=1024 * 1024,
    backupCount=3,
    encoding="utf-8"
)
rfh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s %(name)s: %(levelname)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
rfh.setFormatter(formatter)

logger.addHandler(rfh)

# Main entry point of the program
def main():
    try:
        job_postings, categories = sc_api_scraper.scrape()
        with db.get_connection_pool() as pool:
            tracker.monitor_categories(pool, categories)
            tracker.track_jobs(pool, job_postings)
    except sc_api_scraper.ScraperError as exc:
        logger.exception("Scraper error terminated the program")
    else:
        logger.info("Successful job")

if __name__ == "__main__":
    main()


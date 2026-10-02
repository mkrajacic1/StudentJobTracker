import logging
from logging.handlers import RotatingFileHandler
import os

from student_job_tracker.core import db
from student_job_tracker.core.config import ROOT_DIR
from student_job_tracker.services import tracker
from student_job_tracker.services import sc_api_scraper
from student_job_tracker.services import telegram


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
    except sc_api_scraper.ScraperError:
        logger.exception("Scraper error terminated the program")
    except db.ConnectionError:
        logger.exception("Error while trying to create a database connection pool")
    except tracker.DatabaseServiceError:
        logger.exception("Error occurred attempting database operations")
    except tracker.TrackerError:
        logger.exception("Error occurred in the tracker module")
    except telegram.TelegramError:
        logger.exception("Error occurred in the Telegram Bot service")
    except Exception as exc:
        logger.exception("Ambiguous error occurred")
    else:
        try:
            telegram.success_notify()
        except telegram.TelegramError:
            logger.exception("Telegram success message error")
        else:
            logger.info("Successful job")


if __name__ == "__main__":
    main()


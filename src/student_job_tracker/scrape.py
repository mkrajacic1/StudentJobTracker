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
    success = False
    error_message = "Unknown error"
    try:
        job_postings, categories = sc_api_scraper.scrape()
        with db.get_connection_pool() as pool:
            tracker.monitor_categories(pool, categories)
            tracker.track_jobs(pool, job_postings)
    except sc_api_scraper.ScraperError:
        error_message = "Scraper error terminated the program"
        logger.exception(error_message)
    except db.ConnectionError:
        error_message = "Error while trying to create a database connection pool"
        logger.exception(error_message)
    except tracker.DatabaseServiceError:
        error_message = "Error occurred attempting database operations"
        logger.exception(error_message)
    except tracker.TrackerError:
        error_message = "Error occurred in the tracker module"
        logger.exception(error_message)
    except telegram.TelegramError:
        error_message = "Error occurred in the Telegram Bot service"
        logger.exception(error_message)
    except Exception:
        error_message = "Ambiguous error occurred"
        logger.exception(error_message)
    else:
        success = True
    finally:
        try:
            if success:
                telegram.success_notify()
                logger.info("Successful job")
            else:
                telegram.alert_notify(error_message)            
        except telegram.TelegramError:
            logger.exception("Telegram status message error")
            

if __name__ == "__main__":
    main()
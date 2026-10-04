from psycopg import DatabaseError
from psycopg_pool import ConnectionPool, PoolTimeout
import requests

from student_job_tracker.core import db
from student_job_tracker.repositories import jobs
from student_job_tracker.services.sc_api_scraper import scrape_initial_jobs_data, scrape_categories, ScraperError

# CLI interface for managing tracked categories
def track_categories(pool: ConnectionPool) -> None:
    while True:
        with pool.connection() as conn:
            available_categories = jobs.fetch_categories_status(conn)

        longest_name = max(len(category["category_name"]) for category in available_categories)

        print()
        print(f"ID:\t{"Category name:".ljust(longest_name)}\tTracking:")
        for category in available_categories:
            print(f"{category["category_id"]}\t{category["category_name"].ljust(longest_name)}\t{category["tracked_status"]}")
        print()
        print("<------- Command menu ------->")
        print("Start tracking categories - 1")
        print("Stop tracking categories -- 2")
        print("Choose any other key to exit")
        print("<---------------------------->")
        choice = input("Input: ").strip()
        
        match choice:
            case "1":
                start_tracking = input("Choose which categories to track, type category IDs separated by spaces: ").split()
                if start_tracking:
                    with pool.connection() as conn:
                        jobs.start_tracking_categories(conn, start_tracking)
            case "2":
                stop_tracking = input("Choose which categories to stop tracking, type category IDs separated by spaces: ").split()
                if stop_tracking:
                    with pool.connection() as conn:
                        jobs.stop_tracking_categories(conn, stop_tracking)
            case _:
                break


def scrape_and_populate_categories(pool: ConnectionPool) -> None:
    with requests.Session() as se:
        initial_jobs_data = scrape_initial_jobs_data(se)
    all_categories = scrape_categories(initial_jobs_data)

    with pool.connection() as conn:
        jobs.populate_categories(conn, all_categories)


def get_category_count(pool: ConnectionPool) -> int:
    with pool.connection() as conn:
        category_count = jobs.categories_count(conn)
        return category_count


def main():
    print("Welcome to job category management for Student Job Tracker!")
    try:
        with db.get_connection_pool() as pool:
            category_count = get_category_count(pool)

            should_scrape = False
            if not category_count:
                print()
                print("There is currently no job category info in the database.")
                choice = input("Would you like the job categories to be scraped? (y/n): ").strip().lower()
                print()
                if choice == 'y':
                    print("Scraping job categories, please be patient...")
                    should_scrape = True
                else:
                    print("Cannot continue with category management.")
                    return

            if should_scrape:
                scrape_and_populate_categories(pool)
                print("Scraping complete!")
                
            track_categories(pool)
    except (PoolTimeout, DatabaseError):
        print("An error occurred while accessing the database. Aborting...")
    except ScraperError:
        print("An error occurred while scraping job category data. Aborting...")

        
if __name__ == "__main__":
    main()
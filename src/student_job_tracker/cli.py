from psycopg_pool import ConnectionPool

from student_job_tracker.core import db
from student_job_tracker.repositories import jobs
from student_job_tracker.services.tracker import track_categories


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
        print("Stop tracking categories  - 2")
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


def main():
    with db.get_connection_pool() as pool:
        track_categories(pool)


if __name__ == "__main__":
    main()
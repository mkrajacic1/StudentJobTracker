from psycopg_pool import ConnectionPool

from student_job_tracker.core.config import CONN_STRING


class ConnectionError(Exception):
    """Exception class for database connection errors"""


def get_connection_pool() -> ConnectionPool:
    try:
        return ConnectionPool(
            CONN_STRING,
            min_size=1
        )
    except Exception as exc:
        raise ConnectionError("An error occurred trying to create a database connection pool") from exc
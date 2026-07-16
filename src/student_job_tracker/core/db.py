from psycopg_pool import ConnectionPool

from student_job_tracker.core.config import CONN_STRING


def get_connection_pool() -> ConnectionPool:
    return ConnectionPool(
        CONN_STRING,
        min_size=1
    )
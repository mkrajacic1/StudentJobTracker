import pytest

from datetime import datetime

from student_job_tracker.models.category import JobCategory
from student_job_tracker.models.job import JobPosting
from student_job_tracker.services.tracker import find_deleted_jobs, find_new_and_modified_jobs, compare_categories

# tests for find_deleted_jobs()

def test_find_deleted_none():
    snapshot_jobs = [
        {"job_id": 123, "last_modified": datetime(2021, 6, 23, 14, 45, 12)},
        {"job_id": 456, "last_modified": datetime(2022, 7, 23, 14, 45, 12)},
        {"job_id": 789, "last_modified": datetime(2023, 6, 23, 14, 45, 13)}
    ]
    scraped_ids = {123, 456, 789, 200}
    assert find_deleted_jobs(snapshot_jobs, scraped_ids) == []


def test_find_deleted_some():
    snapshot_jobs = [
        {"job_id": 111, "last_modified": datetime(2021, 6, 23, 14, 45, 12)},
        {"job_id": 222, "last_modified": datetime(2022, 7, 23, 14, 45, 12)},
        {"job_id": 333, "last_modified": datetime(2023, 6, 23, 14, 45, 13)}
    ]
    scraped_ids = {111, 500, 600, 800}
    assert find_deleted_jobs(snapshot_jobs, scraped_ids) == [222, 333]


def test_find_deleted_all():
    snapshot_jobs = [
        {"job_id": 111, "last_modified": datetime(2021, 6, 23, 14, 45, 12)},
        {"job_id": 222, "last_modified": datetime(2022, 7, 23, 14, 45, 12)},
        {"job_id": 333, "last_modified": datetime(2023, 6, 23, 14, 45, 13)}
    ]
    scraped_ids = {500, 600, 800, 900}
    assert find_deleted_jobs(snapshot_jobs, scraped_ids) == [111, 222, 333]


# tests for find_new_and_modified_jobs()

def test_find_new_modified_none():
    job_postings = [
        JobPosting(111, datetime(2021, 6, 23, 14, 45, 12), datetime(2021, 6, 23, 14, 45, 22), datetime(2021, 6, 30, 14, 45, 12), "slug1", "Title 1",
                   200, "ABC", "abc@abc.com", "Zagreb", "odmah", "1 godina", "6,56€", "30h tjedno", "opis", "Vještine...", "", ""),
        JobPosting(222, datetime(2022, 6, 23, 14, 45, 12), datetime(2022, 6, 23, 14, 45, 22), datetime(2022, 6, 30, 14, 45, 12), "slug2", "Title 2",
                   201, "ABC", "abc@abc.com", "Zagreb", "odmah", "1 godina", "6,56€", "30h tjedno", "opis", "Vještine...", "", ""),
        JobPosting(333, datetime(2023, 6, 23, 14, 45, 12), datetime(2023, 6, 23, 14, 45, 22), datetime(2023, 6, 30, 14, 45, 12), "slug3", "Title 3",
                   200, "ABC", "abc@abc.com", "Zagreb", "odmah", "1 godina", "6,56€", "30h tjedno", "opis", "Vještine...", "", "")
    ]
    jobs_last_modified = {111: datetime(2021, 6, 23, 14, 45, 22), 222: datetime(2022, 6, 23, 14, 45, 22), 333: datetime(2023, 6, 23, 14, 45, 22)}
    assert find_new_and_modified_jobs(job_postings, jobs_last_modified) == ([], [])


def test_find_new_modified_all_modified():
    first = JobPosting(111, datetime(2021, 6, 26, 14, 45, 12), datetime(2021, 6, 23, 14, 45, 22), datetime(2021, 6, 30, 14, 45, 12), "slug1", "Title 1",
                       200, "ABC", "abc@abc.com", "Zagreb", "odmah", "1 godina", "6,56€", "30h tjedno", "opis", "Vještine...", "", "")
    second = JobPosting(222, datetime(2022, 6, 26, 14, 45, 12), datetime(2022, 6, 23, 14, 45, 22), datetime(2022, 6, 30, 14, 45, 12), "slug2", "Title 2",
                        201, "ABC", "abc@abc.com", "Zagreb", "odmah", "1 godina", "6,56€", "30h tjedno", "opis", "Vještine...", "", "")
    third = JobPosting(333, datetime(2023, 6, 26, 14, 45, 12), datetime(2023, 6, 23, 14, 45, 22), datetime(2023, 6, 30, 14, 45, 12), "slug3", "Title 3",
                       200, "ABC", "abc@abc.com", "Zagreb", "odmah", "1 godina", "6,56€", "30h tjedno", "opis", "Vještine...", "", "")
    fourth = JobPosting(444, datetime(2024, 6, 26, 14, 45, 12), datetime(2024, 6, 23, 14, 45, 22), datetime(2024, 6, 30, 14, 45, 12), "slug3", "Title 3",
                        200, "ABC", "abc@abc.com", "Zagreb", "odmah", "1 godina", "6,56€", "30h tjedno", "opis", "Vještine...", "", "")
    job_postings = [first, second, third, fourth]
    jobs_last_modified = {111: datetime(2021, 6, 25, 14, 45, 22), 222: datetime(2022, 6, 25, 14, 45, 22), 333: datetime(2023, 6, 25, 14, 45, 22)}
    assert find_new_and_modified_jobs(job_postings, jobs_last_modified) == ([fourth], [first, second, third])


# tests for compare_categories()

def test_compare_categories_ID_change():
    scraped_1 = JobCategory(100, "razni-poslovi", "Razni poslovi")
    scraped_2 = JobCategory(200, "skladisni-poslovi", "Skladišni poslovi")
    scraped_3 = JobCategory(300, "it-poslovi", "IT poslovi")
    scraped_categories = [scraped_1, scraped_2, scraped_3]
    db_categories = [
        JobCategory(100, "razni-poslovi", "Razni poslovi"),
        JobCategory(200, "skladisni-poslovi", "Skladišni poslovi"),
        JobCategory(400, "administracija", "Administracija")
    ]
    with pytest.raises(RuntimeError):
        compare_categories(scraped_categories, db_categories)


def test_compare_categories_modified():
    scraped_1 = JobCategory(100, "razni-poslovi", "Razni poslovi")
    scraped_2 = JobCategory(200, "skladisni-poslovi", "Skladišni poslovi")
    scraped_3 = JobCategory(300, "it-poslovi", "IT poslovi")
    scraped_categories = [scraped_1, scraped_2, scraped_3]
    db_categories = [
        JobCategory(100, "razni-poslovi", "Razni poslovi"),
        JobCategory(200, "skladisni-poslovi", "Skladišni poslovi"),
        JobCategory(300, "administracija", "Administracija")
    ]
    assert compare_categories(scraped_categories, db_categories) == [scraped_3]


def test_compare_categories_same():
    scraped_1 = JobCategory(100, "razni-poslovi", "Razni poslovi")
    scraped_2 = JobCategory(200, "skladisni-poslovi", "Skladišni poslovi")
    scraped_3 = JobCategory(300, "it-poslovi", "IT poslovi")
    scraped_categories = [scraped_1, scraped_2, scraped_3]
    db_categories = [
        JobCategory(100, "razni-poslovi", "Razni poslovi"),
        JobCategory(200, "skladisni-poslovi", "Skladišni poslovi"),
        JobCategory(300, "it-poslovi", "IT poslovi")
    ]
    assert compare_categories(scraped_categories, db_categories) == []
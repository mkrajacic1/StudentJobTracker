from repositories import jobs
from api_scraper import scrape_job_data


def populate_jobs_and_categories():
    job_postings, categories = scrape_job_data()
    jobs.populate_categories(categories)
    jobs.populate_jobs(job_postings)


def populate_jobs_table():
    job_postings, _ = scrape_job_data()
    jobs.populate_jobs(job_postings)


def reset_jobs_table():
    jobs.clear_jobs()
    populate_jobs_table()


def resest_jobs_and_categories():
    jobs.clear_jobs_and_categories()
    populate_jobs_and_categories()


def check_for_job_updates():
    job_postings, _ = scrape_job_data()
    scraped_jobs_ids = {job.job_id for job in job_postings}

    jobs_current_db_snapshot = jobs.fetch_jobs_modified_time()
    snapshot_jobs_last_modified = {job["job_id"]: job["last_modified"] for job in jobs_current_db_snapshot}

    print(f"Total jobs: {len(job_postings)}")

    new_jobs, modified_jobs = [], []
    for job in job_postings:
        if job.job_id not in snapshot_jobs_last_modified:
            print(f"New job: {job.job_id}")
            new_jobs.append(job)
        elif job.last_modified != snapshot_jobs_last_modified[job.job_id]:
            print(f"Modified job: {job.job_id}")
            modified_jobs.append(job)
    jobs.insert_jobs(new_jobs)
    jobs.modify_jobs(modified_jobs)

    deleted_jobs = []
    for job in jobs_current_db_snapshot:
        job_id = job["job_id"]
        if job_id not in scraped_jobs_ids:
            print(f"Job {job_id} not available, will be deleted.")
            deleted_jobs.append(job_id)
    jobs.delete_jobs(deleted_jobs)
    

check_for_job_updates()



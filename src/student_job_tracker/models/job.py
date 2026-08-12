from dataclasses import dataclass
from datetime import datetime

@dataclass
class JobPosting:
    job_id: int
    published_at: datetime
    last_modified: datetime
    expires: datetime
    slug: str
    job_title: str
    category_id: int
    company_name: str
    contact: str
    work_location: str
    work_start: str
    work_end: str
    hourly_rate: str
    work_hours: str
    job_description: str
    applicant_profile: str
    required_skills: str
    preferred_skills: str

    def to_db_row(self) -> list:
        return [
            self.job_id,
            self.published_at,
            self.last_modified,
            self.expires,
            self.slug,
            self.job_title,
            self.category_id,
            self.company_name,
            self.contact,
            self.work_location,
            self.work_start,
            self.work_end,
            self.hourly_rate,
            self.work_hours,
            self.job_description,
            self.applicant_profile,
            self.required_skills,
            self.preferred_skills
        ]
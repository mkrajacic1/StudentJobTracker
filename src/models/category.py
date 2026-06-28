from dataclasses import dataclass

@dataclass
class JobCategory:
    category_id: int
    slug: str
    category_name: str

    def to_db_row(self) -> tuple:
        return (
            self.category_id,
            self.slug,
            self.category_name
        )
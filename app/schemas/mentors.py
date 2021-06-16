from pydantic import BaseModel
from typing import List


class ApplicationMentoringSchema(BaseModel):
    mentoring_name: str
    mentoring_description: str = None
    mentoring_fields: List[str]
    capacity: int
    price: int

class ApplicationMentoringResponseSchema(BaseModel):
    pass

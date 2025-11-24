from pydantic import BaseModel
from datetime import datetime

class Review(BaseModel):
    datetime: datetime
    name: str
    rating: int
    comment: str
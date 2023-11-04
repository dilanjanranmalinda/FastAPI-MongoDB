from pydantic import BaseModel
from datetime import datetime

class Task(BaseModel):
    task_id: int
    title: str
    description: str
    status: bool
    created_at: datetime
    updated_at: datetime
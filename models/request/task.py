from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Task(BaseModel):
    title: str
    description: str
    status: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

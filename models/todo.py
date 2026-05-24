from pydantic import BaseModel,Field
from datetime import datetime

class Todo(BaseModel):
    task: str
    done: bool = False
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())


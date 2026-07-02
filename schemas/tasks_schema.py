from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TaskCreateSchema(BaseModel):
    title: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    date_to: Optional[datetime] = None


class TaskSchema(TaskCreateSchema):
    id: int
    done: bool = Field(default=False)
    user_id: int
    created_at: datetime
    date_to: Optional[datetime] = None

    class Config:
        from_attributes = True


class TaskUpdateDoneSchema(BaseModel):
    done: bool


class TaskUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    date_to: Optional[datetime] = None

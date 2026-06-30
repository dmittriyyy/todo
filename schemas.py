from pydantic import BaseModel, Field


class TaskCreateSchema(BaseModel):
    title: str = Field(..., max_length=100)
    description: str = Field(..., max_length=500)


class TaskSchema(TaskCreateSchema):
    id: int
    done: bool = Field(default=False)


class TaskUpdateDoneSchema(BaseModel):
    done: bool


class TaskUpdateSchema(BaseModel):
    title: str = Field(..., max_length=100)
    description: str = Field(..., max_length=500)
    done: bool = Field(default=False)

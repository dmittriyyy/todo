from typing import Optional

from pydantic import BaseModel, Field


class UserCreateSchema(BaseModel):
    name: str = Field(..., max_length=100)
    password: str = Field(..., max_length=100)


class UserResponseSchema(BaseModel):
    id: int
    name: str


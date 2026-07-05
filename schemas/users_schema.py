from typing import Optional

from pydantic import BaseModel, Field
from pydantic.config import ConfigDict


class UserCreateSchema(BaseModel):
    name: str = Field(..., max_length=100)
    password: str = Field(..., max_length=100)
    model_config = ConfigDict(from_attributes=True)


class UserResponseSchema(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)

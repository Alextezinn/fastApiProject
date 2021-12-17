from typing import Optional

from pydantic import BaseModel, Field


class Post(BaseModel):
    id: Optional[int]
    name: str
    subject: str
    content: str
    rating : int = Field(ge=1, le=10)

    class Config:
        orm_mode = True

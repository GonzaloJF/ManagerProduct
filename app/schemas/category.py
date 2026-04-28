from pydantic import BaseModel, Field
from uuid import UUID


class CategoryCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    company_id: UUID | None = None


class CategoryUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    company_id: UUID | None = None


class CategoryResponse(BaseModel):
    id: UUID
    name: str
    company_id: UUID | None

    class Config:
        from_attributes = True

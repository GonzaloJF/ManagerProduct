from pydantic import BaseModel, Field
from uuid import UUID


class CompanyCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)


class CompanyUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)


class CompanyResponse(BaseModel):
    id: UUID
    name: str

    class Config:
        from_attributes = True

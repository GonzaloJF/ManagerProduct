from pydantic import BaseModel, Field
from uuid import UUID


class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    price: float = Field(gt=0)
    stock: int = Field(gt=0)
    company_id: UUID
    category_id: UUID


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    price: float | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, gt=0)
    company_id: UUID | None = None
    category_id: UUID | None = None


class ProductResponse(BaseModel):
    id: UUID
    name: str
    price: float
    stock: int
    company_id: UUID | None
    category_id: UUID | None

    class Config:
        from_attributes = True

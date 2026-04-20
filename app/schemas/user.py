from pydantic import BaseModel, EmailStr, Field
from uuid import UUID

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    company_id: UUID | None = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=3, max_length=50)
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=8, max_length=128)
    company_id: UUID | None = None


class UserResponse(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    company_id: UUID | None

    class Config:
        from_attributes = True
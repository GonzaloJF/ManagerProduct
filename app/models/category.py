import uuid
from sqlalchemy import Column, String, ForeignKey, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)

    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"))

    company = relationship("Company", back_populates="categories")
    products = relationship("Product", back_populates="category")

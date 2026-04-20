import uuid
from sqlalchemy import Column, String, ForeignKey, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)

    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"))
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"))

    created_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="products")
    category = relationship("Category", back_populates="products")
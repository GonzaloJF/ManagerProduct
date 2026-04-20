import uuid
from sqlalchemy import Column, String, ForeignKey, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)

    users = relationship("User", back_populates="company")
    products = relationship("Product", back_populates="company")
    categories = relationship("Category", back_populates="company")

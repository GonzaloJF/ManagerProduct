import uuid
from sqlalchemy import Column, String, ForeignKey, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    email = Column (String, nullable=False, unique=True)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"))

    created_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="users")
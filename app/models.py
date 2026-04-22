import uuid
from sqlalchemy import Column, String, ForeignKey, Float, DateTime, Integer
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


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    email = Column (String, nullable=False, unique=True)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"))

    created_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="users")


class Category(Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)

    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"))

    company = relationship("Company", back_populates="categories")
    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"))
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"))

    created_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("Company", back_populates="products")
    category = relationship("Category", back_populates="products")
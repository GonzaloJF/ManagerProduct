from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.company import Company
from app.models.user import User  # Necesario para la vinculación
from app.schemas.company import CompanyCreate, CompanyUpdate
from uuid import UUID

def get_company_by_id(db: Session, company_id: UUID):
    return db.query(Company).filter(Company.id == company_id).first()

def get_company_by_name(db: Session, name: str):
    return db.query(Company).filter(Company.name == name).first()

def list_companies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Company).offset(skip).limit(limit).all()

def create_company(db: Session, company_create: CompanyCreate, current_user: User):
    # 1. Verificar si el usuario ya tiene una empresa (si quieres limitar a 1)
    if current_user.company_id:
        raise ValueError("USER_ALREADY_HAS_COMPANY")

    # 2. Verificar duplicado de nombre
    if get_company_by_name(db, company_create.name):
        raise ValueError("COMPANY_ALREADY_EXISTS")

    # 3. Crear la empresa
    db_company = Company(**company_create.model_dump())
    db.add(db_company)
    db.flush() # Flush para obtener el ID de la empresa sin terminar la transacción

    # 4. VINCULACIÓN: Asignar la nueva empresa al usuario
    current_user.company_id = db_company.id
    
    db.commit() # Guardamos ambos cambios (Empresa y Usuario)
    db.refresh(db_company)
    return db_company

def update_company(db: Session, db_company: Company, company_update: CompanyUpdate):
    if company_update.name and company_update.name != db_company.name:
        if get_company_by_name(db, company_update.name):
             raise ValueError("COMPANY_ALREADY_EXISTS")
    
    update_data = company_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_company, key, value)

    db.commit()
    db.refresh(db_company)
    return db_company

def delete_company(db: Session, db_company: Company):
    db.delete(db_company)
    db.commit()
    return True
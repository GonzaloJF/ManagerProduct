from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyUpdate
from uuid import UUID

# --- LAS FUNCIONES SE DEFINEN DIRECTAMENTE, NO SE IMPORTAN DE AQUÍ MISMO ---

def get_company_by_id(db: Session, company_id: UUID):
    return db.query(Company).filter(Company.id == company_id).first()

def get_company_by_name(db: Session, name: str):
    return db.query(Company).filter(Company.name == name).first()

def list_companies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Company).offset(skip).limit(limit).all()

def create_company(db: Session, company_create: CompanyCreate):
    # Usamos la función local get_company_by_name
    if get_company_by_name(db, company_create.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de la empresa ya existe"
        )

    db_company = Company(**company_create.model_dump())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

def update_company(db: Session, db_company: Company, company_update: CompanyUpdate):
    if company_update.name and company_update.name != db_company.name:
        if get_company_by_name(db, company_update.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nuevo nombre de la empresa ya está en uso"
            )
    
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
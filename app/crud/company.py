from sqlalchemy.orm import Session
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyUpdate


def get_company_by_id(db: Session, company_id):
    return db.query(Company).filter(Company.id == company_id).first()


def get_company_by_name(db: Session, name: str):
    return db.query(Company).filter(Company.name == name).first()


def list_companies(db: Session):
    return db.query(Company).all()


def create_company(db: Session, company_create: CompanyCreate):
    if get_company_by_name(db, company_create.name):
        raise ValueError("COMPANY_NAME_ALREADY_EXISTS")

    db_company = Company(name=company_create.name)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company


def update_company(db: Session, db_company: Company, company_update: CompanyUpdate):
    if company_update.name and company_update.name != db_company.name:
        if get_company_by_name(db, company_update.name):
            raise ValueError("COMPANY_NAME_ALREADY_EXISTS")
        db_company.name = company_update.name

    db.commit()
    db.refresh(db_company)
    return db_company


def delete_company(db: Session, db_company: Company):
    db.delete(db_company)
    db.commit()

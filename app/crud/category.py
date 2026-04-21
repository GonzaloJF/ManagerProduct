from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.category import Category
from app.models.company import Company  # Importamos el modelo Company para verificar existencia
from app.schemas.category import CategoryCreate, CategoryUpdate
from uuid import UUID

def get_category_by_id(db: Session, category_id: UUID):
    return db.query(Category).filter(Category.id == category_id).first()

def get_category_by_name_and_company(db: Session, name: str, company_id: UUID):
    return db.query(Category).filter(
        Category.name == name, 
        Category.company_id == company_id
    ).first()

def list_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Category).offset(skip).limit(limit).all()

def create_category(db: Session, category_create: CategoryCreate):
    # 1. Verificación de que el company_id fue enviado
    if not category_create.company_id:
        raise ValueError("COMPANY_ID_REQUIRED")

    # 2. Verificación de que la compañía realmente existe en la DB
    db_company = db.query(Company).filter(Company.id == category_create.company_id).first()
    if not db_company:
        raise ValueError("COMPANY_NOT_FOUND")

    # 3. Validamos si ya existe la categoría en esa empresa específica
    if get_category_by_name_and_company(db, category_create.name, category_create.company_id):
        raise ValueError("CATEGORY_ALREADY_EXISTS")
    
    # 4. Creación
    db_category = Category(**category_create.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, db_category: Category, category_update: CategoryUpdate):
    # Si se intenta cambiar el nombre, verificamos que no choque con otra en la misma empresa
    if category_update.name and category_update.name != db_category.name:
        if get_category_by_name_and_company(db, category_update.name, db_category.company_id):
            raise ValueError("CATEGORY_ALREADY_EXISTS")
    
    # Nota: Normalmente no permitimos cambiar el company_id de una categoría ya creada
    # por integridad de datos, por eso solo actualizamos los campos enviados.
    update_data = category_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_category, key, value)

    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, db_category: Category):
    db.delete(db_category)
    db.commit()
    return True
from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.company import Company
from app.models.category import Category
from app.schemas.product import ProductCreate, ProductUpdate
from uuid import UUID

def get_product_by_id(db: Session, product_id: UUID): # Especifica UUID
    return db.query(Product).filter(Product.id == product_id).first()

def list_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()

def create_product(db: Session, product_create: ProductCreate):
    # 1. Verificar existencia de la empresa
    company = db.query(Company).filter(Company.id == product_create.company_id).first()
    if not company:
        raise ValueError("COMPANY_NOT_FOUND")

    # 2. Verificar existencia de la categoría
    category = db.query(Category).filter(Category.id == product_create.category_id).first()
    if not category:
        raise ValueError("CATEGORY_NOT_FOUND")

    # 3. Validación de integridad: ¿La categoría pertenece a la misma empresa?
    if category.company_id != product_create.company_id:
        raise ValueError("CATEGORY_COMPANY_MISMATCH")

    # 4. Creación simplificada con model_dump
    db_product = Product(**product_create.model_dump())
    
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, db_product: Product, product_update: ProductUpdate):
    # Obtenemos los datos que se quieren actualizar
    update_data = product_update.model_dump(exclude_unset=True)

    # Si se intenta cambiar la categoría o la empresa, validamos la relación
    new_company_id = update_data.get("company_id", db_product.company_id)
    new_category_id = update_data.get("category_id", db_product.category_id)

    if "company_id" in update_data or "category_id" in update_data:
        category = db.query(Category).filter(Category.id == new_category_id).first()
        if not category:
            raise ValueError("CATEGORY_NOT_FOUND")
        
        if category.company_id != new_company_id:
            raise ValueError("CATEGORY_COMPANY_MISMATCH")

    # Aplicamos los cambios dinámicamente
    for key, value in update_data.items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, db_product: Product):
    db.delete(db_product)
    db.commit()
    return True
from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.company import Company
from app.models.category import Category
from app.schemas.product import ProductCreate, ProductUpdate


def get_product_by_id(db: Session, product_id):
    return db.query(Product).filter(Product.id == product_id).first()


def list_products(db: Session):
    return db.query(Product).all()


def create_product(db: Session, product_create: ProductCreate):
    company = db.query(Company).filter(Company.id == product_create.company_id).first()
    if not company:
        raise ValueError("COMPANY_NOT_FOUND")

    category = db.query(Category).filter(Category.id == product_create.category_id).first()
    if not category:
        raise ValueError("CATEGORY_NOT_FOUND")

    if category.company_id != product_create.company_id:
        raise ValueError("CATEGORY_COMPANY_MISMATCH")

    db_product = Product(
        name=product_create.name,
        price=product_create.price,
        company_id=product_create.company_id,
        category_id=product_create.category_id,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(db: Session, db_product: Product, product_update: ProductUpdate):
    target_company_id = product_update.company_id if product_update.company_id is not None else db_product.company_id
    target_category_id = product_update.category_id if product_update.category_id is not None else db_product.category_id

    company = db.query(Company).filter(Company.id == target_company_id).first()
    if not company:
        raise ValueError("COMPANY_NOT_FOUND")

    category = db.query(Category).filter(Category.id == target_category_id).first()
    if not category:
        raise ValueError("CATEGORY_NOT_FOUND")

    if category.company_id != target_company_id:
        raise ValueError("CATEGORY_COMPANY_MISMATCH")

    if product_update.name:
        db_product.name = product_update.name
    if product_update.price is not None:
        db_product.price = product_update.price
    if product_update.company_id is not None:
        db_product.company_id = product_update.company_id
    if product_update.category_id is not None:
        db_product.category_id = product_update.category_id

    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, db_product: Product):
    db.delete(db_product)
    db.commit()

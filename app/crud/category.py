from sqlalchemy.orm import Session
from app.models.category import Category
from app.models.company import Company
from app.schemas.category import CategoryCreate, CategoryUpdate


def get_category_by_id(db: Session, category_id):
    return db.query(Category).filter(Category.id == category_id).first()


def get_category_by_name_and_company(db: Session, name: str, company_id):
    return (
        db.query(Category)
        .filter(Category.name == name, Category.company_id == company_id)
        .first()
    )


def list_categories(db: Session):
    return db.query(Category).all()


def create_category(db: Session, category_create: CategoryCreate):
    company = db.query(Company).filter(Company.id == category_create.company_id).first()
    if not company:
        raise ValueError("COMPANY_NOT_FOUND")
    if get_category_by_name_and_company(db, category_create.name, category_create.company_id):
        raise ValueError("CATEGORY_ALREADY_EXISTS")

    db_category = Category(
        name=category_create.name,
        company_id=category_create.company_id,
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def update_category(db: Session, db_category: Category, category_update: CategoryUpdate):
    target_company_id = db_category.company_id
    if category_update.company_id is not None:
        company = db.query(Company).filter(Company.id == category_update.company_id).first()
        if not company:
            raise ValueError("COMPANY_NOT_FOUND")
        target_company_id = category_update.company_id

    target_name = category_update.name if category_update.name else db_category.name
    existing = get_category_by_name_and_company(db, target_name, target_company_id)
    if existing and existing.id != db_category.id:
        raise ValueError("CATEGORY_ALREADY_EXISTS")

    if category_update.name:
        db_category.name = category_update.name
    if category_update.company_id is not None:
        db_category.company_id = category_update.company_id

    db.commit()
    db.refresh(db_category)
    return db_category


def delete_category(db: Session, db_category: Category):
    db.delete(db_category)
    db.commit()

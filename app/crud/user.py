from sqlalchemy.orm import Session
from app.models.user import User
from app.models.company import Company
from app.core.security import hash_password
from app.schemas.user import UserCreate, UserUpdate


def get_user_by_id(db: Session, user_id):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def list_users(db: Session):
    return db.query(User).all()


def create_user(db: Session, user_create: UserCreate):
    if get_user_by_email(db, user_create.email):
        raise ValueError("EMAIL_ALREADY_EXISTS")
    if get_user_by_username(db, user_create.username):
        raise ValueError("USERNAME_ALREADY_EXISTS")
    if user_create.company_id:
        company = db.query(Company).filter(Company.id == user_create.company_id).first()
        if not company:
            raise ValueError("COMPANY_NOT_FOUND")

    db_user = User(
        username=user_create.username,
        email=user_create.email,
        password=hash_password(user_create.password),
        company_id=user_create.company_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, db_user: User, user_update: UserUpdate):
    if user_update.email and user_update.email != db_user.email:
        if get_user_by_email(db, user_update.email):
            raise ValueError("EMAIL_ALREADY_EXISTS")
        db_user.email = user_update.email

    if user_update.username and user_update.username != db_user.username:
        if get_user_by_username(db, user_update.username):
            raise ValueError("USERNAME_ALREADY_EXISTS")
        db_user.username = user_update.username

    if user_update.password:
        db_user.password = hash_password(user_update.password)

    if user_update.company_id is not None:
        if user_update.company_id:
            company = db.query(Company).filter(Company.id == user_update.company_id).first()
            if not company:
                raise ValueError("COMPANY_NOT_FOUND")
        db_user.company_id = user_update.company_id

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, db_user: User):
    db.delete(db_user)
    db.commit()
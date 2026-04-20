from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.crud.user import (
    create_user,
    list_users,
    get_user_by_id,
    update_user,
    delete_user,
)
from app.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return create_user(db, user)
    except ValueError as exc:
        mapping = {
            "EMAIL_ALREADY_EXISTS": "Ya existe un usuario con ese email",
            "USERNAME_ALREADY_EXISTS": "Ya existe un usuario con ese username",
            "COMPANY_NOT_FOUND": "La empresa indicada no existe",
        }
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=mapping.get(str(exc), str(exc)))


@router.get("/", response_model=list[UserResponse])
def get_all(db: Session = Depends(get_db)):
    return list_users(db)


@router.get("/{user_id}", response_model=UserResponse)
def get_one(user_id: UUID, db: Session = Depends(get_db)):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return db_user


@router.put("/{user_id}", response_model=UserResponse)
def update_one(user_id: UUID, user_update_payload: UserUpdate, db: Session = Depends(get_db)):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    try:
        return update_user(db, db_user, user_update_payload)
    except ValueError as exc:
        mapping = {
            "EMAIL_ALREADY_EXISTS": "Ya existe un usuario con ese email",
            "USERNAME_ALREADY_EXISTS": "Ya existe un usuario con ese username",
            "COMPANY_NOT_FOUND": "La empresa indicada no existe",
        }
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=mapping.get(str(exc), str(exc)))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_one(user_id: UUID, db: Session = Depends(get_db)):
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    delete_user(db, db_user)
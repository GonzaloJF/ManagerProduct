from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
from app.crud.category import (
    create_category,
    list_categories,
    get_category_by_id,
    update_category,
    delete_category,
)

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create(category: CategoryCreate, db: Session = Depends(get_db)):
    try:
        return create_category(db, category)
    except ValueError as exc:
        mapping = {
            "COMPANY_NOT_FOUND": "La empresa indicada no existe",
            "CATEGORY_ALREADY_EXISTS": "Ya existe una categoria con ese nombre para esa empresa",
        }
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=mapping.get(str(exc), str(exc)))


@router.get("/", response_model=list[CategoryResponse])
def get_all(db: Session = Depends(get_db)):
    return list_categories(db)


@router.get("/{category_id}", response_model=CategoryResponse)
def get_one(category_id: UUID, db: Session = Depends(get_db)):
    db_category = get_category_by_id(db, category_id)
    if not db_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria no encontrada")
    return db_category


@router.put("/{category_id}", response_model=CategoryResponse)
def update_one(category_id: UUID, category_update_payload: CategoryUpdate, db: Session = Depends(get_db)):
    db_category = get_category_by_id(db, category_id)
    if not db_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria no encontrada")
    try:
        return update_category(db, db_category, category_update_payload)
    except ValueError as exc:
        mapping = {
            "COMPANY_NOT_FOUND": "La empresa indicada no existe",
            "CATEGORY_ALREADY_EXISTS": "Ya existe una categoria con ese nombre para esa empresa",
        }
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=mapping.get(str(exc), str(exc)))


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_one(category_id: UUID, db: Session = Depends(get_db)):
    db_category = get_category_by_id(db, category_id)
    if not db_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria no encontrada")
    delete_category(db, db_category)

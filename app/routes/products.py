from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.crud.product import (
    create_product,
    list_products,
    get_product_by_id,
    update_product,
    delete_product,
)

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create(product: ProductCreate, db: Session = Depends(get_db)):
    try:
        return create_product(db, product)
    except ValueError as exc:
        mapping = {
            "COMPANY_NOT_FOUND": "La empresa indicada no existe",
            "CATEGORY_NOT_FOUND": "La categoria indicada no existe",
            "CATEGORY_COMPANY_MISMATCH": "La categoria no pertenece a la empresa indicada",
        }
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=mapping.get(str(exc), str(exc)))


@router.get("/", response_model=list[ProductResponse])
def get_all(db: Session = Depends(get_db)):
    return list_products(db)


@router.get("/{product_id}", response_model=ProductResponse)
def get_one(product_id: UUID, db: Session = Depends(get_db)):
    db_product = get_product_by_id(db, product_id)
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return db_product


@router.put("/{product_id}", response_model=ProductResponse)
def update_one(product_id: UUID, product_update_payload: ProductUpdate, db: Session = Depends(get_db)):
    db_product = get_product_by_id(db, product_id)
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    try:
        return update_product(db, db_product, product_update_payload)
    except ValueError as exc:
        mapping = {
            "COMPANY_NOT_FOUND": "La empresa indicada no existe",
            "CATEGORY_NOT_FOUND": "La categoria indicada no existe",
            "CATEGORY_COMPANY_MISMATCH": "La categoria no pertenece a la empresa indicada",
        }
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=mapping.get(str(exc), str(exc)))


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_one(product_id: UUID, db: Session = Depends(get_db)):
    db_product = get_product_by_id(db, product_id)
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    delete_product(db, db_product)

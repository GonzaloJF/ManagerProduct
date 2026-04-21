from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.models.user import User
from app.service.auth_service import get_current_user
from app.crud.product import (
    create_product,
    list_products,
    get_product_by_id,
    update_product,
    delete_product,
)

router = APIRouter(prefix="/products", tags=["Products"])

# Función auxiliar para errores limpia
def handle_product_error(exc: ValueError):
    mapping = {
        "COMPANY_NOT_FOUND": "La empresa indicada no existe",
        "CATEGORY_NOT_FOUND": "La categoría indicada no existe",
        "CATEGORY_COMPANY_MISMATCH": "La categoría no pertenece a tu empresa",
    }
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT, 
        detail=mapping.get(str(exc), str(exc))
    )

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create(
    product: ProductCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # ASIGNACIÓN AUTOMÁTICA: Forzamos la empresa del usuario logueado
    product.company_id = current_user.company_id
    
    try:
        return create_product(db, product)
    except ValueError as exc:
        handle_product_error(exc)

@router.get("/", response_model=list[ProductResponse])
def get_all(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # OPCIONAL: Filtrar para que solo vea productos de su empresa
    # return db.query(Product).filter(Product.company_id == current_user.company_id).all()
    return list_products(db)

@router.get("/{product_id}", response_model=ProductResponse)
def get_one(
    product_id: UUID, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_product = get_product_by_id(db, product_id)
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    
    # SEGURIDAD: Verificar que el producto sea de su empresa
    if db_product.company_id != current_user.company_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes acceso a este producto")
        
    return db_product

@router.put("/{product_id}", response_model=ProductResponse)
def update_one(
    product_id: UUID, 
    product_update_payload: ProductUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_product = get_product_by_id(db, product_id)
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    
    # SEGURIDAD: Solo puede editar si es de su empresa
    if db_product.company_id != current_user.company_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso para editar este producto")

    # Aseguramos que no intente cambiar el producto a otra empresa mediante el payload
    if product_update_payload.company_id:
        product_update_payload.company_id = current_user.company_id

    try:
        return update_product(db, db_product, product_update_payload)
    except ValueError as exc:
        handle_product_error(exc)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_one(
    product_id: UUID, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_product = get_product_by_id(db, product_id)
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    
    # SEGURIDAD: Solo puede borrar si es de su empresa
    if db_product.company_id != current_user.company_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso para eliminar este producto")

    delete_product(db, db_product)
    return None
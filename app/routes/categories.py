from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
from app.models.user import User
from app.service.auth_service import get_current_user
from app.crud.category import (
    create_category,
    list_categories,
    get_category_by_id,
    update_category,
    delete_category,
)

router = APIRouter(prefix="/categories", tags=["Categories"])

def handle_category_error(exc: ValueError):
    mapping = {
        "COMPANY_ID_REQUIRED": "El ID de la empresa es obligatorio",
        "COMPANY_NOT_FOUND": "La empresa indicada no existe",
        "CATEGORY_ALREADY_EXISTS": "Ya existe una categoría con ese nombre para esa empresa",
    }
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail=mapping.get(str(exc), str(exc))
    )

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create(
    category: CategoryCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # ASIGNACIÓN AUTOMÁTICA: 
    # Forzamos que la categoría pertenezca a la empresa del usuario logueado.
    # Esto soluciona el error de permisos y evita errores de transcripción de UUIDs.
    category.company_id = current_user.company_id

    try:
        return create_category(db, category)
    except ValueError as exc:
        handle_category_error(exc)

@router.get("/", response_model=list[CategoryResponse])
def get_all(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Opcional: Si quieres que el usuario solo vea las categorías de SU empresa:
    # return db.query(Category).filter(Category.company_id == current_user.company_id).all()
    return list_categories(db)

@router.get("/{category_id}", response_model=CategoryResponse)
def get_one(
    category_id: UUID, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_category = get_category_by_id(db, category_id)
    if not db_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    
    # Seguridad: Verificar que la categoría pertenezca a la empresa del usuario
    if db_category.company_id != current_user.company_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado a este recurso")
        
    return db_category

@router.put("/{category_id}", response_model=CategoryResponse)
def update_one(
    category_id: UUID, 
    category_update_payload: CategoryUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_category = get_category_by_id(db, category_id)
    if not db_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    
    # Seguridad: Solo puede editar si pertenece a su empresa
    if db_category.company_id != current_user.company_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permisos para modificar esta categoría")

    try:
        return update_category(db, db_category, category_update_payload)
    except ValueError as exc:
        handle_category_error(exc)

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_one(
    category_id: UUID, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_category = get_category_by_id(db, category_id)
    if not db_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    
    # Seguridad: Solo puede borrar si pertenece a su empresa
    if db_category.company_id != current_user.company_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permisos para eliminar esta categoría")

    delete_category(db, db_category)
    return None
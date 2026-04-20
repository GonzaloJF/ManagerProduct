from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.company import CompanyCreate, CompanyResponse, CompanyUpdate
from app.models.user import User # Importamos el modelo User
from app.service.auth_service import get_current_user # Función que valida el token
from app.crud.company import (
    create_company,
    list_companies,
    get_company_by_id,
    update_company,
    delete_company,
)

router = APIRouter(prefix="/companies", tags=["Companies"])

# Agregamos la dependencia a nivel de ruta para que 'current_user' esté disponible
@router.post("/", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
def create(
    company: CompanyCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # <--- Usuario autenticado
):
    try:
        return create_company(db, company)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@router.get("/", response_model=list[CompanyResponse])
def get_all(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # Protegido
):
    return list_companies(db)


@router.get("/{company_id}", response_model=CompanyResponse)
def get_one(
    company_id: UUID, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # Protegido
):
    db_company = get_company_by_id(db, company_id)
    if not db_company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa no encontrada")
    return db_company


@router.put("/{company_id}", response_model=CompanyResponse)
def update_one(
    company_id: UUID, 
    company_update_payload: CompanyUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # Protegido
):
    db_company = get_company_by_id(db, company_id)
    if not db_company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa no encontrada")
    try:
        return update_company(db, db_company, company_update_payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_one(
    company_id: UUID, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # Protegido
):
    db_company = get_company_by_id(db, company_id)
    if not db_company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa no encontrada")
    delete_company(db, db_company)
    return None
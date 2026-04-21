from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.company import CompanyCreate, CompanyResponse, CompanyUpdate
from app.models.user import User
from app.service.auth_service import get_current_user
from app.crud.company import (
    create_company,
    list_companies,
    get_company_by_id,
    update_company,
    delete_company,
)

router = APIRouter(prefix="/companies", tags=["Companies"])

def handle_company_error(exc: ValueError):
    mapping = {
        "USER_ALREADY_HAS_COMPANY": "Este usuario ya tiene una empresa asignada",
        "COMPANY_ALREADY_EXISTS": "El nombre de la empresa ya está en uso",
    }
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT, 
        detail=mapping.get(str(exc), str(exc))
    )

@router.post("/", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
def create(
    company: CompanyCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # Pasamos el current_user para que el CRUD haga la vinculación
        return create_company(db, company, current_user)
    except ValueError as exc:
        handle_company_error(exc)

@router.get("/", response_model=list[CompanyResponse])
def get_all(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
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
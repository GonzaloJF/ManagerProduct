from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.routes.users import router as users_router
from app.routes.companies import router as companies_router
from app.routes.categories import router as categories_router
from app.routes.products import router as products_router
from app.routes.auth import router as auth_router
from app.database import get_db

app = FastAPI()

app.include_router(users_router)
app.include_router(companies_router)
app.include_router(categories_router)
app.include_router(products_router)
app.include_router(auth_router)

#### health route
@app.get("/")
async def status_api(db: Session = Depends(get_db)):
    return {"status": "200 ok"}
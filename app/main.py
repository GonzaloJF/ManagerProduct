from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.users import router as users_router
from app.routes.companies import router as companies_router
from app.routes.categories import router as categories_router
from app.routes.products import router as products_router
from app.routes.auth import router as auth_router

from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(users_router)
app.include_router(companies_router)
app.include_router(categories_router)
app.include_router(products_router)
app.include_router(auth_router)


@app.get("/")
async def status_api():
    return {"status": "200 ok"}

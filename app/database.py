import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#Cargar variables del .env
load_dotenv()

#Obtener la url de la base de datos 
DATABASE_URL = os.getenv("DATABASE_URL")

#Crear el engine (conexión)
engine = create_engine(DATABASE_URL)

# Crear Sesiones 
sessionslocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base para modelos
Base = declarative_base()

def get_db():
    db = sessionslocal()
    try:
        yield db
    finally: 
        db.close()

        
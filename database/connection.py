
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from config import settings


# Verificar que exista la URL de conexión
if not settings.DATABASE_URL:
    raise ValueError(
        "No se encontró DATABASE_URL en el archivo .env"
    )


# Motor principal de conexión
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=False
)


# Fábrica de sesiones
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


# Clase base para los modelos ORM
class Base(DeclarativeBase):
    pass


# Función para obtener una sesión de base de datos
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

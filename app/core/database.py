from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings  # Asegúrate de tener la configuración del .env
from sqlalchemy.orm import declarative_base

# Definir el base para los modelos
Base = declarative_base()

# Crear el motor de la base de datos usando la URL de configuración
DATABASE_URL = settings.DATABASE_URL  # Carga la URL de la base de datos desde la configuración

# Crear el motor asíncrono para SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True)

# Crear la sesión de SQLAlchemy
# `async_sessionmaker` para crear sesiones asíncronas
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,  # Usamos AsyncSession para operaciones asíncronas
    expire_on_commit=False  # Evita que las instancias sean marcadas como expiradas después de cada commit
)

# Función para obtener la sesión de la base de datos
async def get_db():
    async with SessionLocal() as session:
        yield session

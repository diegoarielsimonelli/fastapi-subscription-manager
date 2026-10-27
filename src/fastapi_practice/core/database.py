import os
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

### En producción leeríamos esto de las variables de entorno (.env)

### Usamos una base de datos SQLite asincrónica local para el entorno de desarrollo rápido

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./suscripciones.db")

engine = create_async_engine(
DATABASE_URL,
echo=True,
connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

AsyncSessionLocal = async_sessionmaker(
bind=engine,
autocommit=False,
autoflush=False,
expire_on_commit=False
)

class Base(DeclarativeBase):
    pass

async def init_db() -> None:
    """Crea las tablas en la base de datos si no existen."""
    async with engine.begin() as conn:
     await conn.run_sync(Base.metadata.create_all)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency injection para las sesiones de la base de datos por petición."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
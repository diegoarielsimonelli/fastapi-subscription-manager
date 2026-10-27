from contextlib import asynccontextmanager
from fastapi import FastAPI

from .core.database import init_db
from .core.excepciones import CustomAppException, custom_exception_handler
from .api.router import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):

### Evento de inicio: Levanta la base de datos de manera automatizada

    await init_db()
    yield
# Eventos de apagado del servidor si fuesen necesarios van acá 

app = FastAPI(
title="Gestión de Suscripciones API",
description="Estructura limpia orientada al dominio y optimizada para producción.",
version="1.0.0",
lifespan=lifespan
)

### Registramos el manejador global de errores personalizados

app.add_exception_handler(CustomAppException, custom_exception_handler)

### Adjuntamos el ruteador versionado de la aplicación

app.include_router(api_router, prefix="/api/v1")
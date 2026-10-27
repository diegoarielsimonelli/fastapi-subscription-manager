from fastapi import APIRouter
from .v1.endpoints.suscripciones import router as suscripciones_router

api_router = APIRouter()

### Agrupamos todos los submódulos bajo el prefijo v1

api_router.include_router(suscripciones_router, prefix="/suscripciones", tags=["Suscripciones"])
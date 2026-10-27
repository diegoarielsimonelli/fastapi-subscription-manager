from fastapi import Request, status
from fastapi.responses import JSONResponse

class CustomAppException(Exception):
    """Clase base para excepciones personalizadas del negocio."""
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.detail = detail
        self.status_code = status_code

class EntityNotFoundException(CustomAppException):
    """Se ejecuta cuando no se encuentra un registro en la base de datos."""
    def __init__(self, entity_name: str, entity_id: int | str):
        super().__init__(
        detail=f"{entity_name} con identificador {entity_id} no fue encontrado/a.",
        status_code=status.HTTP_404_NOT_FOUND
        )

async def custom_exception_handler(request: Request, exc: CustomAppException) -> JSONResponse:
    """Manejador global para capturar errores de negocio y devolver respuestas limpias."""
    return JSONResponse(
    status_code=exc.status_code,
    content={"status": "error", "message": exc.detail}
    )
from pydantic import BaseModel, Field, EmailStr

class SuscripcionBase(BaseModel):
    plan_name: str = Field(..., min_length=3, max_length=50, description="Nombre del plan contratado")
    price: float = Field(..., gt=0, description="El costo del plan debe ser mayor a cero")
    user_email: EmailStr = Field(..., description="Correo electrónico del suscriptor válido")

class SuscripcionCreate(SuscripcionBase):
    pass

class SuscripcionUpdate(BaseModel):
    plan_name: str | None = Field(None, min_length=3, max_length=50)
    price: float | None = Field(None, gt=0)
    is_active: bool | None = Field(None)

class SuscripcionResponse(SuscripcionBase):
    id: int
    is_active: bool

class ConfigDict:
    from_attributes = True
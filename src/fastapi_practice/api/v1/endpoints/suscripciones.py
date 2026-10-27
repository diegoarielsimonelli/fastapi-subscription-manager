from fastapi import APIRouter, Depends, status,Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ....core.database import get_db
from ....core.excepciones import EntityNotFoundException
from ....models.suscripcion import Suscripcion
from ....schemas.suscripcion import SuscripcionCreate, SuscripcionResponse, SuscripcionUpdate


router = APIRouter()


@router.post("/", response_model=SuscripcionResponse, status_code=status.HTTP_201_CREATED)
async def create_suscripcion(payload: SuscripcionCreate, db: AsyncSession = Depends(get_db)):
    nueva_sub = Suscripcion(**payload.model_dump())
    db.add(nueva_sub)
    await db.commit()
    await db.refresh(nueva_sub)
    return nueva_sub

@router.get("/{suscripcion_id}", response_model=SuscripcionResponse)
async def get_suscripcion(suscripcion_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Suscripcion).where(Suscripcion.id == suscripcion_id))
    suscripcion = result.scalars().first()
    if not suscripcion:
        raise EntityNotFoundException(entity_name="Suscripción", entity_id=suscripcion_id)
    return suscripcion

@router.patch("/{suscripcion_id}", response_model=SuscripcionResponse)
async def update_suscripcion(suscripcion_id: int, payload: SuscripcionUpdate, db: AsyncSession = Depends(get_db)):
    """Actualiza campos específicos de una suscripción de forma asincrónica."""
    result = await db.execute(select(Suscripcion).where(Suscripcion.id == suscripcion_id))
    suscripcion = result.scalars().first()
    
    if not suscripcion:
        raise EntityNotFoundException(entity_name="Suscripción", entity_id=suscripcion_id)
    
    # Filtrar solo los campos que el usuario envió en el JSON
    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(suscripcion, key, value)
        
    await db.commit()
    await db.refresh(suscripcion)
    return suscripcion


@router.delete("/{suscripcion_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_suscripcion(suscripcion_id: int, db: AsyncSession = Depends(get_db)):
    """Elimina una suscripción de la base de datos."""
    result = await db.execute(select(Suscripcion).where(Suscripcion.id == suscripcion_id))
    suscripcion = result.scalars().first()
    
    if not suscripcion:
        raise EntityNotFoundException(entity_name="Suscripción", entity_id=suscripcion_id)
        
    await db.delete(suscripcion)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

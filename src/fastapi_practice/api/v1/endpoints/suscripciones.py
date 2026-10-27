from fastapi import APIRouter, Depends, status,Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import time
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










@router.get("/reporte-lento/resumen")
async def get_reporte_lento(db: AsyncSession = Depends(get_db)):
    """
    Simulación de cuello de botella: 
    Usa 'time.sleep' bloqueando el event loop y hace consultas ineficientes.
    """
    result = await db.execute(select(Suscripcion))
    suscripciones = result.scalars().all()
    
    reporte = []
    for sub in suscripciones:
        # SIMULACIÓN DE PROBLEMA REAl: 
        # Imaginá que por cada suscripción, el código frena para hacer un cálculo pesado síncrono
        time.sleep(0.5) # ❌ ¡ERROR CRÍTICO! Bloquea todo el servidor por 500ms por cada registro
        
        reporte.append({
            "email": sub.user_email,
            "plan": sub.plan_name,
            "precio_con_impuesto": sub.price * 1.21
        })
        
    return {"total_procesado": len(reporte), "datos": reporte}
import asyncio # <--- La alternativa asíncrona correcta
from sqlalchemy import func

@router.get("/reporte-rapido/resumen")
async def get_reporte_optimizado(db: AsyncSession = Depends(get_db)):
    """
    Solución al cuello de botella:
    1. Usamos asyncio.sleep si requerimos esperas (no bloquea el event loop).
    2. Si es posible, dejamos que la base de datos calcule los datos en una sola consulta compacta.
    """
    # Dejamos que la base de datos multiplique el impuesto directamente en el motor SQL (Mucho más rápido)
    # select user_email, plan_name, price * 1.21 ...
    query = select(
        Suscripcion.user_email,
        Suscripcion.plan_name,
        (Suscripcion.price * 1.21).label("precio_con_impuesto")
    )
    
    result = await db.execute(query)
    reporte_db = result.all() # Trae los resultados formateados en un solo viaje
    
    # Si de verdad requiriéramos procesar algo de forma asíncrona:
    # await asyncio.sleep(0.01) # Non-blocking
    
    datos = [
        {"email": r.user_email, "plan": r.plan_name, "precio_con_impuesto": r.precio_con_impuesto}
        for r in reporte_db
    ]
    
    return {"total_procesado": len(datos), "datos": datos}

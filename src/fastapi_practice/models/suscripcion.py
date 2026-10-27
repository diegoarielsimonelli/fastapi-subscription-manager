

from sqlalchemy import String, Integer, Boolean, Float
from sqlalchemy.orm import Mapped, mapped_column
from ..core.database import Base

class Suscripcion(Base):
    __tablename__= "suscripciones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    plan_name: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    user_email: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
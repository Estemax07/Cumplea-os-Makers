from sqlalchemy import Column, Date, DateTime, Integer, String, func

from .database import Base


class Persona(Base):
    """
    Modelo de datos pedido por el frontend.
    IMPORTANTE: la edad NUNCA se guarda como columna. Se calcula al vuelo
    a partir de fecha_nacimiento y se expone como "edad_actual" en los
    schemas de salida (ver app/schemas.py).
    """

    __tablename__ = "personas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    hobbies = Column(String, nullable=True, default="")
    foto_url = Column(String, nullable=True, default=None)


class Usuario(Base):
    """Usuario simple para login/registro (no confundir con Persona)."""

    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())

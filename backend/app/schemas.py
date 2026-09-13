from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr, model_validator

from .date_utils import calcular_edad


class PersonaOut(BaseModel):
    """
    Forma exacta que espera el frontend (ver src/components/PersonDetailModal.jsx
    y src/api.js): id, nombre, fecha_nacimiento, hobbies, foto_url, edad_actual.
    edad_actual se calcula siempre acá, nunca se guarda en la base.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    fecha_nacimiento: date
    hobbies: str | None = ""
    foto_url: str | None = None
    edad_actual: int | None = None

    @model_validator(mode="after")
    def _computar_edad(self):
        # Se recalcula siempre, ignorando cualquier valor recibido, para
        # garantizar que edad_actual nunca se "guarde" ni quede desactualizada.
        self.edad_actual = calcular_edad(self.fecha_nacimiento)
        return self


class PersonaProximoOut(BaseModel):
    """Respuesta de GET /personas/proximo."""

    persona: PersonaOut | None = None
    dias_faltantes: int | None = None


# ---------- Auth ----------

class UsuarioCreate(BaseModel):
    email: EmailStr
    password: str


class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str


class UsuarioOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioOut

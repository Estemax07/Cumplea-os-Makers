import os
import uuid
from datetime import date

from fastapi import UploadFile
from sqlalchemy.orm import Session

from . import models
from .config import settings
from .date_utils import dias_hasta_proximo_cumple, es_hoy, es_manana
from .security import hash_password, verificar_password

EXTENSIONES_PERMITIDAS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}


# ---------- Personas ----------

def get_personas(db: Session) -> list[models.Persona]:
    return db.query(models.Persona).order_by(models.Persona.nombre.asc()).all()


def get_persona(db: Session, persona_id: int) -> models.Persona | None:
    return db.query(models.Persona).filter(models.Persona.id == persona_id).first()


def guardar_foto(foto: UploadFile | None) -> str | None:
    """Guarda la foto en UPLOAD_DIR y devuelve la URL relativa (foto_url)."""
    if foto is None or not foto.filename:
        return None

    ext = os.path.splitext(foto.filename)[1].lower()
    if ext not in EXTENSIONES_PERMITIDAS:
        ext = ".jpg"

    nombre_archivo = f"{uuid.uuid4().hex}{ext}"
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    ruta_destino = os.path.join(settings.UPLOAD_DIR, nombre_archivo)

    with open(ruta_destino, "wb") as f:
        f.write(foto.file.read())

    return f"{settings.UPLOAD_URL_PREFIX}/{nombre_archivo}"


def crear_persona(
    db: Session,
    nombre: str,
    fecha_nacimiento: date,
    hobbies: str,
    foto: UploadFile | None,
) -> models.Persona:
    foto_url = guardar_foto(foto)
    persona = models.Persona(
        nombre=nombre,
        fecha_nacimiento=fecha_nacimiento,
        hobbies=hobbies or "",
        foto_url=foto_url,
    )
    db.add(persona)
    db.commit()
    db.refresh(persona)
    return persona


def eliminar_persona(db: Session, persona_id: int) -> models.Persona | None:
    persona = get_persona(db, persona_id)
    if persona is None:
        return None

    # Borramos también el archivo de foto si es local (no una URL externa)
    if persona.foto_url and persona.foto_url.startswith(settings.UPLOAD_URL_PREFIX):
        nombre_archivo = persona.foto_url.split("/")[-1]
        ruta = os.path.join(settings.UPLOAD_DIR, nombre_archivo)
        if os.path.exists(ruta):
            try:
                os.remove(ruta)
            except OSError:
                pass

    db.delete(persona)
    db.commit()
    return persona


def get_personas_que_cumplen_hoy(db: Session) -> list[models.Persona]:
    hoy = date.today()
    return [p for p in get_personas(db) if es_hoy(p.fecha_nacimiento, hoy)]


def get_personas_que_cumplen_manana(db: Session) -> list[models.Persona]:
    hoy = date.today()
    return [p for p in get_personas(db) if es_manana(p.fecha_nacimiento, hoy)]


def get_proximo_cumpleanios(db: Session) -> tuple[models.Persona | None, int | None]:
    """
    Devuelve (persona, dias_faltantes) de la próxima persona en cumplir años
    (puede ser hoy mismo, con dias_faltantes=0, si nadie más está más cerca).
    Si hay empate, se desempata por nombre para que la respuesta sea estable.
    """
    hoy = date.today()
    personas = get_personas(db)
    if not personas:
        return None, None

    con_dias = [(p, dias_hasta_proximo_cumple(p.fecha_nacimiento, hoy)) for p in personas]
    con_dias.sort(key=lambda tup: (tup[1], tup[0].nombre.lower()))
    return con_dias[0]


# ---------- Usuarios ----------

def get_usuario_por_email(db: Session, email: str) -> models.Usuario | None:
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()


def crear_usuario(db: Session, email: str, password: str) -> models.Usuario:
    usuario = models.Usuario(email=email, hashed_password=hash_password(password))
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


def autenticar_usuario(db: Session, email: str, password: str) -> models.Usuario | None:
    usuario = get_usuario_por_email(db, email)
    if usuario is None or not verificar_password(password, usuario.hashed_password):
        return None
    return usuario

from datetime import date

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/personas", tags=["personas"])


# IMPORTANTE: las rutas específicas (/hoy, /manana, /proximo) tienen que ir
# ANTES de "/{persona_id}", si no FastAPI intenta parsear "hoy" como int y
# tira 422.

@router.get("/hoy", response_model=list[schemas.PersonaOut])
def personas_que_cumplen_hoy(db: Session = Depends(get_db)):
    return crud.get_personas_que_cumplen_hoy(db)


@router.get("/manana", response_model=list[schemas.PersonaOut])
def personas_que_cumplen_manana(db: Session = Depends(get_db)):
    return crud.get_personas_que_cumplen_manana(db)


@router.get("/proximo", response_model=schemas.PersonaProximoOut)
def proximo_cumpleanios(db: Session = Depends(get_db)):
    persona, dias = crud.get_proximo_cumpleanios(db)
    if persona is None:
        return schemas.PersonaProximoOut(persona=None, dias_faltantes=None)
    return schemas.PersonaProximoOut(persona=persona, dias_faltantes=dias)


@router.get("", response_model=list[schemas.PersonaOut])
def listar_personas(db: Session = Depends(get_db)):
    return crud.get_personas(db)


@router.get("/{persona_id}", response_model=schemas.PersonaOut)
def obtener_persona(persona_id: int, db: Session = Depends(get_db)):
    persona = crud.get_persona(db, persona_id)
    if persona is None:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return persona


@router.post("", response_model=schemas.PersonaOut, status_code=201)
async def crear_persona(
    nombre: str = Form(...),
    fecha_nacimiento: date = Form(...),
    hobbies: str = Form(""),
    foto: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    return crud.crear_persona(db, nombre, fecha_nacimiento, hobbies, foto)


@router.delete("/{persona_id}")
def eliminar_persona(persona_id: int, db: Session = Depends(get_db)):
    persona = crud.eliminar_persona(db, persona_id)
    if persona is None:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return {"ok": True, "id": persona_id}

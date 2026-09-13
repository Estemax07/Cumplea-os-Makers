from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db
from ..security import crear_access_token

router = APIRouter(tags=["auth"])


@router.post("/registro", response_model=schemas.Token, status_code=201)
def registro(datos: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    if crud.get_usuario_por_email(db, datos.email):
        raise HTTPException(status_code=400, detail="Ese email ya está registrado")

    usuario = crud.crear_usuario(db, datos.email, datos.password)
    token = crear_access_token({"sub": usuario.email, "uid": usuario.id})
    return schemas.Token(access_token=token, usuario=usuario)


@router.post("/login", response_model=schemas.Token)
def login(datos: schemas.UsuarioLogin, db: Session = Depends(get_db)):
    usuario = crud.autenticar_usuario(db, datos.email, datos.password)
    if usuario is None:
        raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")

    token = crear_access_token({"sub": usuario.email, "uid": usuario.id})
    return schemas.Token(access_token=token, usuario=usuario)

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .config import settings
from .database import Base, engine
from .routers import auth, personas

# Crea las tablas si no existen (SQLite/Postgres vía DATABASE_URL)
Base.metadata.create_all(bind=engine)

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sirve las fotos subidas en /uploads/<archivo> (foto_url apunta acá)
app.mount(
    settings.UPLOAD_URL_PREFIX,
    StaticFiles(directory=settings.UPLOAD_DIR),
    name="uploads",
)

app.include_router(personas.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {
        "app": settings.APP_NAME,
        "estado": "ok",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "ok"}

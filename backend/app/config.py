import os
from dotenv import load_dotenv

load_dotenv()


def _split_origins(raw: str) -> list[str]:
    raw = (raw or "").strip()
    if raw == "" or raw == "*":
        return ["*"]
    return [o.strip() for o in raw.split(",") if o.strip()]


class Settings:
    # --- Base de datos ---
    DATABASE_URL: str = os.environ.get("DATABASE_URL", "sqlite:///./personas.db")

    # --- Archivos subidos (fotos) ---
    UPLOAD_DIR: str = os.environ.get("UPLOAD_DIR", "uploads")
    UPLOAD_URL_PREFIX: str = "/uploads"  # se sirve como estático desde main.py

    # --- Auth / JWT ---
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "cambia-esta-clave-en-produccion")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

    # --- CORS ---
    # En dev: "*" (default). En producción: poné el dominio real del frontend,
    # ej "https://cumple-makers.vercel.app" (separados por coma si son varios).
    CORS_ORIGINS: list[str] = _split_origins(os.environ.get("CORS_ORIGINS", "*"))

    # --- Info general ---
    APP_NAME: str = "Birthday App — backend de personas"


settings = Settings()

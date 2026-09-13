# Birthday App — backend de personas

FastAPI + SQLAlchemy. Implementa el contrato exacto que ya consume el
frontend (`frontend/src/api.js`) y el servicio de IA (`ai-service/main.py`).

## Modelo de datos (`Persona`)

`id, nombre, fecha_nacimiento, hobbies, foto_url`

La edad **nunca se guarda**: `edad_actual` se calcula siempre a partir de
`fecha_nacimiento` y se agrega en cada respuesta (ver `app/schemas.py`).

## Endpoints

| Método | Ruta                | Descripción |
|---|---|---|
| GET    | `/personas`         | Lista completa |
| GET    | `/personas/hoy`     | Quiénes cumplen hoy |
| GET    | `/personas/manana`  | Quiénes cumplen mañana |
| GET    | `/personas/proximo` | `{ "persona": {...}, "dias_faltantes": N }` |
| GET    | `/personas/{id}`    | Detalle de una persona |
| POST   | `/personas`         | multipart/form-data: `nombre, fecha_nacimiento, hobbies, foto` |
| DELETE | `/personas/{id}`    | Elimina una persona (y su foto local) |
| POST   | `/registro`         | `{ "email": "...", "password": "..." }` → JWT |
| POST   | `/login`            | `{ "email": "...", "password": "..." }` → JWT |
| GET    | `/health`           | Chequeo de salud |

Las fotos subidas se guardan en `UPLOAD_DIR` (default `uploads/`) y se
sirven como estático en `/uploads/<archivo>`. `foto_url` en las respuestas
es siempre una ruta relativa (`/uploads/xxx.jpg`) — el frontend ya sabe
anteponerle `VITE_API_URL` (ver `urlFoto()` en `src/api.js`).

## Cómo correrlo local

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate   # opcional pero recomendado
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8123
```

Quedará en `http://localhost:8123`, que es lo que el frontend espera por
default (`VITE_API_URL`). Docs interactivas en `http://localhost:8123/docs`.

## Variables de entorno (`.env`)

Ver `.env.example`. Las importantes:

- `DATABASE_URL`: por default SQLite local (`sqlite:///./personas.db`).
  **En producción usá Postgres** (Render/Railway te dan uno gratis o
  barato) — SQLite en un disco efímero se te puede borrar en cada deploy.
- `UPLOAD_DIR`: carpeta de fotos. En Render, si usás disco efímero (el
  plan free), **las fotos se pierden en cada redeploy**. Para persistirlas
  de verdad, agregá un [Persistent Disk](https://render.com/docs/disks) en
  Render montado en esta carpeta, o migrá a un storage tipo S3/Cloudinary
  más adelante.
- `SECRET_KEY`: cambiala en producción, es la que firma los JWT.
- `CORS_ORIGINS`: `*` en dev. En producción, poné el dominio real del
  frontend (ej `https://cumple-makers.vercel.app`), separado por coma si
  hay más de uno.

## Deploy en Render (resumen)

1. **Web Service** nuevo, apuntando a este repo/carpeta `backend/`.
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
2. Agregá las env vars de `.env.example` en el panel de Render (con los
   valores reales de producción, no los de ejemplo).
3. Si vas a persistir fotos y/o SQLite entre deploys, agregá un Persistent
   Disk montado en `/opt/render/project/src/backend` (o donde corresponda)
   y apuntá `UPLOAD_DIR` (y `DATABASE_URL` si seguís con SQLite) ahí.
   Más simple y más robusto: usar Postgres para `DATABASE_URL` y no
   depender del disco para la base.
4. Copiá la URL pública que te da Render (ej
   `https://birthday-backend.onrender.com`) y usala como:
   - `VITE_API_URL` en el frontend
   - `BACKEND_URL` en el `ai-service`
   - `BACKEND_URL` en `cron/` (ver `cron/README.md`)

## Correo automático (recordatorio del día antes)

Ver `cron/README.md` — es un script aparte (`cron/enviar_recordatorio.py`)
pensado para correr como Render Cron Job (o cualquier scheduler) una vez
al día, usando Resend.

## Notas de diseño

- Las rutas `/personas/hoy`, `/personas/manana` y `/personas/proximo` están
  declaradas ANTES de `/personas/{id}` en `app/routers/personas.py` a
  propósito — si no, FastAPI intenta interpretar `"hoy"` como el `int` del
  path param y tira 422.
- `/personas/proximo` puede devolver `dias_faltantes: 0` si justo hoy es
  el cumpleaños más próximo (no excluye "hoy" del cálculo). Si preferís
  que "próximo" arranque siempre desde mañana en adelante, es un cambio
  de una línea en `crud.get_proximo_cumpleanios` — avisame y lo ajusto.
- Passwords: se hashean con `bcrypt` (uso la librería directa, no
  `passlib`, por un bug de compatibilidad conocido entre `passlib` 1.7.x
  y `bcrypt` >= 4.1 — ver comentario en `app/security.py`).

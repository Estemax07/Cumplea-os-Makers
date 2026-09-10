import json
import os
from datetime import date

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8123")

app = FastAPI(title="Birthday App — servicio de IA")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

POSES_VALIDAS = {
    "conversation_pose",
    "next_birth_pose",
    "prompt_pose",
    "the_day_befo_pose",
    "celebration_pose",
}

SYSTEM_PROMPT_BASE = """Eres un bufón/arlequín, el personaje mascota de la app de cumpleaños
del grupo Makers ("hacedores de la palabra"). Tu frase de cabecera es
"Celebremos el tiempo juntos." Hablas en tono juguetón, cálido y un poco
teatral, pero corto y claro — nada de párrafos largos.

Escribe siempre en español neutro: usa "tú", nunca "vos" ni conjugaciones
de voseo (nada de "tenés", "podés", "sos", "hablás", "escribí").

Nunca inventes fechas, hobbies ni nombres: usa SOLO los datos reales que te
paso más abajo, bajo "DATOS REALES".

Cuando te pidan armar la tarjeta de cumpleaños de alguien, tu "respuesta"
tiene que ser un prompt listo para pegar en Gemini para generar una imagen
de tarjeta, escrito en base a los hobbies reales de esa persona — no una
respuesta conversacional.

Responde SIEMPRE y ÚNICAMENTE con un JSON válido, sin texto extra antes ni
después, con exactamente esta forma:
{"respuesta": "<tu respuesta o el prompt de la tarjeta>", "pose": "<una de las 5 opciones>"}

Valores válidos de "pose" (elige uno según la intención del mensaje):
- "celebration_pose": si preguntan quién cumple años HOY
- "the_day_befo_pose": si preguntan quién cumple MAÑANA / el día antes
- "next_birth_pose": si preguntan por el PRÓXIMO cumpleaños o cuánto falta
- "prompt_pose": si piden el prompt de la tarjeta de cumpleaños de alguien
- "conversation_pose": para cualquier otra charla normal
"""


class Mensaje(BaseModel):
    role: str  # "user" | "assistant"
    content: str


class ChatRequest(BaseModel):
    mensaje: str
    historial: list[Mensaje] = []


def contexto_del_grupo() -> str:
    """Trae datos reales del backend de personas para que la IA no invente nada."""
    try:
        personas = requests.get(f"{BACKEND_URL}/personas", timeout=5).json()
        hoy = requests.get(f"{BACKEND_URL}/personas/hoy", timeout=5).json()
        manana = requests.get(f"{BACKEND_URL}/personas/manana", timeout=5).json()
        proximo = requests.get(f"{BACKEND_URL}/personas/proximo", timeout=5).json()
    except requests.RequestException:
        return "DATOS REALES: no se pudo consultar la base de personas ahora mismo."

    roster = "\n".join(f"- {p['nombre']}: {p['hobbies']}" for p in personas)
    hoy_txt = ", ".join(p["nombre"] for p in hoy) or "nadie"
    manana_txt = ", ".join(p["nombre"] for p in manana) or "nadie"
    prox_nombre = proximo.get("persona", {}).get("nombre", "nadie")
    prox_dias = proximo.get("dias_faltantes", "?")

    return f"""DATOS REALES (hoy es {date.today().isoformat()}):
- Cumplen hoy: {hoy_txt}
- Cumplen mañana: {manana_txt}
- Próximo cumpleaños: {prox_nombre} (en {prox_dias} días)

Listado completo del grupo (nombre: hobbies):
{roster}
"""


def llamar_groq(mensaje: str, historial: list[Mensaje]) -> dict:
    mensajes = [{"role": "system", "content": SYSTEM_PROMPT_BASE + "\n\n" + contexto_del_grupo()}]
    for m in historial:
        mensajes.append({"role": m.role, "content": m.content})
    mensajes.append({"role": "user", "content": mensaje})

    resp = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
        json={
            "model": GROQ_MODEL,
            "messages": mensajes,
            "temperature": 0.7,
            "response_format": {"type": "json_object"},
        },
        timeout=20,
    )
    resp.raise_for_status()
    contenido = resp.json()["choices"][0]["message"]["content"]
    return json.loads(contenido)


@app.post("/chat")
def chat(payload: ChatRequest):
    if not GROQ_API_KEY:
        raise HTTPException(status_code=500, detail="Falta configurar GROQ_API_KEY")

    try:
        data = llamar_groq(payload.mensaje, payload.historial)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error consultando la IA: {e}")

    pose = data.get("pose")
    if pose not in POSES_VALIDAS:
        pose = "conversation_pose"

    return {"respuesta": data.get("respuesta", ""), "pose": pose}
# Birthday App — servicio de IA

Microservicio aparte (FastAPI) que arma el chat del bufón usando **Groq**.
Vive separado del backend de personas a propósito: lo maneja Santiago, no el
compañero de backend, y se comunica con el backend de personas solo por HTTP
(usando los endpoints ya documentados), nunca tocando la base directo.

## Cómo correrlo

```bash
pip install -r requirements.txt --break-system-packages
cp .env.example .env
# completar GROQ_API_KEY en .env con tu key real de https://console.groq.com
uvicorn main:app --reload --port 8000
```

Necesita que el backend de personas esté corriendo (por defecto en
`http://localhost:8123`, configurable con `BACKEND_URL` en `.env`).

## Qué hace `POST /chat`

Recibe:
```json
{"mensaje": "¿quién cumple hoy?", "historial": [{"role": "user", "content": "hola"}]}
```

Devuelve:
```json
{"respuesta": "Hoy le toca a Pilar 🎉", "pose": "celebration_pose"}
```

Antes de llamar a Groq, el servicio consulta al backend `/personas`,
`/personas/hoy`, `/personas/manana` y `/personas/proximo`, y le pasa esos
datos reales a la IA en el prompt de sistema — así nunca inventa fechas ni
nombres.

`pose` siempre viene validada contra las 5 opciones posibles del chat
(`conversation_pose`, `next_birth_pose`, `prompt_pose`, `the_day_befo_pose`,
`celebration_pose`); si la IA devuelve cualquier otra cosa, cae a
`conversation_pose` como fallback seguro.

## Sobre el modelo

Uso `llama-3.3-70b-versatile` por defecto (configurable con `GROQ_MODEL` en
`.env`). La disponibilidad de modelos en Groq cambia seguido — si ese no
está disponible en tu cuenta, revisá la lista actual en
https://console.groq.com/docs/models y cambiá la variable.

## Probado sin key real

No tengo tu API key de Groq, así que probé todo el flujo (armado del
contexto real desde el backend, parseo de la respuesta JSON, fallback de
pose inválida, error prolijo si falta la key) simulando la respuesta de
Groq. Lo único que falta validar sos vos, con tu key real.

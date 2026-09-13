"""
Cron diario para la app de cumpleaños de Makers.

Qué hace:
1. Consulta GET {BACKEND_URL}/personas/manana
2. Si hay alguien, manda un correo por cada persona con:
   - Encabezado: "Mañana Cumple <nombre>"
   - Imagen: the_day_befo_pose (la pose del bufón para "el día antes")
   - Texto de recordatorio juguetón, usando los hobbies reales de la persona
3. Envía con Resend (dominio verificado) para no caer en spam.

Pensado para correr una vez al día vía Render Cron Job (o cualquier
scheduler tipo cron: GitHub Actions, Railway Cron, un cron de Linux, etc).

Variables de entorno necesarias (ver .env.example en esta misma carpeta):
- BACKEND_URL            URL del backend de personas (ej: https://api.tudominio.com)
- RESEND_API_KEY         API key de Resend (https://resend.com/api-keys)
- RESEND_FROM            Remitente verificado, ej: "Makers <cumples@tudominio.com>"
- DESTINATARIOS          Emails que reciben el aviso, separados por coma
- FRONTEND_URL           URL pública del frontend (para armar la URL de la imagen
                          the_day_befo_pose.png, que vive en frontend/public/character/)
- THE_DAY_BEFORE_IMAGE_URL   (opcional) URL directa a la imagen si no querés
                          depender de FRONTEND_URL

Nota: a propósito NO se usa SMTP crudo de Gmail — con un dominio no
verificado, la mayoría de estos correos terminan en spam. Resend (o
SendGrid) con dominio propio verificado es la vía recomendada.
"""

import os
import sys

import requests
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8123").rstrip("/")
RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")
RESEND_FROM = os.environ.get("RESEND_FROM", "Makers <onboarding@resend.dev>")
DESTINATARIOS = [d.strip() for d in os.environ.get("DESTINATARIOS", "").split(",") if d.strip()]
FRONTEND_URL = os.environ.get("FRONTEND_URL", "").rstrip("/")
THE_DAY_BEFORE_IMAGE_URL = os.environ.get("THE_DAY_BEFORE_IMAGE_URL") or (
    f"{FRONTEND_URL}/character/the_day_befo_pose.png" if FRONTEND_URL else ""
)

RESEND_ENDPOINT = "https://api.resend.com/emails"


def obtener_personas_que_cumplen_manana() -> list[dict]:
    resp = requests.get(f"{BACKEND_URL}/personas/manana", timeout=10)
    resp.raise_for_status()
    return resp.json()


def armar_html(persona: dict) -> str:
    nombre = persona.get("nombre", "alguien")
    hobbies = persona.get("hobbies", "") or ""
    edad = persona.get("edad_actual")

    linea_hobbies = (
        f"<p style='margin:0 0 16px;'>Dicen por ahí que le encanta <strong>{hobbies}</strong> — "
        f"buen momento para un detalle que tenga que ver con eso. 👀</p>"
        if hobbies
        else ""
    )
    linea_edad = f" y cumple {edad} años" if edad is not None else ""

    imagen_html = (
        f"<img src='{THE_DAY_BEFORE_IMAGE_URL}' alt='El bufón de Makers avisando el cumple de mañana' "
        f"style='max-width:220px;display:block;margin:0 auto 20px;' />"
        if THE_DAY_BEFORE_IMAGE_URL
        else ""
    )

    return f"""
    <div style="font-family: Georgia, 'Times New Roman', serif; background:#e3d3c0;
                padding:32px 24px; border-radius:16px; max-width:480px; margin:0 auto;
                color:#1a1a1a; border:2.5px solid #1a1a1a;">
      <h1 style="text-align:center; font-size:26px; margin:0 0 4px; color:#482a4d;">
        🎉 Mañana Cumple {nombre}
      </h1>
      <p style="text-align:center; font-style:italic; margin:0 0 20px; color:#b58548;">
        "Celebremos el tiempo juntos."
      </p>
      {imagen_html}
      <p style="margin:0 0 16px;">
        Atención, Makers: mañana es el gran día de <strong>{nombre}</strong>{linea_edad}.
        Todavía están a tiempo de preparar algo lindo. ✨
      </p>
      {linea_hobbies}
      <p style="margin:0; font-size:13px; color:#555;">
        — El bufón de la app de cumpleaños de Makers
      </p>
    </div>
    """


def enviar_correo(persona: dict) -> None:
    if not RESEND_API_KEY:
        print("Falta RESEND_API_KEY, no se puede enviar el correo.", file=sys.stderr)
        sys.exit(1)

    if not DESTINATARIOS:
        print("Falta DESTINATARIOS (emails separados por coma), no se envía nada.", file=sys.stderr)
        sys.exit(1)

    payload = {
        "from": RESEND_FROM,
        "to": DESTINATARIOS,
        "subject": f"Mañana Cumple {persona.get('nombre', '')}",
        "html": (
            "<!DOCTYPE html><html><head><meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width, initial-scale=1'></head>"
            f"<body style='margin:0;padding:24px;background:#f5ece0;'>{armar_html(persona)}</body></html>"
        ),
    }

    resp = requests.post(
        RESEND_ENDPOINT,
        headers={
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=15,
    )

    if resp.status_code >= 300:
        print(f"Error enviando correo para {persona.get('nombre')}: {resp.status_code} {resp.text}", file=sys.stderr)
    else:
        print(f"Correo enviado para {persona.get('nombre')} -> {DESTINATARIOS}")


def main():
    try:
        personas = obtener_personas_que_cumplen_manana()
    except requests.RequestException as e:
        print(f"No se pudo consultar {BACKEND_URL}/personas/manana: {e}", file=sys.stderr)
        sys.exit(1)

    if not personas:
        print("Nadie cumple años mañana. No se envía ningún correo.")
        return

    for persona in personas:
        enviar_correo(persona)


if __name__ == "__main__":
    main()

# Cron de recordatorio — "Mañana Cumple..."

Script standalone (`enviar_recordatorio.py`) que:

1. Consulta `GET {BACKEND_URL}/personas/manana`.
2. Si hay una o más personas, manda un correo por cada una con Resend:
   asunto "Mañana Cumple `<nombre>`", la imagen `the_day_befo_pose`, y un
   texto de recordatorio juguetón usando los hobbies reales.
3. Si nadie cumple mañana, no manda nada (solo loguea un mensaje).

No usa SMTP de Gmail a propósito — con un dominio verificado en Resend (o
SendGrid) la entregabilidad es mucho mejor y no cae en spam.

## Setup

```bash
cd backend/cron
pip install -r requirements.txt
cp .env.example .env
# completar RESEND_API_KEY, RESEND_FROM, DESTINATARIOS, BACKEND_URL, FRONTEND_URL
python3 enviar_recordatorio.py
```

### Resend

1. Creá una cuenta en https://resend.com
2. Domains → Add Domain → agregás los registros DNS (SPF/DKIM) que te
   piden en tu proveedor de dominio. Sin esto podés probar igual con el
   remitente de test `onboarding@resend.dev`, pero para producción real
   necesitás el dominio verificado (mejor entregabilidad, sin el sello de
   "vía resend.dev").
3. API Keys → Create API Key → esa es `RESEND_API_KEY`.
4. `RESEND_FROM` tiene que ser una dirección de tu dominio verificado, ej
   `Makers <cumples@tudominio.com>`.

(Si preferís SendGrid en vez de Resend, el cambio es chico: reemplazar el
POST a `https://api.resend.com/emails` por el endpoint de SendGrid
`https://api.sendgrid.com/v3/mail/send` con su propio formato de payload.)

## Cómo programarlo para que corra todos los días

### Opción A — Render Cron Job

1. En Render: New → Cron Job.
2. Root directory: `backend/cron` (o la carpeta donde vive este script).
3. Build command: `pip install -r requirements.txt`
4. Command: `python3 enviar_recordatorio.py`
5. Schedule: cron estándar en UTC. Ejemplo, para que corra todos los días
   a las 8:00 AM hora Colombia (UTC-5) → `0 13 * * *`.
6. Cargá las env vars (`BACKEND_URL`, `RESEND_API_KEY`, `RESEND_FROM`,
   `DESTINATARIOS`, `FRONTEND_URL`) en el panel del Cron Job.

### Opción B — GitHub Actions (gratis, sin depender de Render)

`.github/workflows/recordatorio-cumple.yml`:

```yaml
name: Recordatorio de cumpleaños
on:
  schedule:
    - cron: "0 13 * * *"  # 8:00 AM Colombia (UTC-5)
  workflow_dispatch: {}   # para poder correrlo manual desde GitHub también

jobs:
  enviar:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r backend/cron/requirements.txt
      - run: python3 backend/cron/enviar_recordatorio.py
        env:
          BACKEND_URL: ${{ secrets.BACKEND_URL }}
          RESEND_API_KEY: ${{ secrets.RESEND_API_KEY }}
          RESEND_FROM: ${{ secrets.RESEND_FROM }}
          DESTINATARIOS: ${{ secrets.DESTINATARIOS }}
          FRONTEND_URL: ${{ secrets.FRONTEND_URL }}
```

(Los secrets se cargan en el repo de GitHub: Settings → Secrets and
variables → Actions.)

## Probarlo sin gastar envíos reales

Podés importar las funciones directamente para ver qué generaría, sin
llamar a Resend:

```bash
python3 -c "
from enviar_recordatorio import obtener_personas_que_cumplen_manana, armar_html
personas = obtener_personas_que_cumplen_manana()
print(len(personas), 'personas cumplen mañana')
for p in personas:
    print(armar_html(p))
"
```

# Birthday App — frontend

React + Vite + Framer Motion. Usa los assets reales del zip (personaje, botón de IA, logo de Makers) y la paleta de color sacada del logo y de las ilustraciones.

## Cómo correrlo

```bash
npm install
npm run dev
```

Necesita el backend corriendo en `http://localhost:8123` (ver `../backend/README.md`).
Si el backend corre en otra URL, creá un archivo `.env` con:

```
VITE_API_URL=http://tu-backend:puerto
```

## Qué incluye

- **Calendario** (`/`): los 12 meses en columna, cada uno en un recuadro con borde
  negro sin relleno (se funde con el fondo crema). Los días con cumpleaños muestran
  la foto de la persona en vez del número, con una pequeña animación de "caída"
  al cargar (una sola vez, no en bucle).
- **Detalle de persona**: al hacer click en una foto del calendario, se abre el
  modal con Nombre / Fecha / Edad actual / Hobbys y el personaje en `celebration_pose`.
- **Admin** (`/admin`): alta de personas (nombre, fecha, hobbys, foto — la edad
  actual se calcula sola, no se pide en el form) y baja con confirmación. Todo
  pega directo contra el backend (POST /personas con multipart, DELETE /personas/{id}).

## Paleta de color usada (`src/theme.css`)

| Variable | Color | De dónde sale |
|---|---|---|
| `--cream` | `#e3d3c0` | Fondo exacto de las ilustraciones del personaje |
| `--purple` | `#482a4d` | Traje del bufón |
| `--gold` | `#b58548` | Detalles dorados del traje |
| `--amber` | `#f49d2c` | Llama del logo de Makers (color de marca, botones) |
| `--ink` | `#1a1a1a` | Texto y bordes, igual que el wordmark del logo |

## Todavía no incluido (a propósito)

El botón/chat de la IA (`Button.png`, las 8 poses restantes, `Card_load.png`) y las
pantallas de login/registro quedaron afuera de esta entrega — el foco de esta
entrega es el front del calendario + admin, la IA se ve en otra sesión.

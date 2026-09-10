import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { enviarMensaje } from "../aiApi";

const imagenDePose = (pose) => `/character/${pose}.png`;

const FRASES_BIENVENIDA = [
  "Celebremos el tiempo juntos. ¿En qué te ayudo hoy?",
  "El bufón está listo para las novedades del grupo.",
  "Antes de que preguntes: siempre hay alguien por cumplir años.",
  "Bienvenido de nuevo. ¿Vemos quién cumple pronto?",
  "Las cartas están listas. ¿Qué quieres saber?",
  "Un nuevo día, una buena excusa para festejar.",
  "¿Empezamos a planear alguna sorpresa?",
];

export default function AIChat() {
  const [open, setOpen] = useState(false);
  const [mensajes, setMensajes] = useState([]);
  const [pose, setPose] = useState("conversation_pose");
  const [cargando, setCargando] = useState(false);
  const [texto, setTexto] = useState("");
  const [saludo, setSaludo] = useState(FRASES_BIENVENIDA[0]);

  useEffect(() => {
    if (open) {
      const elegido = FRASES_BIENVENIDA[Math.floor(Math.random() * FRASES_BIENVENIDA.length)];
      setSaludo(elegido);
    }
  }, [open]);

  async function enviar(e) {
    e.preventDefault();
    const contenido = texto.trim();
    if (!contenido) return;

    const historialPrevio = mensajes;
    setMensajes([...historialPrevio, { role: "user", content: contenido }]);
    setTexto("");
    setCargando(true);

    try {
      const { respuesta, pose: nuevaPose } = await enviarMensaje(contenido, historialPrevio);
      setPose(nuevaPose);
      setMensajes((actuales) => [...actuales, { role: "assistant", content: respuesta }]);
    } catch {
      setMensajes((actuales) => [
        ...actuales,
        { role: "assistant", content: "Uy, no pude responder. Intenta de nuevo en un rato." },
      ]);
    } finally {
      setCargando(false);
    }
  }

  return (
    <>
      <AnimatePresence>
        {!open && (
          <motion.button
            key="boton"
            layoutId="ai-panel"
            onClick={() => setOpen(true)}
            style={{
              position: "fixed",
              bottom: 22,
              right: 22,
              width: 62,
              height: 62,
              borderRadius: "50%",
              border: "none",
              padding: 0,
              overflow: "hidden",
              boxShadow: "0 2px 10px rgba(26,18,20,0.3)",
              zIndex: 40,
            }}
            aria-label="Abrir chat con el bufón"
          >
            <img
              src="/brand/ai_button.png"
              alt=""
              style={{ width: "100%", height: "100%", objectFit: "cover" }}
            />
          </motion.button>
        )}
      </AnimatePresence>

      <AnimatePresence>
        {open && (
          <motion.div
            key="fondo"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setOpen(false)}
            style={{
              position: "fixed",
              inset: 0,
              background: "rgba(26,18,20,0.5)",
              zIndex: 45,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              padding: "1rem",
            }}
          >
            <motion.div
              layoutId="ai-panel"
              onClick={(e) => e.stopPropagation()}
              style={{
                width: "100%",
                maxWidth: 640,
                height: "min(82vh, 560px)",
                background: "var(--cream)",
                border: "2.5px solid var(--ink)",
                borderRadius: "var(--radius-lg)",
                display: "flex",
                overflow: "hidden",
              }}
            >
              {/* Izquierda: el personaje, cambia de pose según la respuesta */}
              <div
                style={{
                  flex: "1 1 40%",
                  position: "relative",
                  overflow: "hidden",
                }}
              >
                <motion.img
                  key={cargando ? "thinking_pose" : pose}
                  src={imagenDePose(cargando ? "thinking_pose" : pose)}
                  alt=""
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ duration: 0.35 }}
                  style={{
                    position: "absolute",
                    inset: 0,
                    width: "100%",
                    height: "100%",
                    objectFit: "cover",
                    objectPosition: "top center",
                  }}
                />

                {cargando && (
                  <motion.img
                    src="/character/card_load.png"
                    alt="Pensando…"
                    animate={{ rotateY: 360 }}
                    transition={{ repeat: Infinity, duration: 1.4, ease: "linear" }}
                    style={{
                      position: "absolute",
                      top: "50%",
                      left: "50%",
                      width: 66,
                      transform: "translate(-50%, -50%)",
                    }}
                  />
                )}
              </div>

              {/* Derecha: el chat */}
              <div style={{ flex: "1 1 60%", display: "flex", flexDirection: "column", padding: "1rem" }}>
                <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 10 }}>
                  <img
                    src="/brand/ai_button.png"
                    alt=""
                    style={{ width: 28, height: 28, borderRadius: "50%", objectFit: "cover" }}
                  />
                  <strong className="titulo-comic" style={{ fontSize: "1.05rem" }}>
                    mensaje diario
                  </strong>
                </div>

                <div style={{ flex: 1, overflowY: "auto", display: "flex", flexDirection: "column", gap: 8, marginBottom: 10 }}>
                  {mensajes.length === 0 && (
                    <p style={{ color: "var(--ink-soft)", fontSize: "0.85rem" }}>{saludo}</p>
                  )}
                  {mensajes.map((m, i) => (
                    <div
                      key={i}
                      style={{
                        alignSelf: m.role === "user" ? "flex-end" : "flex-start",
                        background: m.role === "user" ? "var(--amber)" : "white",
                        borderRadius: 10,
                        padding: "6px 10px",
                        maxWidth: "80%",
                        fontSize: "0.9rem",
                      }}
                    >
                      {m.content}
                    </div>
                  ))}
                </div>

                <form onSubmit={enviar} style={{ display: "flex", gap: 6 }}>
                  <input
                    value={texto}
                    onChange={(e) => setTexto(e.target.value)}
                    placeholder="Empecemos a planear"
                    style={{
                      flex: 1,
                      borderRadius: 999,
                      border: "1.5px solid rgba(72,42,77,0.25)",
                      padding: "0.5rem 0.9rem",
                      fontSize: "0.9rem",
                    }}
                  />
                  <button type="submit" className="btn-primario" disabled={cargando} aria-label="Enviar">
                    ↑
                  </button>
                </form>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
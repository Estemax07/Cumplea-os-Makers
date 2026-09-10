import { motion, AnimatePresence } from "framer-motion";
import { urlFoto } from "../api";

export default function PersonDetailModal({ persona, onClose }) {
  return (
    <AnimatePresence>
      {persona && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={onClose}
          style={{
            position: "fixed",
            inset: 0,
            background: "rgba(26,18,20,0.55)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            padding: "1rem",
            zIndex: 50,
          }}
        >
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.92 }}
            transition={{ type: "spring", bounce: 0.25, duration: 0.4 }}
            onClick={(e) => e.stopPropagation()}
            style={{
              background: "var(--cream)",
              borderRadius: "var(--radius-lg)",
              border: "2.5px solid var(--ink)",
              maxWidth: 560,
              width: "100%",
              display: "flex",
              flexWrap: "wrap",
              overflow: "hidden",
            }}
          >
            {/* Izquierda: polaroid + datos */}
            <div style={{ flex: "1 1 240px", padding: "1.5rem" }}>
              <div
                style={{
                  background: "white",
                  padding: "8px 8px 24px 8px",
                  border: "1px solid rgba(26,26,26,0.2)",
                  transform: "rotate(-3deg)",
                  width: "80%",
                  margin: "0 auto 1.2rem auto",
                }}
              >
                <img
                  src={urlFoto(persona.foto_url)}
                  alt={persona.nombre}
                  style={{ width: "100%", aspectRatio: "1", objectFit: "cover" }}
                />
              </div>

              <p><strong>Nombre:</strong> {persona.nombre}</p>
              <p><strong>Fecha:</strong> {persona.fecha_nacimiento}</p>
              <p><strong>Edad actual:</strong> {persona.edad_actual}</p>
              <p><strong>Hobbys:</strong> {persona.hobbies}</p>
            </div>

            {/* Derecha: personaje en pose de celebración */}
            <div
              style={{
                flex: "1 1 200px",
                background: "var(--cream-soft)",
                display: "flex",
                alignItems: "flex-end",
                justifyContent: "center",
              }}
            >
              <img
                src="/character/celebration_pose.png"
                alt="Personaje celebrando"
                style={{ width: "100%", maxHeight: 340, objectFit: "cover" }}
              />
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

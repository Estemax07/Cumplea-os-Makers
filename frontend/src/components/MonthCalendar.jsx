import { motion } from "framer-motion";
import { urlFoto } from "../api";

const DIAS_SEMANA = ["D", "L", "M", "M", "J", "V", "S"];

function diasDelMes(anio, mesIndex0) {
  return new Date(anio, mesIndex0 + 1, 0).getDate();
}

function primerDiaSemana(anio, mesIndex0) {
  return new Date(anio, mesIndex0, 1).getDay(); // 0 = domingo
}

export default function MonthCalendar({ anio, mesIndex0, monthLabel, personas, onSelectPersona }) {
  const totalDias = diasDelMes(anio, mesIndex0);
  const offset = primerDiaSemana(anio, mesIndex0);

  const cumpleañerosPorDia = {};
  for (const p of personas) {
    const fecha = new Date(p.fecha_nacimiento + "T00:00:00");
    if (fecha.getMonth() === mesIndex0) {
      const dia = fecha.getDate();
      (cumpleañerosPorDia[dia] ||= []).push(p);
    }
  }

  const celdas = [];
  for (let i = 0; i < offset; i++) celdas.push(null);
  for (let dia = 1; dia <= totalDias; dia++) celdas.push(dia);

  return (
    <div
      style={{
        border: "2.5px solid var(--ink)",
        background: "transparent",
        borderRadius: "var(--radius-lg)",
        padding: "1.1rem 1rem",
        marginBottom: "1.5rem",
      }}
    >
      <h2 className="titulo-comic" style={{ fontSize: "1.6rem", marginBottom: "0.7rem" }}>
        {monthLabel}
      </h2>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(7, 1fr)",
          gap: "6px",
          fontSize: "0.7rem",
          color: "var(--ink-soft)",
          textAlign: "center",
          marginBottom: "6px",
          fontWeight: 600,
        }}
      >
        {DIAS_SEMANA.map((d, i) => (
          <span key={i}>{d}</span>
        ))}
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(7, 1fr)", gap: "6px" }}>
        {celdas.map((dia, idx) => {
          if (dia === null) return <div key={`vacio-${idx}`} />;

          const cumpleañeros = cumpleañerosPorDia[dia];
          if (cumpleañeros && cumpleañeros.length > 0) {
            const persona = cumpleañeros[0];
            return (
              <motion.button
                key={dia}
                onClick={() => onSelectPersona(persona)}
                initial={{ opacity: 0, scale: 0.85, rotate: 0 }}
                animate={{ opacity: 1, scale: 1, rotate: -8 }}
                transition={{ type: "spring", bounce: 0.45, duration: 0.5 }}
                whileHover={{ rotate: 0, scale: 1.08 }}
                style={{
                  aspectRatio: "1",
                  padding: "3px",
                  background: "white",
                  border: "1px solid rgba(26,26,26,0.25)",
                  borderRadius: "4px",
                  cursor: "pointer",
                  position: "relative",
                }}
                title={persona.nombre}
              >
                <img
                  src={urlFoto(persona.foto_url)}
                  alt={persona.nombre}
                  style={{ width: "100%", height: "100%", objectFit: "cover", borderRadius: "2px" }}
                />
                {cumpleañeros.length > 1 && (
                  <span
                    style={{
                      position: "absolute",
                      bottom: -4,
                      right: -4,
                      background: "var(--amber)",
                      color: "var(--ink)",
                      fontSize: "0.6rem",
                      fontWeight: 700,
                      borderRadius: "50%",
                      width: 16,
                      height: 16,
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                    }}
                  >
                    +{cumpleañeros.length - 1}
                  </span>
                )}
              </motion.button>
            );
          }

          return (
            <div
              key={dia}
              style={{
                aspectRatio: "1",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: "0.85rem",
                color: "var(--ink-soft)",
              }}
            >
              {dia}
            </div>
          );
        })}
      </div>
    </div>
  );
}

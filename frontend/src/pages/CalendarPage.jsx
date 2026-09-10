import { useEffect, useState } from "react";
import MonthCalendar from "../components/MonthCalendar";
import PersonDetailModal from "../components/PersonDetailModal";
import { getPersonas } from "../api";

const MESES = [
  "enero", "febrero", "marzo", "abril", "mayo", "junio",
  "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
];

export default function CalendarPage() {
  const [personas, setPersonas] = useState([]);
  const [seleccionada, setSeleccionada] = useState(null);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    getPersonas()
      .then(setPersonas)
      .catch(() => setError("No se pudo conectar con el backend. ¿Está corriendo en el puerto 8123?"))
      .finally(() => setCargando(false));
  }, []);

  const anio = new Date().getFullYear();

  if (cargando) {
    return <p style={{ padding: "1.5rem" }}>Cargando calendario…</p>;
  }

  if (error) {
    return <p style={{ padding: "1.5rem", color: "var(--danger)" }}>{error}</p>;
  }

  return (
    <div style={{ maxWidth: 480, margin: "0 auto", padding: "0 1.25rem 2rem" }}>
      {MESES.map((label, mesIndex0) => (
        <MonthCalendar
          key={label}
          anio={anio}
          mesIndex0={mesIndex0}
          monthLabel={label}
          personas={personas}
          onSelectPersona={setSeleccionada}
        />
      ))}

      <PersonDetailModal persona={seleccionada} onClose={() => setSeleccionada(null)} />
    </div>
  );
}

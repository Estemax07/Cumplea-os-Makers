import { useEffect, useState } from "react";
import { getPersonas, crearPersona, eliminarPersona, urlFoto } from "../api";

function edadDesdeFecha(fechaTexto) {
  if (!fechaTexto) return null;
  const nacimiento = new Date(fechaTexto + "T00:00:00");
  const hoy = new Date();
  let edad = hoy.getFullYear() - nacimiento.getFullYear();
  const noCumplioAunEsteAnio =
    hoy.getMonth() < nacimiento.getMonth() ||
    (hoy.getMonth() === nacimiento.getMonth() && hoy.getDate() < nacimiento.getDate());
  if (noCumplioAunEsteAnio) edad -= 1;
  return edad;
}

export default function AdminPage() {
  const [personas, setPersonas] = useState([]);
  const [cargando, setCargando] = useState(true);

  const [nombre, setNombre] = useState("");
  const [fecha, setFecha] = useState("");
  const [hobbies, setHobbies] = useState("");
  const [foto, setFoto] = useState(null);
  const [previewFoto, setPreviewFoto] = useState(null);
  const [enviando, setEnviando] = useState(false);
  const [errorForm, setErrorForm] = useState(null);

  function cargarPersonas() {
    setCargando(true);
    getPersonas().then(setPersonas).finally(() => setCargando(false));
  }

  useEffect(cargarPersonas, []);

  function manejarFoto(e) {
    const archivo = e.target.files?.[0] || null;
    setFoto(archivo);
    setPreviewFoto(archivo ? URL.createObjectURL(archivo) : null);
  }

  async function manejarSubmit(e) {
    e.preventDefault();
    setErrorForm(null);

    if (!nombre || !fecha || !hobbies) {
      setErrorForm("Completá nombre, fecha de nacimiento y hobbies.");
      return;
    }

    setEnviando(true);
    try {
      await crearPersona({ nombre, fecha_nacimiento: fecha, hobbies, foto });
      setNombre("");
      setFecha("");
      setHobbies("");
      setFoto(null);
      setPreviewFoto(null);
      cargarPersonas();
    } catch (err) {
      setErrorForm(err.message);
    } finally {
      setEnviando(false);
    }
  }

  async function manejarEliminar(id) {
    if (!confirm("¿Eliminar a esta persona del calendario?")) return;
    await eliminarPersona(id);
    cargarPersonas();
  }

  return (
    <div style={{ maxWidth: 720, margin: "0 auto", padding: "0 1.25rem 3rem", display: "grid", gap: "2rem" }}>
      {/* Formulario de alta */}
      <section
        style={{
          border: "2.5px solid var(--ink)",
          borderRadius: "var(--radius-lg)",
          padding: "1.3rem",
        }}
      >
        <h2 className="titulo-comic" style={{ fontSize: "1.4rem", marginBottom: "1rem" }}>
          agregar persona
        </h2>

        <form onSubmit={manejarSubmit}>
          <div className="campo">
            <label>Nombre</label>
            <input value={nombre} onChange={(e) => setNombre(e.target.value)} placeholder="Ej: Juan Pérez" />
          </div>

          <div className="campo">
            <label>Fecha de cumpleaños</label>
            <input type="date" value={fecha} onChange={(e) => setFecha(e.target.value)} />
            {fecha && (
              <span style={{ fontSize: "0.8rem", color: "var(--ink-soft)" }}>
                Edad actual (calculada): {edadDesdeFecha(fecha)} años
              </span>
            )}
          </div>

          <div className="campo">
            <label>Hobbys (separados por coma)</label>
            <input value={hobbies} onChange={(e) => setHobbies(e.target.value)} placeholder="fotografía, guitarra, running" />
          </div>

          <div className="campo">
            <label>Foto</label>
            <input type="file" accept="image/*" onChange={manejarFoto} />
            {previewFoto && (
              <img
                src={previewFoto}
                alt="Vista previa"
                style={{ width: 80, height: 80, objectFit: "cover", borderRadius: 6, marginTop: 6 }}
              />
            )}
          </div>

          {errorForm && <p style={{ color: "var(--danger)", fontSize: "0.85rem" }}>{errorForm}</p>}

          <button type="submit" className="btn-primario" disabled={enviando}>
            {enviando ? "Guardando…" : "Agregar"}
          </button>
        </form>
      </section>

      {/* Listado */}
      <section>
        <h2 className="titulo-comic" style={{ fontSize: "1.4rem", marginBottom: "1rem" }}>
          personas ({personas.length})
        </h2>

        {cargando ? (
          <p>Cargando…</p>
        ) : (
          <div style={{ display: "grid", gap: "0.6rem" }}>
            {personas.map((p) => (
              <div
                key={p.id}
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "0.8rem",
                  background: "var(--cream-soft)",
                  borderRadius: "var(--radius-md)",
                  padding: "0.6rem 0.8rem",
                }}
              >
                <img
                  src={urlFoto(p.foto_url)}
                  alt={p.nombre}
                  style={{ width: 42, height: 42, borderRadius: "50%", objectFit: "cover" }}
                />
                <div style={{ flex: 1 }}>
                  <div style={{ fontWeight: 600 }}>{p.nombre}</div>
                  <div style={{ fontSize: "0.8rem", color: "var(--ink-soft)" }}>
                    {p.fecha_nacimiento} · {p.edad_actual} años · {p.hobbies}
                  </div>
                </div>
                <button className="btn-peligro" onClick={() => manejarEliminar(p.id)}>
                  Eliminar
                </button>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}

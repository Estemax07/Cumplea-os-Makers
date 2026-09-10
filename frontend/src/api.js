const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8123";

export async function getPersonas() {
  const res = await fetch(`${API_URL}/personas`);
  if (!res.ok) throw new Error("No se pudo cargar la lista de personas");
  return res.json();
}

export async function crearPersona({ nombre, fecha_nacimiento, hobbies, foto }) {
  const form = new FormData();
  form.append("nombre", nombre);
  form.append("fecha_nacimiento", fecha_nacimiento);
  form.append("hobbies", hobbies);
  if (foto) form.append("foto", foto);

  const res = await fetch(`${API_URL}/personas`, {
    method: "POST",
    body: form,
  });
  if (!res.ok) throw new Error("No se pudo crear la persona");
  return res.json();
}

export async function eliminarPersona(id) {
  const res = await fetch(`${API_URL}/personas/${id}`, { method: "DELETE" });
  if (!res.ok) throw new Error("No se pudo eliminar la persona");
  return res.json();
}

export function urlFoto(foto_url) {
  if (!foto_url) return "";
  return foto_url.startsWith("http") ? foto_url : `${API_URL}${foto_url}`;
}

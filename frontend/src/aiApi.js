const AI_URL = import.meta.env.VITE_AI_URL || "http://localhost:8000";

export async function enviarMensaje(mensaje, historialPrevio) {
  const historial = historialPrevio.map((m) => ({ role: m.role, content: m.content }));
  const res = await fetch(`${AI_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ mensaje, historial }),
  });
  if (!res.ok) throw new Error("Error del servicio de IA");
  return res.json();
}

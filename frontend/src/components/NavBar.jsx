import { NavLink } from "react-router-dom";

export default function NavBar() {
  return (
    <header
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "0.9rem 1.25rem",
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: "0.6rem" }}>
        <img
          src="/brand/logo_makers.jpg"
          alt="Makers"
          style={{ width: 34, height: 34, borderRadius: "50%", objectFit: "cover" }}
        />
        <span className="titulo-comic" style={{ fontSize: "1.3rem" }}>
          cumpleaños
        </span>
      </div>

      <nav style={{ display: "flex", gap: "1.4rem" }}>
        <NavLink
          to="/"
          end
          style={({ isActive }) => ({
            fontWeight: 600,
            fontSize: "0.9rem",
            color: isActive ? "var(--amber-deep)" : "var(--ink-soft)",
            textDecoration: "none",
          })}
        >
          Calendario
        </NavLink>
        <NavLink
          to="/admin"
          style={({ isActive }) => ({
            fontWeight: 600,
            fontSize: "0.9rem",
            color: isActive ? "var(--amber-deep)" : "var(--ink-soft)",
            textDecoration: "none",
          })}
        >
          Admin
        </NavLink>
      </nav>
    </header>
  );
}

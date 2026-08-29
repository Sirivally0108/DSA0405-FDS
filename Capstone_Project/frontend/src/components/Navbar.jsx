import { NavLink } from "react-router-dom";
import "./Navbar.css";

const LINKS = [
  { to: "/", label: "Home" },
  { to: "/upload", label: "Upload" },
  { to: "/dashboard", label: "Dashboard" },
  { to: "/analysis", label: "Analysis" },
  { to: "/charts", label: "Charts" },
  { to: "/reports", label: "Reports" },
  { to: "/prediction", label: "Prediction" },
];

export default function Navbar() {
  return (
    <header className="navbar">
      <NavLink to="/" className="navbar-brand" end>
        <span className="navbar-brand-mark" aria-hidden="true">
          🌾
        </span>
        <span className="navbar-brand-text">
          Agri<span className="navbar-brand-accent">Vision</span>
        </span>
      </NavLink>

      <nav className="navbar-links" aria-label="Primary">
        {LINKS.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            className={({ isActive }) =>
              "navbar-link" + (isActive ? " navbar-link-active" : "")
            }
            end={link.to === "/"}
          >
            {link.label}
          </NavLink>
        ))}
      </nav>
    </header>
  );
}

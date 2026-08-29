import { Link } from "react-router-dom";
import "./Home.css";

const FEATURES = [
  { icon: "⬆️", label: "Upload", desc: "Bring in any agricultural CSV dataset." },
  { icon: "📊", label: "Analyze", desc: "Rows, missing data, duplicates, outliers." },
  { icon: "📈", label: "Visualize", desc: "Histograms, boxplots, heatmaps & more." },
  { icon: "📄", label: "Report", desc: "A shareable PDF report, generated for you." },
];

export default function Home() {
  return (
    <div className="page">
      <div
        className="page-bg"
        style={{ backgroundImage: "url(/images/hero.jpg)" }}
      />
      <div className="page-content home-content">
        <div className="home-hero">
          <span className="eyebrow">🌱 Agricultural Data Intelligence</span>
          <h1 className="home-title">
            See what your <em>fields</em> are telling you.
          </h1>
          <p className="home-subtitle">
            AgriVision turns raw agricultural datasets into clear statistics,
            visual charts, and downloadable reports — so patterns in
            rainfall, yield, and land use don't stay buried in a spreadsheet.
          </p>
          <div className="home-actions">
            <Link to="/upload" className="btn btn-primary">
              Upload a Dataset
            </Link>
            <Link to="/dashboard" className="btn btn-secondary">
              View Dashboard
            </Link>
          </div>
        </div>

        <div className="home-features">
          {FEATURES.map((f, i) => (
            <div className="home-feature glass-card" key={f.label}>
              <div className="hex-badge home-feature-badge" aria-hidden="true">
                {f.icon}
              </div>
              <div>
                <span className="home-feature-step">
                  {String(i + 1).padStart(2, "0")}
                </span>
                <h3 className="home-feature-title">{f.label}</h3>
                <p className="home-feature-desc">{f.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

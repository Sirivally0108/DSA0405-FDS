import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { fetchDatasets } from "../services/api.js";
import LoadingSpinner from "../components/LoadingSpinner.jsx";
import ErrorState from "../components/ErrorState.jsx";
import "./Dashboard.css";

export default function Dashboard() {
  const [datasets, setDatasets] = useState([]);
  const [status, setStatus] = useState("loading"); // loading | ready | error

  useEffect(() => {
    let cancelled = false;
    fetchDatasets()
      .then((data) => {
        if (!cancelled) {
          setDatasets(data);
          setStatus("ready");
        }
      })
      .catch(() => {
        if (!cancelled) setStatus("error");
      });
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <div className="page">
      <div
        className="page-bg"
        style={{ backgroundImage: "url(/images/dashboard.jpg)" }}
      />
      <div className="page-content dashboard-content">
        <span className="eyebrow">📊 Dashboard</span>
        <h1 className="section-title">Your datasets</h1>
        <p className="section-subtitle">
          Select a dataset to open its analysis, charts, and report.
        </p>

        {status === "loading" && (
          <LoadingSpinner label="Loading datasets..." />
        )}

        {status === "error" && (
          <ErrorState
            title="Unable to load datasets"
            message="Please make sure the backend is running."
          />
        )}

        {status === "ready" && datasets.length === 0 && (
          <div className="state-banner glass-card dashboard-empty">
            <h3>No datasets yet</h3>
            <p>Upload your first agricultural CSV to get started.</p>
            <Link to="/upload" className="btn btn-primary">
              Upload a Dataset
            </Link>
          </div>
        )}

        {status === "ready" && datasets.length > 0 && (
          <div className="dashboard-grid">
            {datasets.map((ds) => (
              <div className="dataset-card glass-card" key={ds.id}>
                <div className="dataset-card-header">
                  <div className="hex-badge" aria-hidden="true">
                    🌾
                  </div>
                  <div>
                    <h3 className="dataset-card-title">{ds.filename}</h3>
                    <span className="dataset-card-date">
                      Dataset ID: {ds.id}
                      {ds.upload_date
                        ? ` · ${new Date(ds.upload_date).toLocaleDateString()}`
                        : ""}
                    </span>
                  </div>
                </div>

                <div className="dataset-card-badges">
                  <span className="dataset-badge">{ds.rows.toLocaleString()} rows</span>
                  <span className="dataset-badge">{ds.columns} columns</span>
                  {ds.missing_values > 0 && (
                    <span className="dataset-badge dataset-badge-warn">
                      {ds.missing_values} missing
                    </span>
                  )}
                  {ds.duplicate_rows > 0 && (
                    <span className="dataset-badge dataset-badge-warn">
                      {ds.duplicate_rows} duplicates
                    </span>
                  )}
                </div>

                <Link
                  to={`/analysis?dataset=${ds.id}`}
                  className="btn btn-primary dataset-card-btn"
                >
                  Open Analysis
                </Link>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

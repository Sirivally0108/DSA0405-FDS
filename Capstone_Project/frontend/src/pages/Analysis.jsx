import { useEffect, useState } from "react";
import { useSearchParams, Link } from "react-router-dom";
import { fetchAnalysis } from "../services/api.js";
import StatCard from "../components/StatCard.jsx";
import LoadingSpinner from "../components/LoadingSpinner.jsx";
import ErrorState from "../components/ErrorState.jsx";
import "./Analysis.css";

export default function Analysis() {
  const [searchParams] = useSearchParams();
  const datasetId = searchParams.get("dataset");

  const [analysis, setAnalysis] = useState(null);
  const [status, setStatus] = useState("idle"); // idle | loading | ready | error

  useEffect(() => {
    if (!datasetId) {
      setStatus("idle");
      setAnalysis(null);
      return;
    }
    let cancelled = false;
    setStatus("loading");
    fetchAnalysis(datasetId)
      .then((data) => {
        if (!cancelled) {
          setAnalysis(data);
          setStatus("ready");
        }
      })
      .catch(() => {
        if (!cancelled) setStatus("error");
      });
    return () => {
      cancelled = true;
    };
  }, [datasetId]);

  return (
    <div className="page">
      <div
        className="page-bg"
        style={{ backgroundImage: "url(/images/analysis.jpg)" }}
      />
      <div className="page-content analysis-content">
        <span className="eyebrow">🔍 Analysis</span>
        <h1 className="section-title">Dataset analysis</h1>

        {!datasetId && (
          <ErrorState
            title="No dataset selected."
            message="Please select a dataset from the Dashboard."
            action={
              <Link to="/dashboard" className="btn btn-primary">
                Go to Dashboard
              </Link>
            }
          />
        )}

        {datasetId && status === "loading" && (
          <LoadingSpinner label="Loading analysis..." />
        )}

        {datasetId && status === "error" && (
          <ErrorState
            title="Unable to load analysis."
            message="Please make sure the backend is running."
          />
        )}

        {datasetId && status === "ready" && analysis && (
          <>
            <div className="analysis-meta glass-card">
              <div>
                <span className="analysis-meta-label">Dataset</span>
                <h2 className="analysis-meta-filename">{analysis.filename}</h2>
              </div>
              <span className="analysis-meta-id">
                Dataset ID: {analysis.id}
              </span>
            </div>

            <div className="analysis-stats-grid">
              <StatCard icon="📋" label="Rows" value={analysis.rows.toLocaleString()} tone="leaf" />
              <StatCard icon="📐" label="Columns" value={analysis.columns} tone="leaf" />
              <StatCard icon="🕳️" label="Missing Values" value={analysis.missing_values} tone="wheat" />
              <StatCard icon="🧬" label="Duplicate Rows" value={analysis.duplicate_rows} tone="wheat" />
              <StatCard icon="⚠️" label="Outliers" value={analysis.outliers} tone="clay" />
            </div>

            {analysis.stats?.describe && Object.keys(analysis.stats.describe).length > 0 && (
              <div className="analysis-table-wrap glass-card">
                <h3 className="analysis-table-title">Descriptive statistics</h3>
                <div className="analysis-table-scroll">
                  <table className="analysis-table">
                    <thead>
                      <tr>
                        <th>Field</th>
                        {Object.keys(
                          Object.values(analysis.stats.describe)[0] || {}
                        ).map((stat) => (
                          <th key={stat}>{stat}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {Object.entries(analysis.stats.describe).map(
                        ([col, stats]) => (
                          <tr key={col}>
                            <td className="analysis-table-col">{col}</td>
                            {Object.values(stats).map((v, i) => (
                              <td key={i}>{v === null ? "—" : v}</td>
                            ))}
                          </tr>
                        )
                      )}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            <div className="analysis-actions">
              <Link
                to={`/charts?dataset=${analysis.id}`}
                className="btn btn-primary"
              >
                View Charts
              </Link>
              <Link
                to={`/reports?dataset=${analysis.id}`}
                className="btn btn-gold"
              >
                View Report
              </Link>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

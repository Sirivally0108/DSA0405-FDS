import { useEffect, useState } from "react";
import { useSearchParams, Link } from "react-router-dom";
import { fetchAnalysis, resolveAssetUrl } from "../services/api.js";
import ChartCard from "../components/ChartCard.jsx";
import LoadingSpinner from "../components/LoadingSpinner.jsx";
import ErrorState from "../components/ErrorState.jsx";
import "./Charts.css";

export default function Charts() {
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

  // Normalize the backend's charts map — it's a flat { key: path } object,
  // not an array, and the set of keys can vary by dataset. Never assume a
  // fixed list of chart types.
  const chartEntries = analysis?.charts
    ? Object.entries(analysis.charts).filter(([, path]) => Boolean(path))
    : [];

  return (
    <div className="page">
      <div
        className="page-bg"
        style={{ backgroundImage: "url(/images/charts.jpg)" }}
      />
      <div className="page-content charts-content">
        <span className="eyebrow">📈 Data Visualization</span>
        <h1 className="section-title">Charts</h1>

        {!datasetId && (
          <ErrorState
            title="No dataset selected."
            message="Please select a dataset from Analysis."
            action={
              <Link to="/dashboard" className="btn btn-primary">
                Go to Dashboard
              </Link>
            }
          />
        )}

        {datasetId && status === "loading" && (
          <LoadingSpinner label="Loading charts..." />
        )}

        {datasetId && status === "error" && (
          <ErrorState
            title="Unable to load charts."
            message="Please make sure the backend is running."
          />
        )}

        {datasetId && status === "ready" && analysis && (
          <>
            <p className="charts-meta">
              Dataset: {analysis.filename} · Dataset ID: {analysis.id}
            </p>

            {chartEntries.length === 0 ? (
              <ErrorState
                title="No charts are available for this dataset."
                message="Try re-uploading the dataset, or check back once processing finishes."
              />
            ) : (
              <div className="charts-grid">
                {chartEntries.map(([key, path]) => (
                  <ChartCard
                    key={key}
                    chartKey={key}
                    imageUrl={resolveAssetUrl(path)}
                  />
                ))}
              </div>
            )}

            <div className="charts-actions">
              <Link
                to={`/analysis?dataset=${analysis.id}`}
                className="btn btn-secondary"
              >
                Back to Analysis
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

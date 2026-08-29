import { useEffect, useState } from "react";
import { useSearchParams, Link } from "react-router-dom";
import { fetchAnalysis, resolveAssetUrl } from "../services/api.js";
import LoadingSpinner from "../components/LoadingSpinner.jsx";
import ErrorState from "../components/ErrorState.jsx";
import "./Reports.css";

export default function Reports() {
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

  const reportUrl = analysis?.report ? resolveAssetUrl(analysis.report) : null;

  return (
    <div className="page">
      <div
        className="page-bg"
        style={{ backgroundImage: "url(/images/analysis.jpg)" }}
      />
      <div className="page-content reports-content">
        <span className="eyebrow">📄 Reports</span>
        <h1 className="section-title">Dataset report</h1>

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
          <LoadingSpinner label="Loading report..." />
        )}

        {datasetId && status === "error" && (
          <ErrorState
            title="Unable to load report."
            message="Please make sure the backend is running."
          />
        )}

        {datasetId && status === "ready" && analysis && !reportUrl && (
          <ErrorState
            title="No report is available for this dataset."
            message="Try re-uploading the dataset so a report can be generated."
          />
        )}

        {datasetId && status === "ready" && analysis && reportUrl && (
          <div className="report-card glass-card">
            <div className="hex-badge report-hex" aria-hidden="true">
              📄
            </div>
            <div className="report-info">
              <h3 className="report-filename">{analysis.filename}</h3>
              <span className="report-meta-id">Dataset ID: {analysis.id}</span>
              <p className="report-desc">
                A generated PDF covering dataset summary statistics,
                descriptive analysis, and every chart produced for this
                dataset.
              </p>
            </div>
            <div className="report-actions">
              <a
                href={reportUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-primary"
              >
                View Report
              </a>
              <a href={reportUrl} download className="btn btn-gold">
                Download Report
              </a>
            </div>
          </div>
        )}

        {datasetId && status === "ready" && (
          <div className="reports-actions">
            <Link
              to={`/analysis?dataset=${datasetId}`}
              className="btn btn-secondary"
            >
              Back to Analysis
            </Link>
            <Link to={`/charts?dataset=${datasetId}`} className="btn btn-secondary">
              View Charts
            </Link>
          </div>
        )}
      </div>
    </div>
  );
}

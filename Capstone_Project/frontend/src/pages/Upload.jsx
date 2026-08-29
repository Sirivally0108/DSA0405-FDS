import { useCallback, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { uploadDataset } from "../services/api.js";
import "./Upload.css";

export default function Upload() {
  const [file, setFile] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState("idle"); // idle | uploading | success | error
  const [errorMessage, setErrorMessage] = useState("");
  const [result, setResult] = useState(null);
  const inputRef = useRef(null);
  const navigate = useNavigate();

  const pickFile = useCallback((selected) => {
    if (!selected) return;
    if (!selected.name.toLowerCase().endsWith(".csv")) {
      setStatus("error");
      setErrorMessage("Please choose a .csv file.");
      return;
    }
    setFile(selected);
    setStatus("idle");
    setErrorMessage("");
    setResult(null);
  }, []);

  const handleDrop = (e) => {
    e.preventDefault();
    setDragActive(false);
    pickFile(e.dataTransfer.files?.[0]);
  };

  const handleUpload = async () => {
    if (!file) return;
    setStatus("uploading");
    setProgress(0);
    setErrorMessage("");
    try {
      const data = await uploadDataset(file, setProgress);
      setResult(data);
      setStatus("success");
    } catch (err) {
      setStatus("error");
      setErrorMessage(
        err?.response?.data?.detail ||
          "Upload failed. Please make sure the backend is running."
      );
    }
  };

  return (
    <div className="page">
      <div
        className="page-bg"
        style={{ backgroundImage: "url(/images/dashboard.jpg)" }}
      />
      <div className="page-content upload-content">
        <span className="eyebrow">⬆️ Upload Dataset</span>
        <h1 className="section-title">Bring in a new agricultural dataset</h1>
        <p className="section-subtitle">
          Upload a CSV file. AgriVision will process it, compute statistics,
          generate charts, and build a report you can explore afterward.
        </p>

        <div
          className={
            "upload-dropzone glass-card" + (dragActive ? " dropzone-active" : "")
          }
          onDragOver={(e) => {
            e.preventDefault();
            setDragActive(true);
          }}
          onDragLeave={() => setDragActive(false)}
          onDrop={handleDrop}
          onClick={() => inputRef.current?.click()}
          role="button"
          tabIndex={0}
          onKeyDown={(e) => {
            if (e.key === "Enter" || e.key === " ") inputRef.current?.click();
          }}
        >
          <input
            ref={inputRef}
            type="file"
            accept=".csv"
            hidden
            onChange={(e) => pickFile(e.target.files?.[0])}
          />
          <div className="hex-badge upload-hex" aria-hidden="true">
            📄
          </div>
          {file ? (
            <>
              <p className="upload-filename">{file.name}</p>
              <p className="upload-hint">
                {(file.size / 1024).toFixed(1)} KB — click to choose a
                different file
              </p>
            </>
          ) : (
            <>
              <p className="upload-filename">
                Drag & drop a CSV file here, or click to browse
              </p>
              <p className="upload-hint">Accepted format: .csv</p>
            </>
          )}
        </div>

        {status === "uploading" && (
          <div className="upload-progress-wrap">
            <div className="upload-progress-bar">
              <div
                className="upload-progress-fill"
                style={{ width: `${progress}%` }}
              />
            </div>
            <span className="upload-progress-label">
              Processing dataset… {progress}%
            </span>
          </div>
        )}

        {status === "error" && (
          <div className="state-banner error glass-card upload-banner">
            <h3>Upload failed</h3>
            <p>{errorMessage}</p>
          </div>
        )}

        {status === "success" && result && (
          <div className="state-banner glass-card upload-banner upload-success">
            <h3>Dataset uploaded successfully</h3>
            <p>
              {result.filename} — {result.rows.toLocaleString()} rows,{" "}
              {result.columns} columns. Charts and report have been
              generated.
            </p>
            <div className="upload-success-actions">
              <button
                className="btn btn-primary"
                onClick={() => navigate(`/analysis?dataset=${result.id}`)}
              >
                View Analysis
              </button>
              <button
                className="btn btn-secondary"
                onClick={() => navigate("/dashboard")}
              >
                Go to Dashboard
              </button>
            </div>
          </div>
        )}

        <div className="upload-actions">
          <button
            className="btn btn-primary"
            disabled={!file || status === "uploading"}
            onClick={handleUpload}
          >
            {status === "uploading" ? "Uploading…" : "Upload Dataset"}
          </button>
        </div>
      </div>
    </div>
  );
}

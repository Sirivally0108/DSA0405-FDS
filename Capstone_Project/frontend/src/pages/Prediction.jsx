import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
  fetchDatasets,
  fetchDatasetColumns,
  runPrediction,
} from "../services/api.js";
import LoadingSpinner from "../components/LoadingSpinner.jsx";
import ErrorState from "../components/ErrorState.jsx";
import "./Prediction.css";

export default function Prediction() {
  const [datasets, setDatasets] = useState([]);
  const [datasetsStatus, setDatasetsStatus] = useState("loading");

  const [selectedDataset, setSelectedDataset] = useState("");
  const [numericColumns, setNumericColumns] = useState([]);
  const [columnsStatus, setColumnsStatus] = useState("idle");

  const [targetColumn, setTargetColumn] = useState("");
  const [featureValues, setFeatureValues] = useState({});

  const [predictStatus, setPredictStatus] = useState("idle"); // idle | loading | ready | error
  const [predictResult, setPredictResult] = useState(null);
  const [predictError, setPredictError] = useState("");

  useEffect(() => {
    fetchDatasets()
      .then((data) => {
        setDatasets(data);
        setDatasetsStatus("ready");
      })
      .catch(() => setDatasetsStatus("error"));
  }, []);

  useEffect(() => {
    if (!selectedDataset) {
      setNumericColumns([]);
      setTargetColumn("");
      return;
    }
    setColumnsStatus("loading");
    fetchDatasetColumns(selectedDataset)
      .then((data) => {
        setNumericColumns(data.numeric_columns || []);
        setTargetColumn(data.numeric_columns?.[0] || "");
        setColumnsStatus("ready");
      })
      .catch(() => setColumnsStatus("error"));
  }, [selectedDataset]);

  const featureColumns = numericColumns.filter((c) => c !== targetColumn);

  const handlePredict = async (e) => {
    e.preventDefault();
    setPredictStatus("loading");
    setPredictError("");
    try {
      const result = await runPrediction({
        datasetId: selectedDataset,
        targetColumn,
        features: featureValues,
      });
      setPredictResult(result);
      setPredictStatus("ready");
    } catch (err) {
      setPredictStatus("error");
      setPredictError(
        err?.response?.data?.detail ||
          "Prediction failed. Please make sure the backend is running."
      );
    }
  };

  return (
    <div className="page">
      <div
        className="page-bg"
        style={{ backgroundImage: "url(/images/charts.jpg)" }}
      />
      <div className="page-content prediction-content">
        <span className="eyebrow">🔮 Prediction</span>
        <h1 className="section-title">Predict a field value</h1>
        <p className="section-subtitle">
          Pick a dataset and a numeric field to predict, then fill in the
          other numeric fields to get an estimate from a fitted model.
        </p>

        {datasetsStatus === "loading" && (
          <LoadingSpinner label="Loading datasets..." />
        )}

        {datasetsStatus === "error" && (
          <ErrorState
            title="Unable to load datasets."
            message="Please make sure the backend is running."
          />
        )}

        {datasetsStatus === "ready" && datasets.length === 0 && (
          <div className="state-banner glass-card prediction-empty">
            <h3>No datasets yet</h3>
            <p>Upload a dataset before running a prediction.</p>
            <Link to="/upload" className="btn btn-primary">
              Upload a Dataset
            </Link>
          </div>
        )}

        {datasetsStatus === "ready" && datasets.length > 0 && (
          <form className="prediction-form glass-card" onSubmit={handlePredict}>
            <label className="prediction-field">
              <span>Dataset</span>
              <select
                value={selectedDataset}
                onChange={(e) => {
                  setSelectedDataset(e.target.value);
                  setPredictResult(null);
                  setPredictStatus("idle");
                }}
                required
              >
                <option value="" disabled>
                  Select a dataset
                </option>
                {datasets.map((ds) => (
                  <option key={ds.id} value={ds.id}>
                    {ds.filename} (ID: {ds.id})
                  </option>
                ))}
              </select>
            </label>

            {columnsStatus === "loading" && (
              <p className="prediction-hint">Loading fields…</p>
            )}

            {columnsStatus === "ready" && numericColumns.length < 2 && (
              <ErrorState
                title="Not enough numeric fields."
                message="This dataset needs at least two numeric columns to run a prediction."
              />
            )}

            {columnsStatus === "ready" && numericColumns.length >= 2 && (
              <>
                <label className="prediction-field">
                  <span>Field to predict</span>
                  <select
                    value={targetColumn}
                    onChange={(e) => setTargetColumn(e.target.value)}
                  >
                    {numericColumns.map((c) => (
                      <option key={c} value={c}>
                        {c}
                      </option>
                    ))}
                  </select>
                </label>

                <div className="prediction-features">
                  {featureColumns.map((col) => (
                    <label className="prediction-field" key={col}>
                      <span>{col}</span>
                      <input
                        type="number"
                        step="any"
                        placeholder="Enter a value"
                        value={featureValues[col] ?? ""}
                        onChange={(e) =>
                          setFeatureValues((prev) => ({
                            ...prev,
                            [col]: e.target.value,
                          }))
                        }
                        required
                      />
                    </label>
                  ))}
                </div>

                <button
                  type="submit"
                  className="btn btn-primary"
                  disabled={predictStatus === "loading"}
                >
                  {predictStatus === "loading" ? "Predicting…" : "Run Prediction"}
                </button>
              </>
            )}

            {predictStatus === "error" && (
              <div className="state-banner error prediction-result-error">
                <p>{predictError}</p>
              </div>
            )}

            {predictStatus === "ready" && predictResult && (
              <div className="prediction-result">
                <span className="prediction-result-label">
                  Predicted {predictResult.target_column}
                </span>
                <span className="prediction-result-value">
                  {predictResult.predicted_value.toLocaleString(undefined, {
                    maximumFractionDigits: 2,
                  })}
                </span>
                <span className="prediction-result-meta">
                  Model fit R² {predictResult.r_squared} · trained on{" "}
                  {predictResult.sample_size} rows using{" "}
                  {predictResult.features_used.join(", ")}
                </span>
              </div>
            )}
          </form>
        )}
      </div>
    </div>
  );
}

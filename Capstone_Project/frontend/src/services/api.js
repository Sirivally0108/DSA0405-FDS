import axios from "axios";

// Single backend base URL, read from the env variable when present so the
// project can point at a different backend host without code changes.
export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

const client = axios.create({
  baseURL: API_BASE_URL,
});

/**
 * Backend-generated file paths (charts, reports) come back as
 * root-relative paths like "/charts/dataset_6/histogram.png" or
 * "/report/My_report.pdf". This turns them into an absolute URL against
 * the API host without ever double-prefixing an already-absolute URL.
 */
export function resolveAssetUrl(path) {
  if (!path) return null;
  if (/^https?:\/\//i.test(path)) return path;
  return `${API_BASE_URL}${path.startsWith("/") ? "" : "/"}${path}`;
}

export async function uploadDataset(file, onProgress) {
  const formData = new FormData();
  formData.append("file", file);
  const { data } = await client.post("/api/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
    onUploadProgress: (evt) => {
      if (onProgress && evt.total) {
        onProgress(Math.round((evt.loaded * 100) / evt.total));
      }
    },
  });
  return data;
}

export async function fetchDatasets() {
  const { data } = await client.get("/api/datasets");
  return data;
}

export async function fetchAnalysis(datasetId) {
  const { data } = await client.get(`/api/analysis/${datasetId}`);
  return data;
}

export async function fetchDatasetColumns(datasetId) {
  const { data } = await client.get(`/api/datasets/${datasetId}/columns`);
  return data;
}

export async function runPrediction({ datasetId, targetColumn, features }) {
  const { data } = await client.post("/api/predict", {
    dataset_id: datasetId,
    target_column: targetColumn,
    features,
  });
  return data;
}

export default client;

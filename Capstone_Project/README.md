# AgriVision

An agricultural dataset analysis platform: upload a CSV, get statistics,
generated charts, and a downloadable PDF report.

- **Backend:** Python / FastAPI (pandas + numpy + matplotlib for
  analysis, chart generation, and report generation), SQLite for dataset
  metadata.
- **Frontend:** React + Vite, React Router, Axios.

## Project structure

```
agrivision/
  backend/
    main.py            FastAPI app & routes
    processing.py       analysis, chart generation, PDF report generation
    database.py         SQLite persistence for dataset metadata
    requirements.txt
    storage/
      uploads/           raw uploaded CSVs
      charts/dataset_<id>/  generated chart PNGs
      reports/           generated PDF reports
  frontend/
    src/
      pages/             Home, Upload, Dashboard, Analysis, Charts, Reports, Prediction
      components/        Navbar, StatCard, ChartCard, LoadingSpinner, ErrorState
      services/api.js     single place all backend calls go through
    public/images/       hero.jpg, dashboard.jpg, analysis.jpg, charts.jpg
```

## 1. Run the backend

```bash
cd agrivision
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt
python -m uvicorn backend.main:app --reload
```

The API runs at `http://127.0.0.1:8000`. Uploaded files, generated
charts, and reports are stored under `backend/storage/`; dataset
metadata lives in `backend/agrivision.db` (created automatically).

## 2. Run the frontend

```bash
cd agrivision/frontend
npm install
npm run dev
```

The app runs at `http://localhost:5173`. It talks to the backend via
`VITE_API_BASE_URL` in `frontend/.env` (defaults to
`http://127.0.0.1:8000`).

## 3. Try it out

1. Open `http://localhost:5173/` — home page.
2. Go to **Upload**, drop in a CSV (any agricultural dataset — column
   names aren't hard-coded anywhere).
3. You'll land on **Analysis** for the new dataset
   (`/analysis?dataset=<id>`), showing rows, columns, missing values,
   duplicates, outliers, and descriptive stats.
4. Click **View Charts** → `/charts?dataset=<id>` to see the generated
   histogram, box plot, scatter plot, correlation heatmap, and bar
   chart.
5. Click **View Report** → `/reports?dataset=<id>` to view or download
   the generated PDF.
6. **Dashboard** lists every uploaded dataset so you can jump back into
   any of them later.
7. **Prediction** lets you pick a dataset and a numeric field, fill in
   the other numeric fields, and get an estimate from a small
   regression model fit on the fly.

## Notes on how the dataset-ID flow works

Every page that needs a dataset reads it from the `?dataset=` query
param via `useSearchParams`. Analysis → Charts and Analysis → Reports
links always carry the id forward (`/charts?dataset=${id}`), so it's
never dropped or replaced with `null`. Visiting `/charts` or `/reports`
directly with no query param shows a clear "No dataset selected" state
instead of a blank page or a silent failure.

## Notes on chart handling

The backend returns charts as a flat map, e.g.:

```json
{
  "histogram": "/charts/dataset_6/histogram.png",
  "boxplot": "/charts/dataset_6/boxplot.png",
  "scatter": "/charts/dataset_6/scatter.png",
  "heatmap": "/charts/dataset_6/heatmap.png",
  "bar_chart": "/charts/dataset_6/bar_chart.png"
}
```

The frontend (`Charts.jsx`) iterates `Object.entries(charts)` rather
than assuming a fixed set of keys, so adding or removing a chart type
on the backend needs no frontend change. `resolveAssetUrl()` in
`services/api.js` prepends the API base URL to these root-relative
paths without ever double-prefixing an already-absolute URL.

## Building for production

```bash
cd frontend
npm run build
```

Outputs to `frontend/dist/`.

"""
processing.py — turns a raw uploaded CSV into the analysis payload the
frontend expects: summary stats, per-column detail, generated chart
images, and a PDF report.

Kept dependency-light on purpose: pandas + numpy + matplotlib only, so the
backend can run with nothing more exotic than `pip install -r requirements.txt`.
"""

import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless — no display server on the backend host
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

import numpy as np
import pandas as pd

# Green/earth palette so generated charts match the AgriVision identity
# instead of matplotlib's default blue/orange.
PALETTE = ["#3F8F5C", "#E8B84B", "#5EA8D9", "#B4573A", "#8FD7A8", "#123524"]
plt.rcParams.update(
    {
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.edgecolor": "#2A3B32",
        "axes.labelcolor": "#1A2420",
        "text.color": "#1A2420",
        "xtick.color": "#3A4B42",
        "ytick.color": "#3A4B42",
        "axes.grid": True,
        "grid.color": "#E4E7DF",
        "grid.linewidth": 0.6,
        "font.size": 10,
        "axes.titleweight": "bold",
    }
)


def _clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    return df


def analyze_dataset(df: pd.DataFrame) -> dict:
    """Compute the statistics block described in the AgriVision spec:
    rows, columns, missing values, duplicate rows, outliers, and
    descriptive statistics for numeric columns.
    """
    df = _clean_dataframe(df)
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = [c for c in df.columns if c not in numeric_cols]

    missing_per_column = df.isna().sum()
    total_missing = int(missing_per_column.sum())

    duplicate_rows = int(df.duplicated().sum())

    outliers_per_column = {}
    total_outliers = 0
    for col in numeric_cols:
        series = df[col].dropna()
        if series.empty:
            outliers_per_column[col] = 0
            continue
        q1, q3 = series.quantile(0.25), series.quantile(0.75)
        iqr = q3 - q1
        if iqr == 0 or math.isnan(iqr):
            outliers_per_column[col] = 0
            continue
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        count = int(((series < lower) | (series > upper)).sum())
        outliers_per_column[col] = count
        total_outliers += count

    describe = {}
    if numeric_cols:
        desc_df = df[numeric_cols].describe().round(3)
        for col in numeric_cols:
            describe[col] = {
                stat: (None if pd.isna(val) else float(val))
                for stat, val in desc_df[col].items()
            }

    column_types = {col: str(df[col].dtype) for col in df.columns}

    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": df.columns.tolist(),
        "numeric_columns": numeric_cols,
        "categorical_columns": categorical_cols,
        "column_types": column_types,
        "missing_values": total_missing,
        "missing_per_column": {k: int(v) for k, v in missing_per_column.items()},
        "duplicate_rows": duplicate_rows,
        "outliers": total_outliers,
        "outliers_per_column": outliers_per_column,
        "describe": describe,
    }


def generate_charts(df: pd.DataFrame, dataset_id: int, charts_root: Path) -> dict:
    """Generate the chart set and return a flat {chart_key: url_path} map,
    matching the backend contract in the AgriVision spec — simple
    key/value chart paths, not arrays.
    """
    df = _clean_dataframe(df)
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = [c for c in df.columns if c not in numeric_cols]

    out_dir = charts_root / f"dataset_{dataset_id}"
    out_dir.mkdir(parents=True, exist_ok=True)
    charts: dict = {}

    # ---- Histogram: small multiples over up to 6 numeric columns ----
    if numeric_cols:
        cols = numeric_cols[:6]
        n = len(cols)
        grid_cols = min(3, n)
        grid_rows = math.ceil(n / grid_cols)
        fig, axes = plt.subplots(
            grid_rows, grid_cols, figsize=(4.2 * grid_cols, 3.4 * grid_rows)
        )
        axes = np.atleast_1d(axes).flatten()
        for i, col in enumerate(cols):
            axes[i].hist(
                df[col].dropna(), bins=20, color=PALETTE[i % len(PALETTE)],
                edgecolor="white",
            )
            axes[i].set_title(col, fontsize=10)
        for j in range(len(cols), len(axes)):
            axes[j].axis("off")
        fig.suptitle("Distribution of Numeric Fields", fontsize=13, y=1.02)
        fig.tight_layout()
        path = out_dir / "histogram.png"
        fig.savefig(path, dpi=140, bbox_inches="tight")
        plt.close(fig)
        charts["histogram"] = f"/charts/dataset_{dataset_id}/histogram.png"

    # ---- Box plot across numeric columns ----
    if numeric_cols:
        cols = numeric_cols[:8]
        fig, ax = plt.subplots(figsize=(max(6, 1.2 * len(cols)), 5))
        data = [df[c].dropna() for c in cols]
        # matplotlib renamed boxplot's `labels` kwarg to `tick_labels` in
        # 3.9+; set tick labels manually afterward instead so this works
        # on any matplotlib version.
        bp = ax.boxplot(data, patch_artist=True)
        ax.set_xticks(range(1, len(cols) + 1))
        ax.set_xticklabels(cols)
        for i, box in enumerate(bp["boxes"]):
            box.set_facecolor(PALETTE[i % len(PALETTE)])
            box.set_alpha(0.75)
        ax.set_title("Spread & Outliers by Field")
        plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
        fig.tight_layout()
        path = out_dir / "boxplot.png"
        fig.savefig(path, dpi=140, bbox_inches="tight")
        plt.close(fig)
        charts["boxplot"] = f"/charts/dataset_{dataset_id}/boxplot.png"

    # ---- Scatter of the first two numeric columns ----
    if len(numeric_cols) >= 2:
        x_col, y_col = numeric_cols[0], numeric_cols[1]
        fig, ax = plt.subplots(figsize=(6, 5))
        ax.scatter(
            df[x_col], df[y_col], color=PALETTE[2], alpha=0.65,
            edgecolors="white", linewidths=0.4, s=40,
        )
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_title(f"{y_col} vs {x_col}")
        fig.tight_layout()
        path = out_dir / "scatter.png"
        fig.savefig(path, dpi=140, bbox_inches="tight")
        plt.close(fig)
        charts["scatter"] = f"/charts/dataset_{dataset_id}/scatter.png"

    # ---- Correlation heatmap ----
    if len(numeric_cols) >= 2:
        corr = df[numeric_cols].corr()
        fig, ax = plt.subplots(
            figsize=(max(5, 0.6 * len(numeric_cols) + 2), max(4.5, 0.6 * len(numeric_cols) + 2))
        )
        im = ax.imshow(corr.values, cmap="YlGn", vmin=-1, vmax=1)
        ax.set_xticks(range(len(numeric_cols)))
        ax.set_yticks(range(len(numeric_cols)))
        ax.set_xticklabels(numeric_cols, rotation=45, ha="right", fontsize=8)
        ax.set_yticklabels(numeric_cols, fontsize=8)
        for i in range(len(numeric_cols)):
            for j in range(len(numeric_cols)):
                ax.text(
                    j, i, f"{corr.values[i, j]:.2f}", ha="center", va="center",
                    fontsize=7,
                    color="white" if abs(corr.values[i, j]) > 0.5 else "#1A2420",
                )
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        ax.set_title("Correlation Heatmap")
        fig.tight_layout()
        path = out_dir / "heatmap.png"
        fig.savefig(path, dpi=140, bbox_inches="tight")
        plt.close(fig)
        charts["heatmap"] = f"/charts/dataset_{dataset_id}/heatmap.png"

    # ---- Bar chart: top categorical column value counts, else column means ----
    fig, ax = plt.subplots(figsize=(7, 5))
    if categorical_cols:
        col = categorical_cols[0]
        counts = df[col].value_counts().head(10)
        ax.bar(counts.index.astype(str), counts.values, color=PALETTE[0])
        ax.set_title(f"Top Values — {col}")
        ax.set_ylabel("Count")
        plt.setp(ax.get_xticklabels(), rotation=35, ha="right")
    elif numeric_cols:
        cols = numeric_cols[:10]
        means = df[cols].mean()
        ax.bar(means.index.astype(str), means.values, color=PALETTE[0])
        ax.set_title("Average Value by Field")
        ax.set_ylabel("Mean")
        plt.setp(ax.get_xticklabels(), rotation=35, ha="right")
    else:
        ax.text(0.5, 0.5, "No data available", ha="center", va="center")
        ax.axis("off")
    fig.tight_layout()
    path = out_dir / "bar_chart.png"
    fig.savefig(path, dpi=140, bbox_inches="tight")
    plt.close(fig)
    charts["bar_chart"] = f"/charts/dataset_{dataset_id}/bar_chart.png"

    return charts


def generate_report(
    df: pd.DataFrame,
    analysis: dict,
    dataset_id: int,
    original_filename: str,
    charts_root: Path,
    reports_root: Path,
) -> str:
    """Build a multi-page PDF report (title/summary page + one page per
    chart) and return its URL path, matching the `/report/<file>.pdf`
    contract in the spec.
    """
    reports_root.mkdir(parents=True, exist_ok=True)
    stem = Path(original_filename).stem
    report_filename = f"{stem}_report.pdf"
    report_path = reports_root / report_filename

    chart_dir = charts_root / f"dataset_{dataset_id}"

    PAGE_SIZE = (8.5, 11)
    MARGIN_LEFT = 0.07
    MARGIN_RIGHT = 0.95
    LINE_H = 0.028  # vertical space per text line, in axes fraction

    def new_page():
        fig, ax = plt.subplots(figsize=PAGE_SIZE)
        ax.axis("off")
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        return fig, ax

    with PdfPages(report_path) as pdf:
        # ---- Title / summary page ----
        fig, ax = new_page()
        y = 0.95
        ax.text(MARGIN_LEFT, y, "AgriVision Dataset Report", fontsize=20, fontweight="bold", va="top")
        y -= 0.05
        ax.text(
            MARGIN_LEFT, y,
            f"Dataset: {original_filename}    ·    Dataset ID: {dataset_id}",
            fontsize=11, color="#3a4b42", va="top",
        )
        y -= 0.05

        # Summary numbers as a small aligned two-column table, not
        # free-floating text.
        summary_rows = [
            ("Rows", f"{analysis['rows']:,}"),
            ("Columns", f"{analysis['columns']}"),
            ("Missing values", f"{analysis['missing_values']:,}"),
            ("Duplicate rows", f"{analysis['duplicate_rows']:,}"),
            ("Outliers detected", f"{analysis['outliers']:,}"),
        ]
        summary_table = ax.table(
            cellText=[[label, value] for label, value in summary_rows],
            colWidths=[0.28, 0.18],
            cellLoc="left",
            bbox=[MARGIN_LEFT, y - 0.18, 0.46, 0.18],
        )
        summary_table.auto_set_font_size(False)
        summary_table.set_fontsize(10.5)
        for (row, col), cell in summary_table.get_celld().items():
            cell.set_edgecolor("#E4E7DF")
            cell.set_text_props(
                fontweight="bold" if col == 0 else "normal",
                color="#1A2420",
            )
            cell.PAD = 0.04
        y -= 0.18 + 0.04

        ax.text(MARGIN_LEFT, y, "Column summary", fontsize=13, fontweight="bold", va="top")
        y -= 0.032

        # Column summary as an aligned table: name / dtype / missing —
        # instead of a bullet line whose length varies per column.
        col_rows = []
        for col in analysis["column_names"]:
            dtype = analysis["column_types"].get(col, "")
            missing = analysis["missing_per_column"].get(col, 0)
            col_rows.append([col, dtype, str(missing)])

        rows_per_page = 14
        while col_rows:
            chunk, col_rows = col_rows[:rows_per_page], col_rows[rows_per_page:]
            table_height = 0.045 * (len(chunk) + 1)
            if y - table_height < 0.05:
                pdf.savefig(fig)
                plt.close(fig)
                fig, ax = new_page()
                y = 0.95

            col_table = ax.table(
                cellText=chunk,
                colLabels=["Column", "Type", "Missing"],
                colWidths=[0.42, 0.2, 0.18],
                cellLoc="left",
                bbox=[MARGIN_LEFT, y - table_height, 0.8, table_height],
            )
            col_table.auto_set_font_size(False)
            col_table.set_fontsize(9.5)
            for (row, col), cell in col_table.get_celld().items():
                cell.set_edgecolor("#E4E7DF")
                cell.PAD = 0.035
                if row == 0:
                    cell.set_facecolor("#EEF2E7")
                    cell.set_text_props(fontweight="bold", color="#123524")
                else:
                    cell.set_text_props(color="#1A2420")
            y -= table_height + 0.03

        pdf.savefig(fig)
        plt.close(fig)

        # ---- Descriptive statistics page(s) ----
        # A real grid table (fields as rows, stats as columns) instead of
        # a concatenated string, so nothing runs off the page edge.
        if analysis["describe"]:
            stat_keys = list(next(iter(analysis["describe"].values())).keys())
            SHORT_LABELS = {"25%": "p25", "50%": "p50", "75%": "p75"}
            header = ["Field"] + [SHORT_LABELS.get(k, k) for k in stat_keys]
            body_rows = []
            for col, stats in analysis["describe"].items():
                row = [col]
                for k in stat_keys:
                    v = stats.get(k)
                    if v is None:
                        row.append("—")
                    elif abs(v) >= 1000:
                        row.append(f"{v:,.0f}")
                    else:
                        row.append(f"{v:,.2f}")
                body_rows.append(row)

            fig, ax = new_page()
            y = 0.95
            ax.text(MARGIN_LEFT, y, "Descriptive Statistics", fontsize=16, fontweight="bold", va="top")
            y -= 0.05

            longest_name = max((len(col) for col in analysis["describe"]), default=8)
            first_col_w = min(0.34, max(0.16, 0.011 * longest_name))
            other_col_w = (MARGIN_RIGHT - MARGIN_LEFT - first_col_w) / len(stat_keys)
            col_widths = [first_col_w] + [other_col_w] * len(stat_keys)

            rows_per_page = 9
            remaining = body_rows
            while remaining:
                chunk, remaining = remaining[:rows_per_page], remaining[rows_per_page:]
                table_height = 0.045 * (len(chunk) + 1)
                if y - table_height < 0.05:
                    pdf.savefig(fig)
                    plt.close(fig)
                    fig, ax = new_page()
                    y = 0.95

                stats_table = ax.table(
                    cellText=chunk,
                    colLabels=header,
                    colWidths=col_widths,
                    cellLoc="right",
                    bbox=[MARGIN_LEFT, y - table_height, MARGIN_RIGHT - MARGIN_LEFT, table_height],
                )
                stats_table.auto_set_font_size(False)
                stats_table.set_fontsize(8.5)
                for (row, col), cell in stats_table.get_celld().items():
                    cell.set_edgecolor("#E4E7DF")
                    cell.PAD = 0.05
                    if row == 0:
                        cell.set_facecolor("#EEF2E7")
                        cell.set_text_props(fontweight="bold", color="#123524")
                        if col == 0:
                            cell.get_text().set_ha("left")
                            cell.get_text().set_x(0.03)
                    elif col == 0:
                        cell.set_text_props(fontweight="bold", color="#1A2420")
                        cell.get_text().set_ha("left")
                        cell.get_text().set_x(0.03)
                    else:
                        cell.set_text_props(color="#1A2420")
                y -= table_height + 0.03

            pdf.savefig(fig)
            plt.close(fig)

        # ---- One page per generated chart image ----
        if chart_dir.exists():
            for chart_file in sorted(chart_dir.glob("*.png")):
                img = plt.imread(chart_file)
                fig, ax = plt.subplots(figsize=(8.5, 11))
                ax.imshow(img)
                ax.axis("off")
                ax.set_title(chart_file.stem.replace("_", " ").title(), fontsize=14)
                pdf.savefig(fig)
                plt.close(fig)

    return f"/report/{report_filename}"

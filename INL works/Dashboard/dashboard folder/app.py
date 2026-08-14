from __future__ import annotations

"""Simple Flask dashboard for the Schemagent workflow.

This is an initial, non-production prototype that:

* Renders a teal/black dashboard UI.
* Exposes seven main buttons representing the workflow steps.
* Shows static previews from the existing resource folders.
* Reads validation metrics from the CSV in "Result scores".
* Lets the user download the precomputed connectivity matrix.

Later, the fake operations can be replaced with real backend
processing using the same layout and routes.
"""

from pathlib import Path
import csv

from flask import (
    Flask,
    render_template,
    send_from_directory,
    send_file,
    abort,
)


BASE_DIR = Path(__file__).resolve().parent
# This is C:\Asif_all_python_projects\INL\Dashboard
RESOURCES_DIR = BASE_DIR.parent


app = Flask(__name__)


def _safe_path(*parts: str) -> Path:
    """Build a path under RESOURCES_DIR and ensure it exists.

    This keeps all file access scoped to the known Dashboard
    resources directory.
    """

    path = RESOURCES_DIR.joinpath(*parts)
    if not path.exists():
        raise FileNotFoundError(str(path))
    return path


def load_validation_metrics() -> dict | None:
    """Read TP/FP/FN/Precision/Recall/F1 from the CSV file.

    The expected file lives in:
    Dashboard/Result scores/connectivity_matrix_validation_metrics.csv
    """

    try:
        csv_path = _safe_path(
            "Result scores", "connectivity_matrix_validation_metrics.csv"
        )
    except FileNotFoundError:
        return None

    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        return None

    row = rows[0]

    def _get_number(key: str, cast):
        raw_val = row.get(key)
        if raw_val is None or raw_val == "":
            return None
        try:
            return cast(raw_val)
        except ValueError:
            return None

    return {
        "extractor": row.get("Extractor_name -- Round no."),
        "tp": _get_number("TP", int),
        "fp": _get_number("FP", int),
        "fn": _get_number("FN", int),
        "precision": _get_number("Precision", float),
        "recall": _get_number("Recall", float),
        "f1": _get_number("F1 score", float),
    }


def load_connectivity_matrix_summary() -> dict | None:
    """Return a lightweight summary of the connectivity matrix.

    This keeps the dashboard responsive by avoiding sending the
    full matrix to the browser.
    """

    try:
        csv_path = _safe_path("Result connectivity matrix", "connectivity_matrix.csv")
    except FileNotFoundError:
        return None

    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    if not rows:
        return None

    header = rows[0]
    # First column is the node name; the remaining columns are matrix columns.
    num_rows = max(len(rows) - 1, 0)

    # Count all detected connections as the total number of ones in the
    # matrix (excluding the node-name column), divided by two to avoid
    # double-counting symmetric connections.
    total_ones = 0
    for row in rows[1:]:
        for cell in row[1:]:
            try:
                val = int(cell)
            except ValueError:
                continue
            if val == 1:
                total_ones += 1

    connections = total_ones // 2

    return {
        "rows": num_rows,
        "columns": connections,
    }


@app.route("/")
def index():
    """Render the main dashboard page."""

    metrics = load_validation_metrics()
    matrix_summary = load_connectivity_matrix_summary()

    return render_template(
        "index.html",
        metrics=metrics,
        matrix_summary=matrix_summary,
    )


@app.route("/resource/<category>/<filename>")
def get_resource(category: str, filename: str):
    """Serve image resources from the Dashboard subfolders.

    This is used for the small previews under the top-row buttons.
    """

    # Limit categories to the known resource folders.
    allowed_categories = {
        "Raw",
        "Wires",
        "Junctions",
        "Components",
        "Labels",
    }

    if category not in allowed_categories:
        abort(404)

    directory = RESOURCES_DIR / category
    if not directory.exists():
        abort(404)

    return send_from_directory(directory, filename)


@app.route("/download/matrix")
def download_matrix():
    """Download the precomputed connectivity matrix CSV."""

    try:
        csv_path = _safe_path("Result connectivity matrix", "connectivity_matrix.csv")
    except FileNotFoundError:
        abort(404)

    return send_file(
        csv_path,
        as_attachment=True,
        download_name="connectivity_matrix.csv",
    )


def create_app() -> Flask:
    """Factory to make it easy to import this app elsewhere."""

    return app


if __name__ == "__main__":
    # Local development entry point.
    app.run(debug=True)


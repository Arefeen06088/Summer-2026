import csv
import json
from pathlib import Path

BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\39")
INPUT = BASE / "Input resources"
ART = BASE / "Codes and artifacts"
OUT = ART / "geometry_sanity_current.json"


def parse_bbox(text):
    return [float(x.strip()) for x in text.strip("[]").split(",")]


components = []
with (ART / "component_labels_list_current.csv").open(newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        bbox = parse_bbox(row["bbox"])
        components.append(
            {
                "node_name": row["node_name"],
                "component_type": row["component_type"],
                "center_x": float(row["center_x"]),
                "center_y": float(row["center_y"]),
                "bbox": bbox,
            }
        )

wire_nodes = []
with (INPUT / "wire_nodes.csv").open(newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        wire_nodes.append(
            {
                "node_id": row["node_id"],
                "node_type": row["node_type"],
                "x": float(row["x"]),
                "y": float(row["y"]),
                "degree": int(row["degree"]),
            }
        )


def nearest_components(point, n=5):
    px, py = point["x"], point["y"]
    ranked = []
    for c in components:
        x1, y1, x2, y2 = c["bbox"]
        dx = max(x1 - px, 0, px - x2)
        dy = max(y1 - py, 0, py - y2)
        ranked.append(
            {
                "node_id": point["node_id"],
                "x": px,
                "y": py,
                "near_node": c["node_name"],
                "near_type": c["component_type"],
                "distance_to_bbox": round((dx * dx + dy * dy) ** 0.5, 1),
            }
        )
    return sorted(ranked, key=lambda r: r["distance_to_bbox"])[:n]


focus_points = [
    w
    for w in wire_nodes
    if (
        (0 <= w["x"] <= 650 and 950 <= w["y"] <= 2000)
        or (3900 <= w["x"] <= 4550 and 950 <= w["y"] <= 2000)
        or (1500 <= w["x"] <= 4100 and 2180 <= w["y"] <= 2600)
    )
]

result = {
    "note": "Nearest component boxes for wire nodes in doc39 charger/control focus regions. Input-derived aid only.",
    "focus_wire_node_count": len(focus_points),
    "nearest": [nearest_components(w, 4) for w in focus_points],
}

OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
print(OUT)

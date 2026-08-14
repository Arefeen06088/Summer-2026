from __future__ import annotations

import json
import shutil
from pathlib import Path

from PIL import Image


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\26\Raw + wires + components + junctions"
)
RESULTS = BASE / "results"
CODES = BASE / "codes"
CROP_DIR = RESULTS / "visual_crops"

SOURCES = {
    "raw": BASE / "raw -- synthetic_npp_electrical_schematic_v3(1).png",
    "components": BASE / "detected_components_overlay.png",
    "wire_nodes": BASE / "wire_nodes_overlay.png",
    "wires": BASE / "wires_mask_overlay.png",
}


REGIONS = {
    "full": (0, 0, 7000, 4334),
    "top_left_train": (180, 300, 3000, 1600),
    "top_right_train": (3150, 300, 5800, 1600),
    "middle_left_train": (180, 1500, 3000, 2850),
    "middle_right_train": (3150, 1500, 5800, 2850),
    "bottom_left_train": (180, 2800, 3000, 4210),
    "bottom_right_train": (3150, 2800, 5800, 4210),
    "left_top_bus_close": (250, 650, 2850, 1450),
    "right_top_bus_close": (3200, 650, 5750, 1450),
    "left_middle_loads_close": (250, 1750, 2850, 2750),
    "right_middle_loads_close": (3200, 1750, 5750, 2750),
    "left_bottom_control_close": (250, 2750, 2850, 4200),
    "right_bottom_control_close": (3200, 2750, 5750, 4200),
    "center_ties": (2850, 650, 3300, 3300),
    "title_block": (6000, 3275, 6980, 4260),
    "legend_notes": (6000, 750, 6980, 2500),
    "revisions": (6000, 180, 6980, 760),
    "top_sources_full": (250, 120, 5850, 900),
    "top_sources_left": (250, 120, 1600, 900),
    "top_sources_mid": (1600, 120, 3500, 900),
    "top_sources_right": (3500, 120, 5850, 900),
    "bus_ties_close": (2600, 650, 3650, 3450),
    "lower_left_control_full": (250, 2550, 3100, 4300),
    "lower_right_control_full": (3150, 2550, 5950, 4300),
    "rps_panel_a_close": (3900, 2750, 5400, 3650),
    "rps_panel_b_close": (4850, 2750, 6350, 3650),
    "rps_pt_a_close": (3900, 3350, 5400, 4250),
    "rps_pt_b_close": (4850, 3350, 6350, 4250),
}


def crop_and_save(image: Image.Image, name: str, box: tuple[int, int, int, int]) -> dict[str, object]:
    crop = image.crop(box)
    out = CROP_DIR / f"{name}.png"
    crop.save(out)
    return {"file": str(out), "box": box, "size": crop.size}


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    CODES.mkdir(parents=True, exist_ok=True)
    CROP_DIR.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, object] = {"base": str(BASE), "sources": {}, "crops": []}

    for source_name, source_path in SOURCES.items():
        image = Image.open(source_path)
        manifest["sources"][source_name] = {
            "path": str(source_path),
            "size": image.size,
            "mode": image.mode,
        }
        for region_name, box in REGIONS.items():
            if region_name == "full":
                thumb = image.copy()
                thumb.thumbnail((1800, 1200))
                out = CROP_DIR / f"{source_name}_full_thumb.png"
                thumb.save(out)
                manifest["crops"].append({"file": str(out), "box": (0, 0, *image.size), "size": thumb.size})
            else:
                manifest["crops"].append(crop_and_save(image, f"{source_name}_{region_name}", box))

    (CROP_DIR / "crop_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    shutil.copy2(Path(__file__), CODES / Path(__file__).name)
    print(json.dumps({"crop_dir": str(CROP_DIR), "crop_count": len(manifest["crops"])}, indent=2))


if __name__ == "__main__":
    main()

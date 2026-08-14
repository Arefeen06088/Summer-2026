from __future__ import annotations

import json
import shutil
from pathlib import Path

from PIL import Image


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\2\Raw + wires + components + junctions"
)
RESULTS = BASE / "results"
CODES = BASE / "codes"
CROP_DIR = RESULTS / "visual_crops"

SOURCES = {
    "raw": BASE / "raw -- schematic_image_variant_b_100.png",
    "components": BASE / "detected_components_and_logical_overlay.png",
    "wire_nodes": BASE / "wire_nodes_overlay.png",
    "wires": BASE / "wires_mask_overlay.png",
}

REGIONS = {
    "full": (0, 0, 10800, 7200),
    "top_sources_and_4160": (900, 250, 9000, 1900),
    "top_left_sources": (1200, 350, 3800, 1900),
    "top_right_sources": (5850, 350, 9000, 1900),
    "header_left_bus": (850, 1250, 5050, 1650),
    "header_tie": (4650, 1200, 5650, 1650),
    "header_right_bus": (5200, 1250, 9050, 1650),
    "left_train_a_full": (650, 1350, 5150, 5400),
    "right_train_b_full": (5050, 1350, 9300, 5400),
    "left_feeders_close": (700, 1550, 3900, 3800),
    "right_feeders_close": (5200, 1550, 8950, 3800),
    "left_480_and_loads": (700, 2500, 3900, 5200),
    "right_480_and_loads": (5200, 2500, 8950, 5200),
    "left_dc_ac_rps": (3150, 3100, 5150, 6550),
    "right_dc_ac_rps": (7600, 3100, 9300, 6550),
    "cvcs_a_branch": (4000, 1750, 5150, 4200),
    "cvcs_b_branch": (8450, 1750, 9300, 4200),
    "lower_control_tie": (3400, 5150, 8150, 6750),
    "notes_legend": (8950, 900, 10750, 2500),
    "title_block": (8950, 5800, 10750, 7100),
}


def save_crop(image: Image.Image, source: str, region: str, box: tuple[int, int, int, int]) -> dict[str, object]:
    crop = image.crop(box)
    out = CROP_DIR / f"{source}_{region}.png"
    crop.save(out)
    return {"file": str(out), "source": source, "region": region, "box": box, "size": crop.size}


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    CODES.mkdir(parents=True, exist_ok=True)
    CROP_DIR.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, object] = {"base": str(BASE), "sources": {}, "crops": []}

    for source, path in SOURCES.items():
        image = Image.open(path)
        manifest["sources"][source] = {"path": str(path), "size": image.size, "mode": image.mode}
        for region, box in REGIONS.items():
            if region == "full":
                thumb = image.copy()
                thumb.thumbnail((1800, 1200))
                out = CROP_DIR / f"{source}_full_thumb.png"
                thumb.save(out)
                manifest["crops"].append({"file": str(out), "source": source, "region": region, "box": box, "size": thumb.size})
            else:
                manifest["crops"].append(save_crop(image, source, region, box))

    (CROP_DIR / "crop_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    shutil.copy2(Path(__file__), CODES / Path(__file__).name)
    print(json.dumps({"crop_dir": str(CROP_DIR), "crop_count": len(manifest["crops"])}, indent=2))


if __name__ == "__main__":
    main()

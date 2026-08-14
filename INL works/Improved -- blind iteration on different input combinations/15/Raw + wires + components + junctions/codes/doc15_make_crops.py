from __future__ import annotations

import json
import shutil
from pathlib import Path

from PIL import Image


DOC = "15"
BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\15\Raw + wires + components + junctions"
)
RESULTS = BASE / "results"
CODES = BASE / "codes"
CROPS = RESULTS / "visual_crops"

SOURCES = {
    "raw": BASE / "raw -- improved_synthetic_nuclear_electrical_schematic.png",
    "components": BASE / "detected_components_overlay.png",
    "wires_mask": BASE / "wires_mask.png",
    "wires_overlay": BASE / "wires_mask_overlay.png",
    "wire_nodes": BASE / "wire_nodes_overlay.png",
}


BOXES = {
    "full_schematic": (0, 0, 7600, 5000),
    "main_drawing": (120, 80, 6460, 3820),
    "offsite_sources_top": (350, 80, 6300, 700),
    "nss_and_4160_top": (250, 520, 6350, 1500),
    "division_1a_full": (300, 520, 1850, 3650),
    "division_1b_full": (1780, 520, 3350, 3650),
    "division_2a_full": (3250, 520, 4900, 3650),
    "division_2b_full": (4750, 520, 6400, 3650),
    "div_1a_top_safety": (360, 480, 1880, 1500),
    "div_1b_top_safety": (1780, 480, 3350, 1500),
    "div_2a_top_safety": (3260, 480, 4900, 1500),
    "div_2b_top_safety": (4750, 480, 6400, 1500),
    "div_1a_mcc": (360, 1420, 1880, 2920),
    "div_1b_mcc": (1780, 1420, 3350, 2920),
    "div_2a_mcc": (3260, 1420, 4900, 2920),
    "div_2b_mcc": (4750, 1420, 6400, 2920),
    "div_1a_dc_ups": (360, 2800, 1880, 3720),
    "div_1b_dc_ups": (1780, 2800, 3350, 3720),
    "div_2a_dc_ups": (3260, 2800, 4900, 3720),
    "div_2b_dc_ups": (4750, 2800, 6400, 3720),
    "tie_1a_1b": (1460, 560, 2200, 1500),
    "tie_2a_2b": (4420, 560, 5200, 1500),
    "central_control_1": (1450, 2850, 3400, 3760),
    "central_control_2": (4400, 2850, 6400, 3760),
    "right_notes": (6320, 420, 7480, 3520),
    "title_block": (5200, 4200, 7440, 4900),
    "revision_block": (100, 4200, 1800, 4900),
}


def clamp_box(img: Image.Image, box: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    x0, y0, x1, y1 = box
    return (
        max(0, min(img.width, x0)),
        max(0, min(img.height, y0)),
        max(0, min(img.width, x1)),
        max(0, min(img.height, y1)),
    )


def save_crop(
    img: Image.Image,
    source_name: str,
    crop_name: str,
    box: tuple[int, int, int, int],
    manifest: list[dict[str, object]],
) -> None:
    x0, y0, x1, y1 = clamp_box(img, box)
    if x1 <= x0 or y1 <= y0:
        return
    out_name = f"{crop_name}_{source_name}.png"
    out = img.crop((x0, y0, x1, y1))
    out.save(CROPS / out_name)
    manifest.append(
        {
            "source": source_name,
            "file": out_name,
            "box": [x0, y0, x1, y1],
            "size": [out.width, out.height],
        }
    )


def main() -> None:
    missing = [str(path) for path in SOURCES.values() if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing approved source files: " + "; ".join(missing))

    RESULTS.mkdir(parents=True, exist_ok=True)
    CODES.mkdir(parents=True, exist_ok=True)
    CROPS.mkdir(parents=True, exist_ok=True)

    opened = {name: Image.open(path).convert("RGB") for name, path in SOURCES.items()}
    try:
        raw = opened["raw"]
        w, h = raw.size
        manifest: list[dict[str, object]] = []

        for source_name, img in opened.items():
            thumb = img.copy()
            thumb.thumbnail((1800, 1200))
            thumb_name = f"{source_name}_full_thumb.png"
            thumb.save(CROPS / thumb_name)
            manifest.append(
                {
                    "source": source_name,
                    "file": thumb_name,
                    "box": [0, 0, w, h],
                    "size": [thumb.width, thumb.height],
                    "thumb": True,
                }
            )
            for crop_name, box in BOXES.items():
                save_crop(img, source_name, crop_name, box, manifest)

            cols, rows = 5, 4
            tile_w, tile_h = w // cols, h // rows
            for yy in range(rows):
                for xx in range(cols):
                    x0 = xx * tile_w - 120
                    y0 = yy * tile_h - 120
                    x1 = (xx + 1) * tile_w + 120
                    y1 = (yy + 1) * tile_h + 120
                    save_crop(img, source_name, f"grid_r{yy}_c{xx}", (x0, y0, x1, y1), manifest)

        # Extra overlapping detailed crops for the four division columns.
        detail_sources = ("raw", "components", "wire_nodes")
        detail_id = 0
        for x0 in (260, 1650, 3100, 4550):
            for y0 in (420, 1050, 1700, 2380, 3000):
                box = (x0, y0, x0 + 1750, y0 + 950)
                for source_name in detail_sources:
                    save_crop(opened[source_name], source_name, f"detail_{detail_id:02d}", box, manifest)
                detail_id += 1

        manifest_path = CROPS / "crop_manifest.json"
        manifest_path.write_text(
            json.dumps(
                {
                    "document": DOC,
                    "source_size": [w, h],
                    "allowed_base": str(BASE),
                    "sources": {name: str(path) for name, path in SOURCES.items()},
                    "crops": manifest,
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        shutil.copy2(Path(__file__), CODES / Path(__file__).name)
        print(json.dumps({"source_size": [w, h], "crops": len(manifest), "manifest": str(manifest_path)}, indent=2))
    finally:
        for img in opened.values():
            img.close()


if __name__ == "__main__":
    main()

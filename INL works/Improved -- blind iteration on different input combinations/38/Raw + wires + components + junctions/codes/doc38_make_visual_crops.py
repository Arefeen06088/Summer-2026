from __future__ import annotations

import json
import shutil
from pathlib import Path

from PIL import Image


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\38\Raw + wires + components + junctions"
)
RESULTS = BASE / "results"
CODES = BASE / "codes"
CROPS = RESULTS / "visual_crops"


SOURCES = {
    "raw": BASE / "raw -- synthetic_npp_schematic_improved.png",
    "components": BASE / "detected_components_and_logical_overlay.png",
    "wires_mask": BASE / "wires_mask.png",
    "wires_overlay": BASE / "wires_mask_overlay.png",
    "wire_nodes": BASE / "wire_nodes_overlay.png",
}


def crop_box(img: Image.Image, box: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    x0, y0, x1, y1 = box
    return (
        max(0, min(img.width, x0)),
        max(0, min(img.height, y0)),
        max(0, min(img.width, x1)),
        max(0, min(img.height, y1)),
    )


def save_crop(
    manifest: list[dict[str, object]],
    source_name: str,
    img: Image.Image,
    box_name: str,
    box: tuple[int, int, int, int],
) -> None:
    x0, y0, x1, y1 = crop_box(img, box)
    if x1 <= x0 or y1 <= y0:
        return
    out_name = f"{box_name}_{source_name}.png"
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


def make_crops() -> None:
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

        bands = {
            "full": (0, 0, w, h),
            "top_sources": (0, 0, w, int(h * 0.24)),
            "upper_distribution": (0, int(h * 0.13), w, int(h * 0.42)),
            "middle_distribution": (0, int(h * 0.30), w, int(h * 0.66)),
            "lower_distribution": (0, int(h * 0.55), w, h),
            "left_half": (0, 0, int(w * 0.55), h),
            "right_half": (int(w * 0.45), 0, w, h),
            "center_controls": (int(w * 0.28), int(h * 0.24), int(w * 0.74), int(h * 0.78)),
            "left_loads": (0, int(h * 0.38), int(w * 0.55), h),
            "right_loads": (int(w * 0.45), int(h * 0.38), w, h),
            "bottom_controls": (int(w * 0.10), int(h * 0.66), int(w * 0.92), h),
        }

        for source_name, img in opened.items():
            thumb = img.copy()
            thumb.thumbnail((1700, 1200))
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

            for box_name, box in bands.items():
                save_crop(manifest, source_name, img, box_name, box)

            cols, rows = 5, 4
            tile_w, tile_h = w // cols, h // rows
            for yy in range(rows):
                for xx in range(cols):
                    x0 = xx * tile_w - 100
                    y0 = yy * tile_h - 100
                    x1 = (xx + 1) * tile_w + 100
                    y1 = (yy + 1) * tile_h + 100
                    save_crop(manifest, source_name, img, f"grid_r{yy}_c{xx}", (x0, y0, x1, y1))

        # Extra overlapping detail windows on the raw, component, and wire-node views.
        detail_sources = ("raw", "components", "wire_nodes")
        detail_id = 0
        win_w, win_h = int(w * 0.28), int(h * 0.24)
        step_x, step_y = int(w * 0.18), int(h * 0.16)
        for y in range(int(h * 0.02), int(h * 0.88), step_y):
            for x in range(int(w * 0.01), int(w * 0.86), step_x):
                for source_name in detail_sources:
                    save_crop(
                        manifest,
                        source_name,
                        opened[source_name],
                        f"detail_{detail_id:02d}",
                        (x, y, x + win_w, y + win_h),
                    )
                detail_id += 1

        manifest_path = CROPS / "crop_manifest.json"
        manifest_path.write_text(
            json.dumps(
                {
                    "document": "38",
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
    make_crops()

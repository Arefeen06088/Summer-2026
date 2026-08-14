from __future__ import annotations

import json
from pathlib import Path

from PIL import Image


Image.MAX_IMAGE_PIXELS = None

BASE_DIR = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\26\Raw + wires + components")
RESULTS_DIR = BASE_DIR / "results"
CROPS_DIR = RESULTS_DIR / "visual_crops"

RAW = BASE_DIR / "raw -- synthetic_npp_electrical_schematic_v3(1).png"
COMPONENTS = BASE_DIR / "detected_components_overlay.png"
WIRES = BASE_DIR / "wires_mask.png"
WIRES_OVERLAY = BASE_DIR / "wires_mask_overlay.png"

SOURCES = {
    "raw": RAW,
    "components": COMPONENTS,
    "wires": WIRES,
    "wires_overlay": WIRES_OVERLAY,
}


def save_resized_crop(img: Image.Image, box: tuple[int, int, int, int], out: Path, max_side: int = 2800) -> None:
    crop = img.crop(box)
    scale = min(max_side / max(crop.size), 1.0)
    if scale < 1.0:
        crop = crop.resize((int(crop.width * scale), int(crop.height * scale)))
    out.parent.mkdir(parents=True, exist_ok=True)
    crop.save(out)


def main() -> None:
    CROPS_DIR.mkdir(parents=True, exist_ok=True)
    with Image.open(RAW) as raw_img:
        width, height = raw_img.size

    for tag, path in SOURCES.items():
        with Image.open(path) as img:
            thumb = img.copy()
            thumb.thumbnail((2400, 1600))
            thumb.save(CROPS_DIR / f"{tag}_full_thumb.png")

    nx, ny = 4, 3
    overlap = 0.10
    tile_w = width / nx
    tile_h = height / ny
    regions: dict[str, tuple[int, int, int, int]] = {}
    for row in range(ny):
        for col in range(nx):
            x0 = max(0, int(col * tile_w - overlap * tile_w))
            y0 = max(0, int(row * tile_h - overlap * tile_h))
            x1 = min(width, int((col + 1) * tile_w + overlap * tile_w))
            y1 = min(height, int((row + 1) * tile_h + overlap * tile_h))
            regions[f"grid_r{row + 1}_c{col + 1}"] = (x0, y0, x1, y1)

    regions.update(
        {
            "full_top_sources": (0, 0, width, int(height * 0.32)),
            "upper_distribution_all": (0, int(height * 0.12), width, int(height * 0.50)),
            "middle_distribution_all": (0, int(height * 0.28), width, int(height * 0.75)),
            "bottom_control_all": (0, int(height * 0.60), width, height),
            "left_half": (0, 0, int(width * 0.55), height),
            "right_half": (int(width * 0.45), 0, width, height),
            "center_overlap": (int(width * 0.24), int(height * 0.16), int(width * 0.76), int(height * 0.86)),
            "top_left": (0, 0, int(width * 0.43), int(height * 0.40)),
            "top_center": (int(width * 0.28), 0, int(width * 0.72), int(height * 0.40)),
            "top_right": (int(width * 0.57), 0, width, int(height * 0.40)),
            "mid_left": (0, int(height * 0.22), int(width * 0.43), int(height * 0.68)),
            "mid_center": (int(width * 0.28), int(height * 0.22), int(width * 0.72), int(height * 0.68)),
            "mid_right": (int(width * 0.57), int(height * 0.22), width, int(height * 0.68)),
            "lower_left": (0, int(height * 0.50), int(width * 0.43), height),
            "lower_center": (int(width * 0.28), int(height * 0.50), int(width * 0.72), height),
            "lower_right": (int(width * 0.57), int(height * 0.50), width, height),
            "title_notes": (int(width * 0.66), 0, width, int(height * 0.30)),
        }
    )

    # Extra regions based on the common INL synthetic single-line sheet layout.
    regions.update(
        {
            "train_a_upper_detail": (100, 420, 2380, 1880),
            "train_b_upper_detail": (2140, 420, 4420, 1880),
            "train_c_upper_detail": (4180, 420, 6450, 1880),
            "train_a_lower_detail": (100, 1700, 2380, 3500),
            "train_b_lower_detail": (2140, 1700, 4420, 3500),
            "train_c_lower_detail": (4180, 1700, 6450, 3500),
            "bottom_left_control_detail": (100, 3200, 3000, 4250),
            "bottom_center_control_detail": (2300, 3200, 5000, 4250),
            "bottom_right_control_detail": (4300, 3200, 6900, 4250),
        }
    )

    for name, box in regions.items():
        for tag, path in SOURCES.items():
            if tag == "wires":
                continue
            max_side = 4300 if "detail" in name else 2800
            with Image.open(path) as img:
                save_resized_crop(img, box, CROPS_DIR / f"{name}_{tag}.png", max_side=max_side)

    manifest = {
        "image_size": [width, height],
        "raw": RAW.name,
        "regions": {name: list(box) for name, box in regions.items()},
    }
    (CROPS_DIR / "crop_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()

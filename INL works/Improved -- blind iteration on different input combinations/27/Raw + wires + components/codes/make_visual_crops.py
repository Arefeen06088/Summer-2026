from __future__ import annotations

import json
from pathlib import Path

from PIL import Image


BASE = Path(__file__).resolve().parents[1]
RESULTS = BASE / "results"
CROPS = RESULTS / "visual_crops"


def find_raw() -> Path:
    candidates = sorted(BASE.glob("raw*.png"))
    if not candidates:
        raise FileNotFoundError("No raw*.png schematic found")
    return candidates[0]


SOURCES = {
    "raw": find_raw(),
    "components": BASE / "detected_components_overlay.png",
    "wires_overlay": BASE / "wires_mask_overlay.png",
}


def clamp_box(box: tuple[int, int, int, int], w: int, h: int) -> tuple[int, int, int, int]:
    x1, y1, x2, y2 = box
    x1 = max(0, min(w - 1, x1))
    y1 = max(0, min(h - 1, y1))
    x2 = max(x1 + 1, min(w, x2))
    y2 = max(y1 + 1, min(h, y2))
    return x1, y1, x2, y2


def resize_for_view(img: Image.Image, max_side: int = 3200) -> Image.Image:
    w, h = img.size
    scale = min(max_side / max(w, h), 1.0)
    if scale >= 1.0:
        return img.copy()
    return img.resize((round(w * scale), round(h * scale)), Image.Resampling.LANCZOS)


def save_crop(src_name: str, img: Image.Image, name: str, box: tuple[int, int, int, int], max_side: int = 3200) -> None:
    crop = img.crop(clamp_box(box, *img.size))
    resize_for_view(crop, max_side=max_side).save(CROPS / f"{name}_{src_name}.png")


def main() -> None:
    CROPS.mkdir(parents=True, exist_ok=True)
    with Image.open(SOURCES["raw"]) as raw_img:
        width, height = raw_img.size

    regions: dict[str, tuple[int, int, int, int]] = {}

    # Overlapped 4x4 grid, good for labels on this larger drawing.
    cols, rows = 4, 4
    ox = width // 18
    oy = height // 18
    for r in range(rows):
        for c in range(cols):
            x1 = max(0, c * width // cols - ox)
            x2 = min(width, (c + 1) * width // cols + ox)
            y1 = max(0, r * height // rows - oy)
            y2 = min(height, (r + 1) * height // rows + oy)
            regions[f"grid_r{r + 1}_c{c + 1}"] = (x1, y1, x2, y2)

    # Broad bands and halves/thirds for topology.
    regions.update(
        {
            "full_top": (0, 0, width, int(height * 0.30)),
            "upper_distribution_all": (0, int(height * 0.14), width, int(height * 0.52)),
            "middle_distribution_all": (0, int(height * 0.32), width, int(height * 0.76)),
            "bottom_control_all": (0, int(height * 0.62), width, height),
            "left_half": (0, 0, int(width * 0.55), height),
            "right_half": (int(width * 0.45), 0, width, height),
            "center_overlap": (int(width * 0.25), int(height * 0.12), int(width * 0.75), int(height * 0.88)),
            "top_left": (0, 0, int(width * 0.38), int(height * 0.35)),
            "top_center": (int(width * 0.28), 0, int(width * 0.72), int(height * 0.35)),
            "top_right": (int(width * 0.62), 0, width, int(height * 0.35)),
            "mid_left": (0, int(height * 0.22), int(width * 0.38), int(height * 0.70)),
            "mid_center": (int(width * 0.28), int(height * 0.22), int(width * 0.72), int(height * 0.70)),
            "mid_right": (int(width * 0.62), int(height * 0.22), width, int(height * 0.70)),
            "lower_left": (0, int(height * 0.50), int(width * 0.38), height),
            "lower_center": (int(width * 0.28), int(height * 0.50), int(width * 0.72), height),
            "lower_right": (int(width * 0.62), int(height * 0.50), width, height),
            "title_notes": (int(width * 0.68), 0, width, int(height * 0.38)),
        }
    )

    # Smaller detail windows by columns, useful for the repeated train areas.
    for i, (x1f, x2f) in enumerate([(0.02, 0.28), (0.24, 0.50), (0.46, 0.72), (0.68, 0.96)], start=1):
        regions[f"upper_detail_{i}"] = (int(width * x1f), int(height * 0.08), int(width * x2f), int(height * 0.43))
        regions[f"middle_detail_{i}"] = (int(width * x1f), int(height * 0.36), int(width * x2f), int(height * 0.69))
        regions[f"lower_detail_{i}"] = (int(width * x1f), int(height * 0.60), int(width * x2f), height)

    for src_name, path in SOURCES.items():
        with Image.open(path) as img:
            resize_for_view(img, max_side=3200).save(CROPS / f"{src_name}_full_thumb.png")
            for name, box in regions.items():
                save_crop(src_name, img, name, box)

    manifest = {
        "image_size": [width, height],
        "raw": SOURCES["raw"].name,
        "regions": {k: list(v) for k, v in regions.items()},
        "sources": {k: str(v) for k, v in SOURCES.items()},
    }
    (CROPS / "crop_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps({"crops": len(regions) * len(SOURCES) + len(SOURCES), "manifest": str(CROPS / "crop_manifest.json")}, indent=2))


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\38\Raw + wires + components")
RESULTS = BASE / "results"
CODES = BASE / "codes"
CROPS = RESULTS / "visual_crops"


def find_image(prefix: str) -> Path:
    matches = sorted(BASE.glob(f"{prefix}*.png"))
    if not matches:
        raise FileNotFoundError(f"No image matching {prefix}*.png in {BASE}")
    return matches[0]


SOURCES = {
    "raw": find_image("raw --"),
    "components": BASE / "detected_components_and_logical_overlay.png",
    "wires_mask": BASE / "wires_mask.png",
    "wires_overlay": BASE / "wires_mask_overlay.png",
}


def save_crop(src_name: str, img: Image.Image, box: tuple[int, int, int, int], out_name: str, manifest: list[dict[str, object]]) -> None:
    x0, y0, x1, y1 = box
    x0 = max(0, min(img.width, x0))
    y0 = max(0, min(img.height, y0))
    x1 = max(0, min(img.width, x1))
    y1 = max(0, min(img.height, y1))
    if x1 <= x0 or y1 <= y0:
        return
    out = img.crop((x0, y0, x1, y1))
    out.save(CROPS / out_name)
    manifest.append({"source": src_name, "file": out_name, "box": [x0, y0, x1, y1], "size": [out.width, out.height]})


def make() -> None:
    CODES.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)
    CROPS.mkdir(parents=True, exist_ok=True)
    (CODES / "make_visual_crops.py").write_text(Path(__file__).read_text(encoding="utf-8"), encoding="utf-8")
    manifest: list[dict[str, object]] = []

    opened = {name: Image.open(path).convert("RGB") for name, path in SOURCES.items()}
    try:
        raw = opened["raw"]
        w, h = raw.size

        named_boxes = {
            "top_band": (0, 0, w, int(h * 0.30)),
            "upper_mid_band": (0, int(h * 0.20), w, int(h * 0.50)),
            "middle_band": (0, int(h * 0.34), w, int(h * 0.68)),
            "lower_mid_band": (0, int(h * 0.50), w, int(h * 0.84)),
            "bottom_band": (0, int(h * 0.68), w, h),
            "left_half": (0, 0, int(w * 0.56), h),
            "right_half": (int(w * 0.44), 0, w, h),
            "center_overlap": (int(w * 0.20), int(h * 0.14), int(w * 0.80), int(h * 0.90)),
            "focus_top_distribution": (int(w * 0.03), int(h * 0.03), int(w * 0.97), int(h * 0.35)),
            "focus_middle_distribution": (int(w * 0.05), int(h * 0.24), int(w * 0.95), int(h * 0.64)),
            "focus_lower_distribution": (int(w * 0.04), int(h * 0.55), int(w * 0.96), int(h * 0.96)),
            "focus_center": (int(w * 0.22), int(h * 0.23), int(w * 0.78), int(h * 0.80)),
            "focus_left_loads": (int(w * 0.02), int(h * 0.40), int(w * 0.54), int(h * 0.96)),
            "focus_right_loads": (int(w * 0.46), int(h * 0.40), int(w * 0.98), int(h * 0.96)),
            "focus_dc_controls": (int(w * 0.02), int(h * 0.66), int(w * 0.98), h),
        }

        for src_name, img in opened.items():
            thumb = img.copy()
            thumb.thumbnail((1600, 1200))
            thumb.save(CROPS / f"{src_name}_full_thumb.png")
            manifest.append({"source": src_name, "file": f"{src_name}_full_thumb.png", "box": [0, 0, w, h], "size": [thumb.width, thumb.height], "thumb": True})

            for box_name, box in named_boxes.items():
                save_crop(src_name, img, box, f"{box_name}_{src_name}.png", manifest)

            cols, rows = 4, 4
            tile_w, tile_h = w // cols, h // rows
            for yy in range(rows):
                for xx in range(cols):
                    x0 = max(0, xx * tile_w - 120)
                    y0 = max(0, yy * tile_h - 120)
                    x1 = min(w, (xx + 1) * tile_w + 120)
                    y1 = min(h, (yy + 1) * tile_h + 120)
                    save_crop(src_name, img, (x0, y0, x1, y1), f"grid_r{yy}_c{xx}_{src_name}.png", manifest)

        detail_boxes = []
        step_x, step_y = int(w * 0.20), int(h * 0.18)
        win_w, win_h = int(w * 0.32), int(h * 0.28)
        for y in range(int(h * 0.04), int(h * 0.90), step_y):
            for x in range(int(w * 0.02), int(w * 0.88), step_x):
                detail_boxes.append((x, y, min(w, x + win_w), min(h, y + win_h)))
        for i, box in enumerate(detail_boxes):
            for src_name in ("components", "wires_overlay"):
                save_crop(src_name, opened[src_name], box, f"detail_{i:02d}_{src_name}.png", manifest)

        with (CROPS / "crop_manifest.json").open("w", encoding="utf-8") as handle:
            json.dump({"source_size": [w, h], "sources": {k: str(v) for k, v in SOURCES.items()}, "crops": manifest}, handle, indent=2)
        print(json.dumps({"source_size": [w, h], "crops": len(manifest), "manifest": str(CROPS / "crop_manifest.json")}, indent=2))
    finally:
        for img in opened.values():
            img.close()


if __name__ == "__main__":
    make()

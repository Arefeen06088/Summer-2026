from __future__ import annotations

import json
from pathlib import Path

from PIL import Image


Image.MAX_IMAGE_PIXELS = None

BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\37\Raw + wires + components"
)
CODES = BASE / "codes"
RESULTS = BASE / "results"
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


def save_crop(
    src_name: str,
    img: Image.Image,
    box: tuple[int, int, int, int],
    out_name: str,
    manifest: list[dict[str, object]],
) -> None:
    x0, y0, x1, y1 = box
    x0 = max(0, min(img.width, x0))
    y0 = max(0, min(img.height, y0))
    x1 = max(0, min(img.width, x1))
    y1 = max(0, min(img.height, y1))
    if x1 <= x0 or y1 <= y0:
        return
    out = img.crop((x0, y0, x1, y1)).convert("RGB")
    out.save(CROPS / out_name)
    manifest.append(
        {
            "source": src_name,
            "file": out_name,
            "box": [x0, y0, x1, y1],
            "size": [out.width, out.height],
        }
    )


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
            "upper_mid_band": (0, int(h * 0.18), w, int(h * 0.53)),
            "middle_band": (0, int(h * 0.35), w, int(h * 0.70)),
            "lower_mid_band": (0, int(h * 0.52), w, int(h * 0.88)),
            "bottom_band": (0, int(h * 0.66), w, h),
            "left_half": (0, 0, int(w * 0.56), h),
            "right_half": (int(w * 0.44), 0, w, h),
            "center_overlap": (int(w * 0.18), int(h * 0.10), int(w * 0.82), int(h * 0.92)),
            "focus_top_distribution": (int(w * 0.02), int(h * 0.03), int(w * 0.98), int(h * 0.36)),
            "focus_middle_distribution": (int(w * 0.02), int(h * 0.22), int(w * 0.98), int(h * 0.64)),
            "focus_lower_distribution": (int(w * 0.02), int(h * 0.48), int(w * 0.98), int(h * 0.95)),
            "focus_bottom_controls": (int(w * 0.02), int(h * 0.58), int(w * 0.98), h),
            "focus_left_distribution": (0, int(h * 0.12), int(w * 0.58), int(h * 0.80)),
            "focus_right_distribution": (int(w * 0.42), int(h * 0.12), w, int(h * 0.80)),
        }

        for src_name, img in opened.items():
            thumb = img.copy()
            thumb.thumbnail((1600, 1200))
            thumb.save(CROPS / f"{src_name}_full_thumb.png")
            manifest.append(
                {
                    "source": src_name,
                    "file": f"{src_name}_full_thumb.png",
                    "box": [0, 0, w, h],
                    "size": [thumb.width, thumb.height],
                    "thumb": True,
                }
            )

            for box_name, box in named_boxes.items():
                save_crop(src_name, img, box, f"{box_name}_{src_name}.png", manifest)

            cols, rows = 5, 4
            tile_w, tile_h = w // cols, h // rows
            for yy in range(rows):
                for xx in range(cols):
                    x0 = max(0, xx * tile_w - 120)
                    y0 = max(0, yy * tile_h - 120)
                    x1 = min(w, (xx + 1) * tile_w + 120)
                    y1 = min(h, (yy + 1) * tile_h + 120)
                    save_crop(src_name, img, (x0, y0, x1, y1), f"grid_r{yy}_c{xx}_{src_name}.png", manifest)

        detail_boxes: list[tuple[int, int, int, int]] = []
        step_x, step_y = int(w * 0.18), int(h * 0.17)
        win_w, win_h = int(w * 0.30), int(h * 0.27)
        for y in range(int(h * 0.03), int(h * 0.92), step_y):
            for x in range(int(w * 0.02), int(w * 0.88), step_x):
                detail_boxes.append((x, y, min(w, x + win_w), min(h, y + win_h)))
        for i, box in enumerate(detail_boxes):
            for src_name in ("raw", "components", "wires_overlay"):
                save_crop(src_name, opened[src_name], box, f"detail_{i:02d}_{src_name}.png", manifest)

        with (CROPS / "crop_manifest.json").open("w", encoding="utf-8") as handle:
            json.dump({"source_size": [w, h], "sources": {k: str(v) for k, v in SOURCES.items()}, "crops": manifest}, handle, indent=2)
        print(json.dumps({"source_size": [w, h], "crops": len(manifest), "manifest": str(CROPS / "crop_manifest.json")}, indent=2))
    finally:
        for img in opened.values():
            img.close()


if __name__ == "__main__":
    make()

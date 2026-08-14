from __future__ import annotations

import json
from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\36\Raw + wires + components")
RESULTS = BASE / "results"
CROPS = RESULTS / "visual_crops"

SOURCES = {
    "raw": BASE / "raw -- synthetic_npp_electrical_schematic_v2.png",
    "components": BASE / "detected_components_and_logical_overlay.png",
    "wires_overlay": BASE / "wires_mask_overlay.png",
    "wires_mask": BASE / "wires_mask.png",
}


def clamp_box(box: tuple[int, int, int, int], w: int, h: int) -> tuple[int, int, int, int]:
    left, top, right, bottom = box
    left = max(0, min(left, w - 1))
    top = max(0, min(top, h - 1))
    right = max(left + 1, min(right, w))
    bottom = max(top + 1, min(bottom, h))
    return left, top, right, bottom


def save_crop(img: Image.Image, name: str, box: tuple[int, int, int, int], max_side: int | None, manifest: list[dict[str, object]]) -> None:
    w, h = img.size
    box = clamp_box(box, w, h)
    crop = img.crop(box)
    if max_side and max(crop.size) > max_side:
        ratio = max_side / max(crop.size)
        crop = crop.resize((max(1, int(crop.width * ratio)), max(1, int(crop.height * ratio))), Image.Resampling.LANCZOS)
    crop.save(CROPS / name)
    manifest.append({"file": name, "box": box, "saved_size": crop.size})


def main() -> None:
    CROPS.mkdir(parents=True, exist_ok=True)
    manifest: list[dict[str, object]] = []
    images = {key: Image.open(path).convert("RGB") for key, path in SOURCES.items()}
    w, h = images["raw"].size

    for key, img in images.items():
        save_crop(img, f"{key}_full_thumb.png", (0, 0, w, h), 2200, manifest)

    # 4x4 grid tiles give coverage across the whole sheet.
    for r in range(4):
        for c in range(4):
            box = (c * w // 4, r * h // 4, (c + 1) * w // 4, (r + 1) * h // 4)
            for key in ("raw", "components", "wires_overlay"):
                save_crop(images[key], f"grid_r{r + 1}_c{c + 1}_{key}.png", box, 1800, manifest)

    broad_boxes = {
        "top_band": (0, 0, w, int(h * 0.24)),
        "upper_mid_band": (0, int(h * 0.16), w, int(h * 0.46)),
        "middle_band": (0, int(h * 0.34), w, int(h * 0.68)),
        "lower_mid_band": (0, int(h * 0.54), w, int(h * 0.86)),
        "bottom_band": (0, int(h * 0.76), w, h),
        "left_half": (0, 0, int(w * 0.55), h),
        "right_half": (int(w * 0.45), 0, w, h),
        "center_overlap": (int(w * 0.20), int(h * 0.14), int(w * 0.80), int(h * 0.86)),
    }
    for name, box in broad_boxes.items():
        for key in ("raw", "components", "wires_overlay"):
            save_crop(images[key], f"{name}_{key}.png", box, 2200, manifest)

    # Detail windows around the main body; intentionally overlapping.
    xs = [0.00, 0.18, 0.36, 0.54, 0.72]
    ys = [0.05, 0.25, 0.45, 0.65]
    idx = 1
    win_w = int(w * 0.30)
    win_h = int(h * 0.28)
    for y_frac in ys:
        for x_frac in xs:
            left = int(w * x_frac)
            top = int(h * y_frac)
            box = (left, top, left + win_w, top + win_h)
            for key in ("raw", "components", "wires_overlay"):
                save_crop(images[key], f"detail_{idx:02d}_{key}.png", box, 2200, manifest)
            idx += 1

    # A few larger central closeups for likely dense distribution and control areas.
    focus_boxes = {
        "focus_top_distribution": (int(w * 0.05), int(h * 0.02), int(w * 0.95), int(h * 0.34)),
        "focus_middle_distribution": (int(w * 0.05), int(h * 0.24), int(w * 0.95), int(h * 0.62)),
        "focus_lower_distribution": (int(w * 0.05), int(h * 0.50), int(w * 0.95), int(h * 0.90)),
        "focus_center": (int(w * 0.25), int(h * 0.20), int(w * 0.75), int(h * 0.78)),
    }
    for name, box in focus_boxes.items():
        for key in ("raw", "components", "wires_overlay"):
            save_crop(images[key], f"{name}_{key}.png", box, 2400, manifest)

    data = {"source_size": [w, h], "count": len(manifest), "crops": manifest}
    (CROPS / "crop_manifest.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(json.dumps({"source_size": [w, h], "crops": len(manifest), "manifest": str(CROPS / "crop_manifest.json")}, indent=2))


if __name__ == "__main__":
    main()

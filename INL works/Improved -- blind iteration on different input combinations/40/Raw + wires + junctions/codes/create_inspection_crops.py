from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageOps


DOC = "40"
WORK = Path(r"C:\Asif_all_python_projects\INL\INL\doc40_work")
ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\40\Raw + wires + junctions")
DESIGNATED_RESULTS = ROOT / "results"
FALLBACK_RESULTS = WORK / "results"

SOURCES = {
    "raw": ROOT / "raw -- synthetic_nuclear_distribution_schematic.png",
    "wires": ROOT / "wires_mask_overlay.png",
    "nodes": ROOT / "wire_nodes_overlay.png",
    "mask": ROOT / "wires_mask.png",
}


def result_dir() -> Path:
    try:
        DESIGNATED_RESULTS.mkdir(parents=True, exist_ok=True)
        probe = DESIGNATED_RESULTS / ".write_probe_doc40"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
        return DESIGNATED_RESULTS
    except OSError:
        FALLBACK_RESULTS.mkdir(parents=True, exist_ok=True)
        return FALLBACK_RESULTS


def save_crop(
    img: Image.Image,
    box: tuple[int, int, int, int],
    out_path: Path,
    manifest: list[dict[str, object]],
    source: str,
    label: str,
) -> None:
    x0, y0, x1, y1 = box
    x0 = max(0, min(img.width, x0))
    y0 = max(0, min(img.height, y0))
    x1 = max(0, min(img.width, x1))
    y1 = max(0, min(img.height, y1))
    if x1 <= x0 or y1 <= y0:
        return
    crop = img.crop((x0, y0, x1, y1))
    crop.save(out_path)
    manifest.append(
        {
            "source": source,
            "label": label,
            "file": out_path.name,
            "box": [x0, y0, x1, y1],
            "size": [crop.width, crop.height],
        }
    )


def save_thumb(img: Image.Image, out_path: Path, max_size: tuple[int, int]) -> None:
    thumb = img.copy()
    thumb.thumbnail(max_size)
    thumb.save(out_path)


def main() -> None:
    out_dir = result_dir()
    crop_dir = out_dir / "inspection_crops"
    crop_dir.mkdir(parents=True, exist_ok=True)
    manifest: list[dict[str, object]] = []

    opened: dict[str, Image.Image] = {}
    try:
        for name, path in SOURCES.items():
            opened[name] = Image.open(path).convert("RGB")

        raw = opened["raw"]
        w, h = raw.size
        boxes = {
            "doc40_full": (0, 0, w, h),
            "top_full": (0, 0, w, int(h * 0.31)),
            "upper_mid_full": (0, int(h * 0.18), w, int(h * 0.50)),
            "mid_full": (0, int(h * 0.34), w, int(h * 0.69)),
            "lower_mid_full": (0, int(h * 0.52), w, int(h * 0.86)),
            "bottom_full": (0, int(h * 0.68), w, h),
            "left_full": (0, 0, int(w * 0.36), h),
            "center_full": (int(w * 0.25), 0, int(w * 0.75), h),
            "right_full": (int(w * 0.64), 0, w, h),
            "top_left": (0, 0, int(w * 0.38), int(h * 0.35)),
            "top_center": (int(w * 0.30), 0, int(w * 0.70), int(h * 0.35)),
            "top_right": (int(w * 0.62), 0, w, int(h * 0.35)),
            "mid_left": (0, int(h * 0.25), int(w * 0.40), int(h * 0.70)),
            "mid_center": (int(w * 0.28), int(h * 0.25), int(w * 0.72), int(h * 0.70)),
            "mid_right": (int(w * 0.60), int(h * 0.25), w, int(h * 0.70)),
            "bottom_left": (0, int(h * 0.58), int(w * 0.42), h),
            "bottom_center": (int(w * 0.27), int(h * 0.58), int(w * 0.73), h),
            "bottom_right": (int(w * 0.58), int(h * 0.58), w, h),
            "source_and_buses": (0, 0, w, int(h * 0.36)),
            "left_train": (0, int(h * 0.15), int(w * 0.52), h),
            "right_train": (int(w * 0.48), int(h * 0.15), w, h),
            "central_controls": (int(w * 0.22), int(h * 0.26), int(w * 0.78), h),
            "lower_dc_ac": (0, int(h * 0.55), w, h),
            "lower_left_detail": (0, int(h * 0.50), int(w * 0.55), h),
            "lower_right_detail": (int(w * 0.45), int(h * 0.50), w, h),
            "title": (int(w * 0.42), int(h * 0.70), w, h),
        }

        cols, rows = 4, 4
        tile_w, tile_h = w // cols, h // rows
        for yy in range(rows):
            for xx in range(cols):
                x0 = max(0, xx * tile_w - 160)
                y0 = max(0, yy * tile_h - 160)
                x1 = min(w, (xx + 1) * tile_w + 160)
                y1 = min(h, (yy + 1) * tile_h + 160)
                boxes[f"grid_r{yy}_c{xx}"] = (x0, y0, x1, y1)

        for src_name, img in opened.items():
            save_thumb(img, crop_dir / f"{src_name}_overview_2400.png", (2400, 1600))
            save_thumb(img, crop_dir / f"{src_name}_overview_1600.png", (1600, 1100))
            for label, box in boxes.items():
                save_crop(img, box, crop_dir / f"{src_name}_{label}.png", manifest, src_name, label)
            if src_name == "raw":
                gray = ImageOps.grayscale(img).convert("RGB")
                save_thumb(gray, crop_dir / "raw_gray_overview_2400.png", (2400, 1600))
                for label, box in boxes.items():
                    save_crop(gray, box, crop_dir / f"raw_gray_{label}.png", manifest, "raw_gray", label)

        with (crop_dir / "crop_manifest.json").open("w", encoding="utf-8") as handle:
            json.dump(
                {
                    "document": DOC,
                    "resource_root": str(ROOT),
                    "source_size": [w, h],
                    "sources": {k: str(v) for k, v in SOURCES.items()},
                    "crops": manifest,
                },
                handle,
                indent=2,
            )
        print(f"inspection crops written to {crop_dir}")
    finally:
        for img in opened.values():
            img.close()


if __name__ == "__main__":
    main()



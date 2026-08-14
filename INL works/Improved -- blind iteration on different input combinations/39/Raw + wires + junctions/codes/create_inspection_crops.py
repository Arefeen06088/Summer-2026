from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageOps


DOC = "39"
WORK = Path(r"C:\Asif_all_python_projects\INL\INL\doc39_work")
ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\39\Raw + wires + junctions")
DESIGNATED_RESULTS = ROOT / "results"
FALLBACK_RESULTS = WORK / "results"

SOURCES = {
    "raw": ROOT / "raw -- npp_schematic_improved_no_overlap.png",
    "wires": ROOT / "wires_mask_overlay.png",
    "nodes": ROOT / "wire_nodes_overlay.png",
    "mask": ROOT / "wires_mask.png",
}


def result_dir() -> Path:
    try:
        DESIGNATED_RESULTS.mkdir(parents=True, exist_ok=True)
        probe = DESIGNATED_RESULTS / ".write_probe_doc39"
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
            "doc39_full": (0, 0, w, h),
            "top_full": (0, 0, w, 1000),
            "upper_mid_full": (0, 700, w, 1700),
            "mid_full": (0, 1100, w, 2300),
            "bottom_full": (0, 2100, w, h),
            "left_full": (0, 0, 1800, h),
            "center_full": (1400, 0, 3400, h),
            "right_full": (3000, 0, w, h),
            "top_left": (0, 0, 1800, 1100),
            "top_center": (1300, 0, 3500, 1100),
            "top_right": (3000, 0, w, 1100),
            "mid_left": (0, 900, 1850, 2350),
            "mid_center": (1300, 900, 3500, 2350),
            "mid_right": (2950, 900, w, 2350),
            "bottom_left": (0, 1900, 1850, h),
            "bottom_center": (1300, 1900, 3500, h),
            "bottom_right": (2950, 1900, w, h),
            "source_and_buses": (0, 0, w, 1300),
            "left_train": (0, 450, 2300, h),
            "right_train": (2400, 450, w, h),
            "central_controls": (1100, 1250, 3700, h),
            "lower_dc_ac": (900, 1750, 3900, h),
            "lower_left_detail": (0, 1700, 2500, h),
            "lower_right_detail": (2300, 1700, w, h),
            "title": (3000, 2450, w, h),
        }

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


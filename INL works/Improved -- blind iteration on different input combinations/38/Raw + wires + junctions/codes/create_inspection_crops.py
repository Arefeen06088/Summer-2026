from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageOps


DOC = "38"
WORK = Path(r"C:\Asif_all_python_projects\INL\INL\doc38_work")
ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\38\Raw + wires + junctions")
DESIGNATED_RESULTS = ROOT / "results"
FALLBACK_RESULTS = WORK / "results"

SOURCES = {
    "raw": ROOT / "raw -- synthetic_npp_schematic_improved.png",
    "wires": ROOT / "wires_mask_overlay.png",
    "nodes": ROOT / "wire_nodes_overlay.png",
    "mask": ROOT / "wires_mask.png",
}


def result_dir() -> Path:
    try:
        DESIGNATED_RESULTS.mkdir(parents=True, exist_ok=True)
        probe = DESIGNATED_RESULTS / ".write_probe_doc38"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
        return DESIGNATED_RESULTS
    except OSError:
        FALLBACK_RESULTS.mkdir(parents=True, exist_ok=True)
        return FALLBACK_RESULTS


def clamp_box(box: tuple[int, int, int, int], w: int, h: int) -> tuple[int, int, int, int]:
    x0, y0, x1, y1 = box
    return max(0, x0), max(0, y0), min(w, x1), min(h, y1)


def save_crop(
    img: Image.Image,
    box: tuple[int, int, int, int],
    out_path: Path,
    manifest: list[dict[str, object]],
    source: str,
    label: str,
) -> None:
    x0, y0, x1, y1 = clamp_box(box, img.width, img.height)
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
            "doc38_full": (0, 0, w, h),
            "top_full": (0, 0, w, 1050),
            "mid_full": (0, 850, w, 2200),
            "bottom_full": (0, 2000, w, h),
            "left_full": (0, 0, 1900, h),
            "center_full": (1500, 0, 3600, h),
            "right_full": (3200, 0, w, h),
            "top_left": (0, 0, 1900, 1150),
            "top_center": (1500, 0, 3600, 1150),
            "top_right": (3200, 0, w, 1150),
            "mid_left": (0, 850, 1900, 2300),
            "mid_center": (1500, 850, 3600, 2300),
            "mid_right": (3200, 850, w, 2300),
            "bottom_left": (0, 1900, 1900, h),
            "bottom_center": (1500, 1900, 3600, h),
            "bottom_right": (3200, 1900, w, h),
            "source_top": (950, 0, 4200, 980),
            "distribution_center": (950, 680, 4200, 2000),
            "train_a_loads": (0, 1450, 2300, h),
            "train_b_loads": (2800, 1450, w, h),
            "dc_control_left": (900, 1900, 2700, h),
            "dc_control_right": (2400, 1900, 4200, h),
            "lower_control_center": (1300, 2150, 3800, h),
            "title": (3500, 2600, w, h),
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

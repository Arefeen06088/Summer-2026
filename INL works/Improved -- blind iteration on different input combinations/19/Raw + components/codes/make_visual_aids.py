from __future__ import annotations

from pathlib import Path

from PIL import Image


ROOT = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\19\Raw + components"
)
RAW = ROOT / "raw -- synthetic_npp_electrical_schematic_v3.png"
OVERLAY = ROOT / "detected_components_and_logical_overlay.png"
OUT = ROOT / "results"


def save_preview(img: Image.Image, name: str, max_side: int = 2200) -> None:
    preview = img.copy()
    preview.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
    preview.save(OUT / name)


def save_crop(img: Image.Image, prefix: str, name: str, box: tuple[int, int, int, int], upscale: int = 1) -> None:
    x0, y0, x1, y1 = box
    x0 = max(0, min(img.width, x0))
    y0 = max(0, min(img.height, y0))
    x1 = max(0, min(img.width, x1))
    y1 = max(0, min(img.height, y1))
    if x1 <= x0 or y1 <= y0:
        return
    crop = img.crop((x0, y0, x1, y1))
    crop.save(OUT / f"{prefix}_{name}.png")
    if upscale > 1:
        crop.resize((crop.width * upscale, crop.height * upscale), Image.Resampling.LANCZOS).save(
            OUT / f"{prefix}_{name}_{upscale}x.png"
        )


def make_for_image(path: Path, prefix: str) -> None:
    with Image.open(path) as opened:
        img = opened.convert("RGB")
        w, h = img.size
        save_preview(img, f"{prefix}_full_preview.png")

        # Coarse grid with overlap for reading labels near boundaries.
        cols = 4
        rows = 4
        pad_x = 150
        pad_y = 130
        for row in range(rows):
            for col in range(cols):
                save_crop(
                    img,
                    prefix,
                    f"grid_r{row + 1}c{col + 1}",
                    (
                        int(col * w / cols) - pad_x,
                        int(row * h / rows) - pad_y,
                        int((col + 1) * w / cols) + pad_x,
                        int((row + 1) * h / rows) + pad_y,
                    ),
                )

        boxes = {
            "01_top_4160_buses_full": (550, 250, 7600, 1200),
            "02_top_4160_left": (650, 250, 3650, 1180),
            "03_top_4160_right": (3450, 250, 7600, 1180),
            "04_480_feeders_full": (400, 1050, 7700, 3300),
            "05_480_feeders_left": (430, 1100, 2600, 3300),
            "06_480_feeders_left_mid": (2200, 1100, 4400, 3300),
            "07_480_feeders_right_mid": (4000, 1100, 6100, 3300),
            "08_480_feeders_right": (5750, 1100, 7700, 3300),
            "09_lower_dc_control_full": (450, 3050, 7800, 4400),
            "10_lower_dc_control_a": (500, 3150, 4200, 4350),
            "11_lower_dc_control_b": (4800, 3150, 7800, 4350),
            "12_left_train_full": (430, 250, 4300, 4400),
            "13_right_train_full": (4200, 250, 7800, 4400),
            "14_notes_legend": (7750, 520, 9100, 2000),
            "15_revision_title": (7700, 1900, 9100, 5350),
            "16_main_drawing_area": (360, 250, 7900, 4450),
        }
        for name, box in boxes.items():
            save_crop(img, prefix, name, box)

        close_boxes = {
            "17_close_top_left_sources": (820, 280, 2700, 1000),
            "18_close_top_center_tie": (3400, 520, 4800, 1100),
            "19_close_top_right_sources": (4900, 280, 7150, 1000),
            "20_close_480_tie": (3750, 950, 4650, 1250),
            "21_close_left_loads_1": (620, 1180, 1800, 2700),
            "22_close_left_loads_2": (1750, 1180, 3000, 2700),
            "23_close_mid_loads_1": (2850, 1180, 4150, 2700),
            "24_close_mid_loads_2": (4000, 1180, 5300, 2700),
            "25_close_right_loads_1": (5200, 1180, 6550, 2700),
            "26_close_right_loads_2": (6350, 1180, 7600, 2700),
            "27_close_a_load_bottoms": (600, 2350, 3600, 3300),
            "28_close_b_load_bottoms": (4300, 2350, 7600, 3300),
            "29_close_a_dc": (640, 3300, 4300, 4200),
            "30_close_b_dc": (4800, 3300, 7700, 4200),
        }
        for name, box in close_boxes.items():
            save_crop(img, prefix, name, box, upscale=2)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    make_for_image(RAW, "raw")
    make_for_image(OVERLAY, "overlay")
    print(f"wrote Doc19 Raw + components visual aids to {OUT}")


if __name__ == "__main__":
    main()

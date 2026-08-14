from __future__ import annotations

from pathlib import Path

from PIL import Image


ROOT = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\20\Raw + components"
)
RAW = ROOT / "raw -- synthetic_npp_electrical_schematic_v3_label_clearance.png"
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

        cols = 4
        rows = 4
        pad_x = 120
        pad_y = 100
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
            "01_top_13kv_4160_full": (350, 170, 4850, 1020),
            "02_top_left_sources": (420, 190, 2300, 830),
            "03_top_center_ties": (2100, 420, 3600, 900),
            "04_top_right_sources": (3150, 190, 4850, 850),
            "05_480_load_centers_full": (280, 980, 4880, 2360),
            "06_480_load_centers_left": (300, 1010, 1800, 2360),
            "07_480_load_centers_left_mid": (1600, 1010, 3000, 2360),
            "08_480_load_centers_right_mid": (2800, 1010, 4100, 2360),
            "09_480_load_centers_right": (3900, 1010, 5000, 2360),
            "10_bottom_dc_control_full": (300, 2280, 4900, 3520),
            "11_bottom_dc_control_a": (330, 2310, 2500, 3500),
            "12_bottom_dc_control_b": (2500, 2310, 4900, 3500),
            "13_notes_legend": (4930, 260, 6100, 1650),
            "14_title_revision": (4920, 3000, 6100, 4150),
            "15_main_drawing_area": (260, 180, 4920, 3520),
        }
        for name, box in boxes.items():
            save_crop(img, prefix, name, box)

        close_boxes = {
            "16_close_a_source_chain": (430, 200, 1400, 720),
            "17_close_a_4160_to_480": (1200, 500, 2050, 1160),
            "18_close_mid_13kv_4160_ties": (2100, 410, 3600, 920),
            "19_close_b_source_chain": (3400, 190, 4680, 750),
            "20_close_480_tie": (2400, 1040, 3100, 1340),
            "21_close_loads_a1": (320, 1120, 1500, 2350),
            "22_close_loads_a2": (1450, 1120, 2700, 2350),
            "23_close_loads_c": (2600, 1120, 3850, 2350),
            "24_close_loads_d": (3750, 1120, 4900, 2350),
            "25_close_dc_a_left": (340, 2400, 1900, 3450),
            "26_close_dc_a_right": (1600, 2400, 2750, 3450),
            "27_close_dc_b_left": (2500, 2400, 3800, 3450),
            "28_close_dc_b_right": (3600, 2400, 4900, 3450),
        }
        for name, box in close_boxes.items():
            save_crop(img, prefix, name, box, upscale=2)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    make_for_image(RAW, "raw")
    make_for_image(OVERLAY, "overlay")
    print(f"wrote Doc20 Raw + components visual aids to {OUT}")


if __name__ == "__main__":
    main()

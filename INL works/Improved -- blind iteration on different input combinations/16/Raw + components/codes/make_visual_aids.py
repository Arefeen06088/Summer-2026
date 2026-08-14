from __future__ import annotations

from pathlib import Path

from PIL import Image


ROOT = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\16\Raw + components"
)
RAW = ROOT / "raw -- synthetic_npp_electrical_schematic_revised(1).png"
OVERLAY = ROOT / "detected_components_and_logical_overlay.png"
OUT = ROOT / "results"


def save_preview(img: Image.Image, name: str, max_side: int = 1800) -> None:
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
        pad_x = 90
        pad_y = 80
        for row in range(rows):
            for col in range(cols):
                box = (
                    int(col * w / cols) - pad_x,
                    int(row * h / rows) - pad_y,
                    int((col + 1) * w / cols) + pad_x,
                    int((row + 1) * h / rows) + pad_y,
                )
                save_crop(img, prefix, f"grid_r{row + 1}c{col + 1}", box)

        boxes = {
            "01_top_band": (0, 0, w, int(h * 0.28)),
            "02_upper_middle_band": (0, int(h * 0.20), w, int(h * 0.50)),
            "03_middle_band": (0, int(h * 0.40), w, int(h * 0.72)),
            "04_bottom_band": (0, int(h * 0.65), w, h),
            "05_left_half": (0, 0, int(w * 0.54), h),
            "06_right_half": (int(w * 0.46), 0, w, h),
            "07_center": (int(w * 0.20), int(h * 0.18), int(w * 0.82), int(h * 0.82)),
            "08_title_block": (int(w * 0.58), int(h * 0.78), w, h),
            "09_notes_right": (int(w * 0.72), 0, w, int(h * 0.82)),
            "10_left_source_train": (0, 0, 1500, 930),
            "11_center_source_train": (1200, 0, 2700, 930),
            "12_right_source_train": (2400, 0, w, 930),
            "13_left_mid_controls": (0, 900, 1500, 1850),
            "14_center_mid_controls": (1300, 900, 2700, 1850),
            "15_right_mid_controls": (2450, 900, w, 1850),
            "16_left_lower_dc": (0, 1650, 1500, h),
            "17_center_lower_dc": (1300, 1650, 2700, h),
            "18_right_lower_dc": (2450, 1650, w, h),
        }
        for name, box in boxes.items():
            save_crop(img, prefix, name, box)

        close_boxes = {
            "19_close_cb11a_cb12a_cb21a": (250, 760, 1350, 1220),
            "20_close_480_tie_cb31a": (1280, 760, 1880, 1220),
            "21_close_mcc31a_cb11b": (1450, 780, 2250, 1250),
            "22_close_left_rps_control": (160, 1380, 1160, 1900),
            "23_close_esf_instruments": (1030, 1410, 1820, 1950),
            "24_close_right_rps_control": (1830, 1380, 2880, 1900),
            "25_close_right_instruments": (2440, 1410, 3200, 1900),
            "26_close_vital_a": (430, 1690, 1500, 2270),
            "27_close_vital_b": (1900, 1690, 2950, 2270),
            "28_close_bottom_left_batteries": (0, 2100, 1500, h),
            "29_close_bottom_right_batteries": (1650, 2100, 3200, h),
        }
        for name, box in close_boxes.items():
            save_crop(img, prefix, name, box, upscale=2)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    make_for_image(RAW, "raw")
    make_for_image(OVERLAY, "overlay")
    print(f"wrote Doc16 Raw + components visual aids to {OUT}")


if __name__ == "__main__":
    main()

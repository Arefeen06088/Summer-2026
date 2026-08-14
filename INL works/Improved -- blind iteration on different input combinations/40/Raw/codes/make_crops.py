from pathlib import Path

from PIL import Image


RAW_DIR = Path(__file__).resolve().parents[1]
RAW_IMAGE = RAW_DIR / "raw -- synthetic_nuclear_distribution_schematic.png"
OUT_DIR = RAW_DIR / "codes" / "crops"


def save_crop(img: Image.Image, name: str, box: tuple[int, int, int, int]) -> None:
    img.crop(box).save(OUT_DIR / f"{name}.png")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    img = Image.open(RAW_IMAGE)
    img.save(OUT_DIR / "full_sheet.png")

    crops = {
        "left_channel_top_sources": (330, 470, 2900, 1620),
        "right_channel_top_sources": (3000, 470, 5350, 1620),
        "center_tie_breaker": (2500, 930, 3650, 1370),
        "left_mcc_loads": (380, 1600, 2900, 2700),
        "right_mcc_loads": (3000, 1600, 5350, 2700),
        "left_rps_dc_logic": (380, 2550, 2900, 3600),
        "right_rps_dc_logic": (3000, 2550, 5350, 3600),
        "left_mcc_to_dc_interface": (2000, 2100, 2850, 3100),
        "right_mcc_to_dc_interface": (3000, 2100, 3900, 3100),
        "left_signal_lane": (400, 2680, 2100, 3600),
        "right_signal_lane": (4100, 2680, 5400, 3600),
        "notes_legend_index": (5350, 300, 6480, 3650),
        "title_block": (3900, 3650, 6480, 4520),
    }
    for name, box in crops.items():
        save_crop(img, name, box)

    width, height = img.size
    for row in range(4):
        for col in range(4):
            left = col * width // 4
            upper = row * height // 4
            right = (col + 1) * width // 4
            lower = (row + 1) * height // 4
            save_crop(img, f"grid_r{row + 1}_c{col + 1}", (left, upper, right, lower))

    print(f"Wrote crops to {OUT_DIR}")


if __name__ == "__main__":
    main()

from pathlib import Path
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "crops"
RESULTS.mkdir(parents=True, exist_ok=True)

RAW = ROOT / "raw -- schematic_image_clean_100_connected.png"
OVERLAY = ROOT / "wires_mask_overlay.png"

CROPS = {
    "01_ac_train_a": (450, 160, 1720, 1070),
    "02_ac_train_b": (1660, 160, 2900, 1070),
    "03_ac_train_c": (2860, 160, 3820, 1070),
    "04_480_loads_a": (480, 1020, 1620, 1980),
    "05_480_loads_b": (1680, 1020, 2860, 1980),
    "06_480_loads_c": (2860, 1020, 3820, 1980),
    "07_dc_ac_control_power": (460, 1880, 2920, 2920),
    "08_bus_tie_a_b": (1480, 410, 1840, 560),
    "09_bus_tie_b_c": (2740, 410, 3140, 560),
}


def main() -> None:
    for source_path in (RAW, OVERLAY):
        prefix = "raw" if source_path == RAW else "overlay"
        with Image.open(source_path) as image:
            for name, box in CROPS.items():
                crop = image.crop(box)
                crop.save(RESULTS / f"{prefix}_{name}.png")


if __name__ == "__main__":
    main()

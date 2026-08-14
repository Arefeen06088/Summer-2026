from pathlib import Path
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "crops"
RESULTS.mkdir(parents=True, exist_ok=True)

RAW = ROOT / "raw -- schematic_image_variant_b_100.png"
OVERLAY = ROOT / "wires_mask_overlay.png"

CROPS = {
    "01_top_train_a_sources": (1350, 350, 3950, 1650),
    "02_top_bus_tie": (4200, 1300, 5850, 1650),
    "03_top_train_b_sources": (5850, 350, 9100, 1650),
    "04_train_a_480_feeders": (700, 1450, 3900, 5450),
    "05_train_a_dc_rps": (3100, 3300, 4300, 6600),
    "06_cvcs_a": (3850, 1450, 5100, 4700),
    "07_train_b_480_feeders": (5150, 1450, 8500, 5450),
    "08_train_b_dc_rps": (7600, 3300, 8900, 6600),
    "09_cvcs_b": (8300, 1450, 9300, 4700),
    "10_title_notes": (9000, 900, 10650, 6900),
    "11_bottom_rps_control": (3300, 5400, 9400, 7050),
    "12_middle_cvcs_control": (3950, 2500, 9050, 6000),
}


def main() -> None:
    for source_path in (RAW, OVERLAY):
        prefix = "raw" if source_path == RAW else "overlay"
        with Image.open(source_path) as image:
            for name, box in CROPS.items():
                image.crop(box).save(RESULTS / f"{prefix}_{name}.png")


if __name__ == "__main__":
    main()

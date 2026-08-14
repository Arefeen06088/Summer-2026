from pathlib import Path
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "crops"
RESULTS.mkdir(parents=True, exist_ok=True)

RAW = ROOT / "raw -- synthetic_npp_electrical_schematic_variant3_redo_clean_v7.png"
OVERLAY = ROOT / "wires_mask_overlay.png"

CROPS = {
    "01_generator_switchyard": (200, 200, 4700, 1650),
    "02_medium_voltage_buses": (200, 900, 6100, 1900),
    "03_480_load_center_a": (200, 1650, 2700, 3150),
    "04_480_load_center_b": (3950, 1650, 5900, 3150),
    "05_non_safety_480": (2600, 1300, 3900, 2700),
    "05b_non_safety_loads": (2500, 2250, 4050, 3250),
    "06_dc_ups_distribution": (1900, 2950, 5400, 4100),
    "07_esfas_rps_control_bay": (6800, 600, 8850, 2450),
    "08_line_types_notes_title": (5200, 180, 8900, 4250),
}


def main() -> None:
    for source_path in (RAW, OVERLAY):
        prefix = "raw" if source_path == RAW else "overlay"
        with Image.open(source_path) as image:
            for name, box in CROPS.items():
                image.crop(box).save(RESULTS / f"{prefix}_{name}.png")


if __name__ == "__main__":
    main()

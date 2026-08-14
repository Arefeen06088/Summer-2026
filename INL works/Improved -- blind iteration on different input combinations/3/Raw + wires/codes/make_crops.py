from pathlib import Path
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "crops"
RESULTS.mkdir(parents=True, exist_ok=True)

RAW = ROOT / "raw -- synthetic_npp_100_component_electrical_schematic.png"
OVERLAY = ROOT / "wires_mask_overlay.png"

CROPS = {
    "01_top_left_sources_bus_a": (250, 220, 2450, 1180),
    "02_top_center_tie_dc": (2100, 520, 3750, 1900),
    "03_top_right_sources_bus_b": (3100, 220, 5100, 1180),
    "04_mcc_a1_a2_feeders": (280, 1600, 2600, 2850),
    "05_mcc_b1_b2_feeders": (2550, 1600, 4900, 2850),
    "06_loads_a1": (260, 2500, 1720, 3150),
    "07_loads_a2": (1680, 2500, 2630, 3150),
    "08_loads_b1": (2580, 2500, 3730, 3150),
    "09_loads_b2": (3700, 2500, 4960, 3150),
    "10_bottom_rps_esf_a": (1200, 3000, 2700, 3900),
    "11_bottom_rps_esf_b": (3000, 3000, 4450, 3900),
    "12_notes_legend_title": (5000, 250, 5900, 3800),
}


def main() -> None:
    for source_path in (RAW, OVERLAY):
        prefix = "raw" if source_path == RAW else "overlay"
        with Image.open(source_path) as image:
            for name, box in CROPS.items():
                image.crop(box).save(RESULTS / f"{prefix}_{name}.png")


if __name__ == "__main__":
    main()

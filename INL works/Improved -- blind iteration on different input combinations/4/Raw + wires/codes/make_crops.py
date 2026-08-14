from pathlib import Path
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "crops"
RESULTS.mkdir(parents=True, exist_ok=True)

RAW = ROOT / "raw.png"
OVERLAY = ROOT / "wires_mask_overlay.png"

CROPS = {
    "01_top_left_sources": (300, 250, 2200, 1550),
    "02_top_bus_and_loads_left": (850, 650, 3800, 2350),
    "03_top_bus_and_loads_right": (3500, 650, 7200, 2350),
    "04_left_vertical_feeder": (650, 1450, 1250, 3900),
    "05_dc_ups_rps_insert": (4300, 2100, 7300, 3600),
    "06_bottom_left_loads": (1000, 3800, 3600, 5200),
    "07_bottom_right_loads": (4300, 3800, 6300, 5200),
    "08_notes_legend_title": (7350, 300, 8500, 5200),
    "09_bottom_bus_tie": (700, 3300, 7600, 4600),
    "10_right_vertical_feeder": (6500, 1200, 8200, 5200),
}


def main() -> None:
    for source_path in (RAW, OVERLAY):
        prefix = "raw" if source_path == RAW else "overlay"
        with Image.open(source_path) as image:
            for name, box in CROPS.items():
                image.crop(box).save(RESULTS / f"{prefix}_{name}.png")


if __name__ == "__main__":
    main()

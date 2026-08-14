from pathlib import Path
from PIL import Image


BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "codes" / "visual_aids"
OUT.mkdir(parents=True, exist_ok=True)

RAW = BASE / "raw.png"
OVERLAY = BASE / "detected_components_and_logical_overlay.png"


CROPS = {
    "top_left_sources": (250, 250, 1700, 980),
    "top_mid_edg_a": (1650, 250, 2600, 980),
    "mid_left_sat_source": (250, 930, 1750, 1550),
    "top_buses_full": (760, 650, 7350, 1180),
    "upper_left_loads": (820, 1000, 2600, 2320),
    "upper_mid_left_loads": (2300, 980, 4300, 2320),
    "upper_mid_right_loads": (4100, 980, 6200, 2320),
    "upper_right_loads": (5850, 980, 7350, 2320),
    "left_vertical_source": (720, 1230, 1650, 3800),
    "right_vertical_source": (6750, 1750, 7350, 3650),
    "dc_rps_center": (4300, 2050, 7350, 3650),
    "dc_rps_zoom_a": (4400, 2150, 6350, 2950),
    "dc_rps_zoom_b": (4400, 2850, 6350, 3600),
    "rps_esfas_control_detail": (5750, 2100, 7350, 3900),
    "lower_left_loads": (950, 3650, 3650, 5250),
    "lower_right_loads": (4300, 3650, 6500, 5250),
    "full_left_working": (700, 650, 4300, 5350),
    "full_right_working": (4050, 650, 7400, 5350),
    "notes_legend_title": (7300, 280, 8600, 5250),
}


def crop_all(source: Path, prefix: str) -> None:
    image = Image.open(source)
    for name, box in CROPS.items():
        image.crop(box).save(OUT / f"{prefix}_{name}.png")


def main() -> None:
    crop_all(RAW, "raw")
    crop_all(OVERLAY, "overlay")
    print(f"Wrote {len(CROPS) * 2} crop files to {OUT}")


if __name__ == "__main__":
    main()

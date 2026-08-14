from __future__ import annotations

from pathlib import Path

from PIL import Image


Image.MAX_IMAGE_PIXELS = None

BASE = Path(__file__).resolve().parents[1]
CROPS = BASE / "codes" / "crops"
CROPS.mkdir(parents=True, exist_ok=True)

SOURCES = {
    "raw": BASE / "raw -- synthetic_npp_electrical_schematic_ats_components_shifted_v18.png",
    "components": BASE / "detected_components_overlay.png",
    "wires": BASE / "wires_mask_overlay.png",
    "wire_nodes": BASE / "wire_nodes_overlay.png",
}

CROPS_DEF = {
    "overview": (0, 0, 14400, 9400),
    "working_area": (600, 350, 13200, 8800),
    "top_left_source": (650, 500, 3700, 1900),
    "top_aux_buses_ab": (1700, 700, 6900, 2450),
    "top_aux_buses_cd": (6500, 700, 12200, 2450),
    "train_a_full": (650, 2200, 4000, 6500),
    "train_b_full": (3600, 2200, 6900, 6500),
    "train_c_full": (6500, 2200, 9900, 6500),
    "train_d_full": (9400, 2200, 12700, 6500),
    "train_a_loads_detail": (900, 3400, 3650, 5450),
    "train_b_loads_detail": (3850, 3400, 6600, 5450),
    "train_c_loads_detail": (6750, 3400, 9550, 5450),
    "train_d_loads_detail": (9650, 3400, 12450, 5450),
    "train_a_lower_controls": (900, 5200, 3700, 6550),
    "train_b_lower_controls": (3800, 5200, 6650, 6550),
    "train_c_lower_controls": (6700, 5200, 9600, 6550),
    "train_d_lower_controls": (9600, 5200, 12500, 6550),
    "dc_ups_full": (650, 6200, 12300, 8950),
    "dc_ups_left": (650, 6200, 5900, 8950),
    "dc_ups_right": (5700, 6200, 12300, 8950),
    "dc_bus_a_ups_a": (900, 6750, 5200, 8500),
    "dc_bus_b_ups_b": (5600, 6750, 9800, 8500),
    "control_power_center": (4200, 7300, 11000, 9100),
    "notes_legend": (12200, 600, 14100, 4900),
    "title_block": (12100, 7100, 14100, 9000),
}


def save_crop(source_name: str, source_path: Path, crop_name: str, box: tuple[int, int, int, int]) -> None:
    with Image.open(source_path) as image:
        image = image.convert("RGB")
        crop = image.crop(box)
        if crop_name == "overview":
            overview = crop.copy()
            overview.thumbnail((2400, 1600), Image.Resampling.LANCZOS)
            overview.save(CROPS / f"{source_name}__{crop_name}.png")
            return
        crop.save(CROPS / f"{source_name}__{crop_name}.png")
        crop.resize((crop.width * 2, crop.height * 2), Image.Resampling.LANCZOS).save(
            CROPS / f"{source_name}__{crop_name}_2x.png"
        )


def main() -> None:
    for source_name, source_path in SOURCES.items():
        for crop_name, box in CROPS_DEF.items():
            save_crop(source_name, source_path, crop_name, box)


if __name__ == "__main__":
    main()

from __future__ import annotations

from pathlib import Path

from PIL import Image

BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\20\Raw + wires + components + junctions")
CROPS = BASE / "codes" / "crops"

SOURCES = {
    "raw": BASE / "raw -- synthetic_npp_electrical_schematic_v3_label_clearance.png",
    "components": BASE / "detected_components_overlay.png",
    "wire_nodes": BASE / "wire_nodes_overlay.png",
    "wires": BASE / "wires_mask_overlay.png",
}

CROPS_DEF = {
    "full_working_area": (250, 130, 4850, 3500),
    "top_left_sources_bus_a": (430, 150, 1880, 900),
    "top_center_bus_ties": (1720, 230, 3270, 950),
    "top_right_sources_bus_b": (3070, 230, 4700, 950),
    "medium_voltage_left": (430, 520, 2450, 1230),
    "medium_voltage_right": (2450, 520, 4700, 1230),
    "load_centers_a_b": (360, 1110, 2140, 2370),
    "load_centers_b_c": (1660, 1110, 3460, 2370),
    "load_centers_c_d": (2700, 1110, 4720, 2370),
    "loads_left_detail": (360, 1230, 1500, 2300),
    "loads_mid_left_detail": (1450, 1230, 2600, 2300),
    "loads_mid_right_detail": (2500, 1230, 3650, 2300),
    "loads_right_detail": (3600, 1230, 4750, 2300),
    "dc_control_left": (330, 2230, 2450, 3450),
    "dc_control_right": (2450, 2230, 4750, 3450),
    "dc_control_a_detail": (350, 2320, 1250, 3350),
    "dc_control_a2_detail": (1350, 2320, 2350, 3350),
    "dc_control_b_detail": (2450, 2320, 3350, 3350),
    "dc_control_b2_detail": (3500, 2320, 4550, 3350),
    "notes_legend": (4920, 250, 6020, 1220),
}


def save_crop(img: Image.Image, name: str, box: tuple[int, int, int, int], scale: int = 1) -> None:
    crop = img.crop(box)
    if scale != 1:
        crop = crop.resize((crop.width * scale, crop.height * scale), Image.Resampling.LANCZOS)
    crop.save(CROPS / name)


def main() -> None:
    CROPS.mkdir(parents=True, exist_ok=True)
    for prefix, path in SOURCES.items():
        img = Image.open(path)
        for crop_name, box in CROPS_DEF.items():
            save_crop(img, f"{prefix}__{crop_name}.png", box, 1)
            if crop_name != "full_working_area":
                save_crop(img, f"{prefix}__{crop_name}_2x.png", box, 2)
        print(prefix, img.size)


if __name__ == "__main__":
    main()

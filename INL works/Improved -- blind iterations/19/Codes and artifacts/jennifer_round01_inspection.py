from pathlib import Path
from PIL import Image

BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\19")
INPUT = BASE / "Input resources"
ART = BASE / "Codes and artifacts" / "jennifer_round01_crops"

IMAGES = {
    "raw": INPUT / "raw -- synthetic_npp_electrical_schematic_v3.png",
    "det": INPUT / "detected_components_and_logical_detection_plus_ocr_overlay.png",
    "wires": INPUT / "wires_mask_overlay.png",
    "nodes": INPUT / "wire_nodes_overlay.png",
}

CROPS = {
    "full_top_buses": (700, 250, 7100, 1300),
    "a_feeders_left": (400, 1150, 4300, 3300),
    "b_feeders_right": (4550, 1150, 8200, 3300),
    "lower_control_dc": (500, 3200, 7800, 5250),
    "lower_a_control_120dc": (500, 3200, 3400, 5250),
    "lower_b_control_120dc": (5000, 3200, 7800, 5250),
    "ds_f301_area": (1780, 1120, 2100, 1620),
    "cb_f402_area": (5900, 1140, 6230, 1460),
    "mov601_ls_area": (3500, 2220, 3820, 2585),
    "lower_a_bus480_candidate": (700, 3000, 3000, 3650),
    "lower_b_bus480_candidate": (5200, 3000, 6400, 3650),
    "trace_a_cb301_from_bus480": (650, 950, 1150, 3650),
    "trace_a_chgr125a_from_bus480": (2550, 950, 3050, 3650),
    "trace_b_cb302_from_bus480": (5150, 950, 5650, 3650),
    "trace_b_chgr125b_from_bus480": (5900, 950, 6400, 3650),
}


def main():
    ART.mkdir(exist_ok=True)
    for image_name, path in IMAGES.items():
        image = Image.open(path)
        for crop_name, box in CROPS.items():
            image.crop(box).save(ART / f"{crop_name}__{image_name}.png")


if __name__ == "__main__":
    main()

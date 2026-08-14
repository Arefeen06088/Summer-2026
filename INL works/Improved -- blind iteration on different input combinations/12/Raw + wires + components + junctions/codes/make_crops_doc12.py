from pathlib import Path

from PIL import Image


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\12\Raw + wires + components + junctions"
)
CROPS_DIR = BASE / "codes" / "crops"

SOURCES = {
    "raw": BASE / "raw -- synthetic_npp_electrical_schematic_rps_rerouted.png",
    "detected": BASE / "detected_components_overlay.png",
    "wire_nodes": BASE / "wire_nodes_overlay.png",
    "wire_mask_overlay": BASE / "wires_mask_overlay.png",
}

CROPS = {
    "top_a_source": (140, 100, 1750, 820),
    "top_b_source": (1700, 100, 3230, 820),
    "tie_close": (1500, 430, 1900, 620),
    "train_a_mcc1": (190, 720, 1450, 1500),
    "train_a_mcc2": (190, 1450, 1450, 1940),
    "train_b_mcc1": (1850, 720, 3100, 1500),
    "train_b_mcc2": (1850, 1450, 3100, 1940),
    "dc_center": (1030, 1800, 2850, 2320),
    "bottom_logic_a": (760, 2240, 1700, 2740),
    "bottom_logic_b": (2150, 2240, 3100, 2740),
    "bottom_logic_center": (1500, 2170, 2300, 2700),
    "a_mcc1_labels_close": (210, 1050, 1150, 1470),
    "a_mcc2_labels_close": (330, 1550, 1290, 1910),
    "b_mcc1_labels_close": (1910, 1050, 2850, 1470),
    "b_mcc2_labels_close": (1980, 1550, 2850, 1910),
    "a_logic_close": (880, 2240, 1680, 2670),
    "b_logic_close": (2180, 2240, 3100, 2670),
    "dc_a_close": (1040, 1780, 1780, 2280),
    "dc_b_close": (2060, 1780, 2860, 2280),
    "notes_legend": (3240, 170, 4070, 1160),
    "title_block": (3240, 2140, 4070, 2820),
    "left_full": (120, 100, 1650, 2850),
    "center_full": (1500, 100, 2850, 2850),
    "right_full": (2700, 100, 4100, 2850),
}


def main() -> None:
    CROPS_DIR.mkdir(parents=True, exist_ok=True)
    for source_name, source_path in SOURCES.items():
        image = Image.open(source_path)
        for crop_name, box in CROPS.items():
            crop = image.crop(box)
            out_path = CROPS_DIR / f"{source_name}__{crop_name}.png"
            crop.save(out_path)
            print(out_path)


if __name__ == "__main__":
    main()

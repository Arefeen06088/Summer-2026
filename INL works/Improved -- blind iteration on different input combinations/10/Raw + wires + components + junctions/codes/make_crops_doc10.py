from pathlib import Path

from PIL import Image


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\10\Raw + wires + components + junctions"
)
CROPS_DIR = BASE / "codes" / "crops"

SOURCES = {
    "raw": BASE / "raw -- synthetic_nuclear_electrical_schematic_layout_labels_clear.png",
    "detected": BASE / "detected_components_overlay.png",
    "wire_nodes": BASE / "wire_nodes_overlay.png",
    "wire_mask_overlay": BASE / "wires_mask_overlay.png",
}

CROPS = {
    "top_sources": (80, 70, 2500, 420),
    "top_left_a_source": (120, 280, 1120, 760),
    "top_right_b_source_mcr": (1700, 280, 2700, 780),
    "mid_left_a_switchgear": (140, 520, 1280, 1180),
    "mid_right_b_switchgear": (1720, 520, 2600, 1180),
    "bottom_left_a_loads": (180, 1000, 1280, 1700),
    "bottom_right_b_loads": (1720, 1000, 2600, 1700),
    "dc_a": (180, 1650, 1280, 2110),
    "dc_b": (1700, 1650, 2600, 2110),
    "mcr_notes_legend": (2450, 330, 3260, 1810),
    "left_full": (80, 80, 1300, 2110),
    "center_full": (1100, 80, 2200, 2110),
    "right_full": (2000, 80, 3260, 2110),
    "a_control_close": (160, 720, 980, 1180),
    "b_control_close": (1650, 720, 2300, 1180),
    "a_lc_mcc_close": (650, 1020, 1260, 1660),
    "b_lc_mcc_close": (1800, 1020, 2400, 1660),
    "a_source_tie_close": (450, 390, 1300, 620),
    "b_source_tie_close": (1680, 390, 2250, 620),
    "a_fuses_ds_close": (430, 1180, 1050, 1500),
    "b_fuses_ds_close": (1500, 1180, 2050, 1500),
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

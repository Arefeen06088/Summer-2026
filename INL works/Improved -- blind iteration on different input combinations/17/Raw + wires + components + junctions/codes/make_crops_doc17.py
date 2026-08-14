from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\17\Raw + wires + components + junctions")
OUT = BASE / "codes" / "crops"
OUT.mkdir(parents=True, exist_ok=True)

IMAGES = {
    "raw": BASE / "raw -- synthetic_npp_aux_power_schematic_overlap_fixed.png",
    "detected": BASE / "detected_components_overlay.png",
    "wire_nodes": BASE / "wire_nodes_overlay.png",
    "wire_mask_overlay": BASE / "wires_mask_overlay.png",
}

CROPS = {
    "full_left_train": (180, 170, 2160, 1900),
    "full_right_train": (2140, 170, 4100, 1900),
    "top_sources_left": (250, 210, 2120, 900),
    "top_sources_right": (2210, 210, 3950, 900),
    "ac_bus_tie_center": (1800, 220, 2380, 1280),
    "ac_tie_mid": (1700, 980, 2360, 1420),
    "left_mcc_feeders": (220, 1080, 1980, 1840),
    "left_mcc_feeders_01_05": (220, 1080, 980, 1840),
    "left_mcc_feeders_06_09": (900, 1080, 1560, 1840),
    "left_mcc_feeders_10_12": (1460, 1080, 1980, 1840),
    "right_mcc_feeders": (2260, 1080, 3980, 1840),
    "right_mcc_feeders_01_05": (2260, 1080, 2960, 1840),
    "right_mcc_feeders_06_09": (2880, 1080, 3500, 1840),
    "right_mcc_feeders_10_12": (3420, 1080, 3980, 1840),
    "left_dc_ups": (180, 2040, 2260, 3480),
    "right_dc_ups": (2220, 2040, 4200, 3480),
    "center_annunciator_controls": (1580, 2380, 2860, 3440),
    "dc_tie_center": (1900, 2480, 2320, 2880),
    "notes_legend": (4180, 220, 5400, 2360),
    "title_block": (4180, 2380, 5400, 3520),
}


def main() -> None:
    for prefix, path in IMAGES.items():
        with Image.open(path) as img:
            for name, box in CROPS.items():
                img.crop(box).save(OUT / f"{prefix}__{name}.png")


if __name__ == "__main__":
    main()

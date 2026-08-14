from pathlib import Path

from PIL import Image


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\13\Raw + wires + components + junctions"
)
CROPS_DIR = BASE / "codes" / "crops"

SOURCES = {
    "raw": BASE / "raw -- synthetic diagram _.png",
    "detected": BASE / "detected_components_overlay.png",
    "wire_nodes": BASE / "wire_nodes_overlay.png",
    "wire_mask_overlay": BASE / "wires_mask_overlay.png",
}

CROPS = {
        "incoming_station_feed": (320, 360, 2300, 900),
        "top_ab_source_feed": (300, 360, 5000, 1200),
        "top_cd_source_feed": (300, 1750, 5000, 2450),
    "train_a_full": (350, 730, 2600, 1860),
    "train_b_full": (2650, 730, 4900, 1860),
    "train_c_full": (350, 1950, 2600, 3150),
    "train_d_full": (2650, 1950, 4900, 3150),
    "train_a_4kv_480": (450, 750, 2500, 1150),
    "train_b_4kv_480": (2750, 750, 4800, 1150),
    "train_c_4kv_480": (450, 1980, 2500, 2380),
    "train_d_4kv_480": (2750, 1980, 4800, 2380),
    "train_a_mcc_close": (470, 1100, 2460, 1650),
    "train_b_mcc_close": (2770, 1100, 4760, 1650),
    "train_c_mcc_close": (470, 2320, 2460, 2880),
    "train_d_mcc_close": (2770, 2320, 4760, 2880),
    "train_a_dc_ups_close": (2180, 1150, 2560, 1660),
    "train_b_dc_ups_close": (4480, 1150, 4860, 1660),
    "train_c_dc_ups_close": (2180, 2370, 2560, 2900),
    "train_d_dc_ups_close": (4480, 2370, 4860, 2900),
    "bottom_ground_plant": (470, 3200, 2820, 3700),
    "notes_legend_schedule": (5050, 220, 6200, 2920),
    "title_block": (5050, 3100, 6200, 4100),
    "left_half": (250, 300, 2700, 3600),
    "right_half": (2500, 300, 5000, 3600),
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

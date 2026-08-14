from __future__ import annotations

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "visual_crops"

SOURCES = [
    "raw -- synthetic_nuclear_electrical_schematic_layout_labels_clear.png",
    "detected_components_overlay.png",
    "wires_mask.png",
    "wires_mask_overlay.png",
]

CROPS = {
    "whole_drawing_area": (50, 50, 3200, 2110),
    "top_source_and_345kv_bus": (110, 110, 2600, 380),
    "train_a_main_switchgear": (110, 360, 1160, 1390),
    "train_b_main_switchgear": (1260, 360, 2310, 1390),
    "train_a_lower_control_power": (110, 1170, 1160, 2010),
    "train_b_lower_control_power": (1260, 1170, 2310, 2010),
    "mcr_annunciator_control_bay": (2310, 380, 2680, 1020),
    "notes_legend_title": (2660, 90, 3180, 2040),
}

FOCUSED = {
    "left_source_uat_dg_zoom": (120, 120, 1160, 620),
    "right_source_sat_dg_zoom": (1260, 120, 2250, 620),
    "train_a_breakers_loads_zoom": (430, 520, 1160, 1160),
    "train_b_breakers_loads_zoom": (1650, 520, 2300, 1160),
    "train_a_instrument_relays_zoom": (130, 460, 520, 1260),
    "train_b_instrument_relays_zoom": (1300, 460, 1700, 1260),
    "train_a_lc_mcc_mov_zoom": (560, 1120, 1160, 1690),
    "train_b_lc_mcc_mov_zoom": (1690, 1120, 2300, 1690),
    "train_a_dc_ups_zoom": (160, 1700, 1160, 2020),
    "train_b_dc_ups_zoom": (1300, 1700, 2300, 2020),
    "control_bay_zoom": (2320, 420, 2650, 980),
    "center_separation_zoom": (1120, 360, 1350, 2020),
}


def safe_stem(path: Path) -> str:
    return "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in path.stem)


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    for source in SOURCES:
        path = ROOT / source
        with Image.open(path) as image:
            out_dir = RESULTS / safe_stem(path)
            out_dir.mkdir(parents=True, exist_ok=True)
            for name, box in CROPS.items():
                image.crop(box).save(out_dir / f"{name}.png")
            if source.startswith("raw --"):
                focused_dir = RESULTS / "focused_raw"
                focused_dir.mkdir(parents=True, exist_ok=True)
                for name, box in FOCUSED.items():
                    image.crop(box).save(focused_dir / f"{name}.png")
    print(f"wrote crops to {RESULTS}")


if __name__ == "__main__":
    main()

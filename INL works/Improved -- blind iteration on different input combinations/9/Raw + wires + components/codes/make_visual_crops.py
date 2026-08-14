from __future__ import annotations

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "visual_crops"

SOURCES = [
    "raw -- synthetic_npp_schematic_expanded_clear_refined_v3_reworked.png",
    "detected_components_overlay.png",
    "wires_mask.png",
    "wires_mask_overlay.png",
]

CROPS = {
    "whole_schematic_area": (80, 90, 4940, 3150),
    "top_sources_and_switchgear": (120, 130, 4300, 650),
    "middle_buses_and_transformers": (120, 560, 4100, 1500),
    "left_train_loads": (120, 730, 1460, 2390),
    "center_normal_distribution": (1420, 560, 2820, 2370),
    "right_train_loads": (2680, 730, 4100, 2390),
    "left_train_control": (120, 2380, 1580, 3100),
    "right_train_control": (2680, 2380, 4100, 3100),
    "bottom_interlock_controls": (120, 1770, 4100, 3120),
    "title_legend_notes": (4320, 420, 4880, 2980),
}

FOCUSED = {
    "top_left_source_zoom": (130, 150, 1180, 620),
    "top_center_gen_tie_zoom": (980, 150, 2680, 770),
    "top_right_source_zoom": (3240, 150, 4140, 650),
    "middle_left_bus_zoom": (120, 700, 1510, 1480),
    "middle_center_normal_zoom": (1440, 560, 2810, 1670),
    "middle_right_bus_zoom": (2680, 700, 4100, 1480),
    "left_mcc_loads_zoom": (150, 1380, 1410, 2290),
    "right_mcc_loads_zoom": (2740, 1380, 4020, 2290),
    "left_mov_panel_zoom": (720, 1980, 1470, 2380),
    "right_mov_panel_zoom": (3280, 1980, 4020, 2380),
    "left_control_zoom": (130, 2390, 1570, 3080),
    "right_control_zoom": (2710, 2390, 4080, 3080),
    "normal_aux_loads_zoom": (1460, 1320, 2730, 2190),
    "sequence_controls_zoom": (1600, 1850, 2550, 2310),
    "left_k_relays_zoom": (960, 2680, 1510, 3060),
    "right_k_relays_zoom": (3420, 2680, 4050, 3060),
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

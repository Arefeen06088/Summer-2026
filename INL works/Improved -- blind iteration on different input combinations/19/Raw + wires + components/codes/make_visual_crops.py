from __future__ import annotations

from pathlib import Path

from PIL import Image


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\19\Raw + wires + components"
)
RESULTS = BASE / "results"
CROPS = RESULTS / "visual_crops"


def save_crop(src: Path, out_dir: Path, name: str, box: tuple[int, int, int, int], scale: float = 1.0) -> None:
    image = Image.open(src)
    crop = image.crop(box)
    if scale != 1.0:
        crop = crop.resize((round(crop.width * scale), round(crop.height * scale)), Image.Resampling.LANCZOS)
    out_dir.mkdir(parents=True, exist_ok=True)
    crop.save(out_dir / f"{name}.png")


def main() -> None:
    raw = BASE / "raw -- synthetic_npp_electrical_schematic_v3.png"
    wire_overlay = BASE / "wires_mask_overlay.png"
    detected = BASE / "detected_components_overlay.png"
    wire_mask = BASE / "wires_mask.png"

    broad = {
        "whole_drawing_area": (150, 120, 8900, 5450),
        "top_left": (400, 220, 3350, 1220),
        "top_center": (3000, 220, 6300, 1220),
        "top_right": (5800, 220, 8050, 1220),
        "loads_left": (360, 1000, 2820, 3100),
        "loads_midleft": (2500, 1000, 4420, 3100),
        "loads_midright": (4050, 1000, 6100, 3100),
        "loads_right": (5700, 1000, 7800, 3100),
        "lower_left": (450, 2950, 3150, 4100),
        "lower_center": (2700, 2950, 6100, 4100),
        "lower_right": (5200, 2950, 7600, 4100),
        "notes_title": (7700, 350, 9050, 5400),
    }
    for src in (raw, wire_overlay, detected, wire_mask):
        out_dir = CROPS / src.stem.replace(" -- ", "_").replace(" ", "_")
        for name, box in broad.items():
            save_crop(src, out_dir, name, box)

    focused = {
        "top_all_buses_sources": (480, 250, 7350, 1120),
        "top_division_a": (650, 250, 4100, 1120),
        "top_division_b": (3900, 250, 7350, 1120),
        "tie_between_480_buses": (3600, 580, 4650, 1150),
        "feeders_a_01_03": (470, 1050, 2850, 3100),
        "feeders_a_04_06": (2200, 1050, 4100, 3100),
        "feeders_b_01_03": (3950, 1050, 5750, 3100),
        "feeders_b_04_06": (5450, 1050, 7500, 3100),
        "lower_125a_120a": (550, 3050, 4000, 4050),
        "lower_125b_120b": (4850, 3050, 7400, 4050),
        "right_notes": (7800, 520, 9000, 2450),
        "title_block": (7800, 4050, 9000, 5350),
        "zoom_top_a_source": (650, 250, 1700, 900),
        "zoom_top_a_bus_end": (2650, 450, 4300, 1120),
        "zoom_top_b_source": (5000, 250, 6400, 900),
        "zoom_top_b_bus_end": (6100, 450, 7480, 1120),
        "zoom_lower_a_controls": (2750, 3350, 3900, 3920),
        "zoom_lower_b_controls": (6100, 3350, 7250, 3920),
    }
    focused_dir = CROPS / "focused_raw"
    for name, box in focused.items():
        save_crop(raw, focused_dir, name, box, scale=1.5)

    print(f"wrote crops under {CROPS}")


if __name__ == "__main__":
    main()

from __future__ import annotations

from pathlib import Path

from PIL import Image


BASE_DIR = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\21\Raw + wires + components")
RESULTS_DIR = BASE_DIR / "results"
CROP_DIR = RESULTS_DIR / "visual_crops"

RAW = BASE_DIR / "raw -- synthetic_npp_electrical_schematic_fixed.png"
OVERLAY = BASE_DIR / "detected_components_overlay.png"
WIRE_OVERLAY = BASE_DIR / "wires_mask_overlay.png"
WIRE_MASK = BASE_DIR / "wires_mask.png"


def clamp_box(box: tuple[int, int, int, int], width: int, height: int) -> tuple[int, int, int, int]:
    left, top, right, bottom = box
    return max(0, left), max(0, top), min(width, right), min(height, bottom)


def save_crop(source: Path, out_name: str, box: tuple[int, int, int, int]) -> None:
    image = Image.open(source)
    crop = image.crop(clamp_box(box, image.width, image.height))
    crop.save(CROP_DIR / out_name)


def save_zoom_crop(source: Path, out_name: str, box: tuple[int, int, int, int], scale: int = 4) -> None:
    image = Image.open(source)
    crop = image.crop(clamp_box(box, image.width, image.height))
    crop = crop.resize((crop.width * scale, crop.height * scale), Image.Resampling.LANCZOS)
    crop.save(CROP_DIR / out_name)


def main() -> None:
    CROP_DIR.mkdir(parents=True, exist_ok=True)

    crops = {
        "top_all_aux_and_416": (280, 420, 5850, 1360),
        "top_left_aux_sources": (300, 430, 1980, 1290),
        "top_center_416_buses": (1980, 420, 5900, 1340),
        "top_right_emergency_sources": (4000, 430, 5900, 1320),
        "top_edg_feeders_detail": (3250, 640, 5900, 1360),
        "middle_train_a_all": (300, 1320, 3040, 2750),
        "middle_train_a_taps_detail": (360, 1320, 2320, 2060),
        "middle_train_a_loads": (430, 1880, 2240, 2680),
        "middle_train_b_all": (3020, 1320, 5850, 2750),
        "middle_train_b_taps_detail": (3380, 1320, 5360, 2060),
        "middle_train_b_loads": (3460, 1880, 5270, 2680),
        "feeders_416_to_480": (2050, 1200, 3830, 1920),
        "bottom_dc_ups_all": (300, 2720, 3000, 4250),
        "bottom_dc_ups_left": (300, 2720, 1700, 4250),
        "bottom_dc_ups_right": (1500, 2720, 3000, 4250),
        "middle_to_dc_transition_left": (300, 2300, 2200, 3200),
        "middle_to_dc_transition_right": (1450, 2300, 3400, 3200),
        "dc_ups_bus_handoff_detail": (2350, 2580, 3650, 3500),
        "dc_ups_switchgear_detail": (360, 2580, 2600, 3520),
        "control_logic_all": (2950, 2730, 5850, 4250),
        "control_logic_left_sources": (2950, 2730, 3740, 4250),
        "control_logic_rows_left": (3600, 2730, 4640, 4250),
        "control_logic_rows_right": (4520, 2730, 5850, 4250),
        "control_logic_bottom_crd": (2950, 3860, 4630, 4900),
        "control_logic_lower_full": (2950, 3600, 5850, 4900),
        "notes_legend": (6000, 430, 6940, 1900),
        "title_block": (5980, 3440, 6940, 4450),
    }

    for name, box in crops.items():
        save_crop(RAW, f"{name}_raw.png", box)
        save_crop(OVERLAY, f"{name}_components.png", box)
        save_crop(WIRE_OVERLAY, f"{name}_wires_overlay.png", box)

    zoom_crops = {
        "zoom_edg_1b_left_breaker_label": (3970, 710, 4460, 900),
        "zoom_edg_2a_left_breaker_label": (3920, 920, 4420, 1130),
        "zoom_edg_2b_left_disconnect_label": (4260, 1130, 4730, 1340),
    }
    for name, box in zoom_crops.items():
        save_zoom_crop(RAW, f"{name}_raw.png", box)
        save_zoom_crop(OVERLAY, f"{name}_components.png", box)

    for name, source in {
        "raw_full": RAW,
        "components_full": OVERLAY,
        "wires_overlay_full": WIRE_OVERLAY,
        "wires_mask_full": WIRE_MASK,
    }.items():
        image = Image.open(source)
        image.thumbnail((2600, 1900))
        image.save(CROP_DIR / f"{name}_thumb.png")

    print(f"wrote crops to {CROP_DIR}")


if __name__ == "__main__":
    main()

from __future__ import annotations

from pathlib import Path

from PIL import Image


BASE_DIR = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\22\Raw + wires + components")
RESULTS_DIR = BASE_DIR / "results"
CROP_DIR = RESULTS_DIR / "visual_crops"

RAW = BASE_DIR / "raw -- synthetic_npp_electrical_schematic_clean.png"
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
        "doc22_full_power_top": (320, 210, 5700, 1460),
        "doc22_source_and_aux_bus": (360, 240, 3280, 970),
        "doc22_aux_bus_b_and_sat": (3200, 360, 5750, 980),
        "doc22_4160_buses_all": (330, 900, 5800, 1600),
        "doc22_train_a_all": (380, 1500, 1900, 3300),
        "doc22_train_b_all": (1840, 1500, 3330, 3300),
        "doc22_train_c_all": (3260, 1500, 4760, 3300),
        "doc22_train_d_all": (4680, 1500, 6200, 3300),
        "doc22_train_a_mcc_loads": (450, 1760, 1780, 2750),
        "doc22_train_b_mcc_loads": (1920, 1760, 3230, 2750),
        "doc22_train_c_mcc_loads": (3350, 1760, 4660, 2750),
        "doc22_train_d_mcc_loads": (4770, 1760, 6080, 2750),
        "doc22_bottom_ups_all": (400, 3370, 5900, 4940),
        "doc22_bottom_ups_left_a": (430, 3370, 2940, 4940),
        "doc22_bottom_ups_right_b": (2900, 3370, 5900, 4940),
        "doc22_bottom_control_center": (2450, 3700, 5200, 5050),
        "doc22_meter_area": (4920, 3350, 5700, 4200),
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
        "zoom_top_label_left": (700, 550, 1500, 950),
        "zoom_edg_1b_left_breaker_label": (3970, 710, 4460, 900),
        "zoom_edg_2a_left_breaker_label": (3920, 920, 4420, 1130),
        "zoom_edg_2b_left_disconnect_label": (4260, 1130, 4730, 1340),
        "zoom_train_a_loads_labels": (430, 1900, 2300, 2660),
        "zoom_train_b_loads_labels": (3460, 1900, 5350, 2660),
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

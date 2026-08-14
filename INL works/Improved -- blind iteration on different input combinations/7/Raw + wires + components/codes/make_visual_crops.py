from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "visual_crops"

SOURCES = [
    "raw -- synthetic_npp_electrical_schematic_clean (1).png",
    "detected_components_and_logical_overlay.png",
    "wires_mask.png",
    "wires_mask_overlay.png",
]

CROPS = {
    "top_aux_power_and_sources": (220, 240, 5750, 1450),
    "left_train_ab_loads": (320, 1450, 2850, 3050),
    "right_train_cd_loads": (3000, 1450, 5700, 3050),
    "left_train_a_dc_control": (340, 2900, 2600, 4480),
    "right_train_b_dc_control": (3150, 2900, 5650, 4480),
    "bottom_interlock_raceways": (1250, 3050, 5300, 4480),
    "whole_functional_area": (220, 230, 5850, 4480),
    "title_legend_notes": (5700, 350, 7000, 4450),
}


def safe_stem(name):
    return "".join(ch if ch.isalnum() else "_" for ch in Path(name).stem)


def main():
    RESULTS.mkdir(parents=True, exist_ok=True)
    for source in SOURCES:
        image = Image.open(ROOT / source)
        out_dir = RESULTS / safe_stem(source)
        out_dir.mkdir(parents=True, exist_ok=True)
        for crop_name, box in CROPS.items():
            image.crop(box).save(out_dir / f"{crop_name}.png")
    print(f"wrote crops to {RESULTS}")


if __name__ == "__main__":
    main()

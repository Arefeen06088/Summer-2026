from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
CROPS = RESULTS / "crops"
RAW = ROOT / "raw -- synthetic_npp_electrical_schematic_clean (1).png"
OVERLAY = ROOT / "wires_mask_overlay.png"
MASK = ROOT / "wires_mask.png"


CROPS.mkdir(parents=True, exist_ok=True)

REGIONS = {
    "01_top_left_sources_train_a": (250, 220, 2800, 1450),
    "02_top_center_bus_ties": (2500, 220, 5000, 1450),
    "03_top_right_sources_train_b": (4300, 220, 6200, 1450),
    "04_train_a_load_centers": (350, 1300, 2900, 3150),
    "05_train_b_load_centers": (3300, 1300, 5900, 3150),
    "06_train_a_dc_control": (350, 3000, 2900, 4550),
    "07_train_b_dc_control": (3300, 3000, 5900, 4550),
    "08_bottom_cross_control": (1600, 3800, 4300, 4650),
    "09_notes_legend_title": (5750, 400, 7050, 4650),
    "10_full_left_system": (250, 220, 3600, 4550),
    "11_full_right_system": (3300, 220, 6200, 4550),
    "12_title_block": (5750, 3650, 7050, 4650),
}


def save_crops(source: Path, prefix: str) -> None:
    with Image.open(source) as im:
        for name, box in REGIONS.items():
            im.crop(box).save(CROPS / f"{prefix}_{name}.png")


def main() -> None:
    save_crops(RAW, "raw")
    save_crops(OVERLAY, "overlay")
    save_crops(MASK, "mask")
    print(f"Wrote {len(REGIONS) * 3} crops to {CROPS}")


if __name__ == "__main__":
    main()

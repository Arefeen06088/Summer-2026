from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\40")
INPUT = BASE / "Input resources"
OUT = BASE / "Codes and artifacts" / "inspection_crops_doc40_current" / "focus"
RAW = INPUT / "synthetic_nuclear_distribution_schematic.png"
COMP_OVERLAY = INPUT / "component_and_logical_labels_banners_overlay.png"
WIRE_OVERLAY = INPUT / "wire_nodes_overlay.png"


REGIONS = {
    "top_train_a_sources_swgr": (360, 520, 3020, 1720),
    "top_train_b_sources_swgr": (2860, 520, 5480, 1720),
    "mcc_train_a_loads": (420, 1650, 2750, 2850),
    "mcc_train_b_loads": (2960, 1650, 5320, 2850),
    "dc_rps_train_a": (420, 2700, 2680, 3650),
    "dc_rps_train_b": (3150, 2700, 5300, 3650),
    "central_tie_and_cpt": (2400, 1040, 3380, 2500),
}


def crop(src: Path, prefix: str) -> None:
    img = Image.open(src).convert("RGB")
    for name, box in REGIONS.items():
        img.crop(box).save(OUT / f"{prefix}_{name}.png")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    crop(RAW, "raw")
    crop(COMP_OVERLAY, "component_overlay")
    crop(WIRE_OVERLAY, "wire_nodes")
    print(f"Wrote focus crops to {OUT}")


if __name__ == "__main__":
    main()

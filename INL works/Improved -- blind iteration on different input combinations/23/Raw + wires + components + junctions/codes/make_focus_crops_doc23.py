from __future__ import annotations

from pathlib import Path

from PIL import Image


Image.MAX_IMAGE_PIXELS = None

BASE = Path(__file__).resolve().parents[1]
CROPS = BASE / "codes" / "crops"
CROPS.mkdir(parents=True, exist_ok=True)

RAW = BASE / "raw -- synthetic_npp_electrical_schematic_ats_components_shifted_v18.png"
NODES = BASE / "wire_nodes_overlay.png"
COMPONENTS = BASE / "detected_components_overlay.png"

FOCUS = {
    "top_full_power": (400, 500, 11200, 3250),
    "ats_1a_detail": (400, 1900, 2500, 3300),
    "ats_1b_detail": (9000, 1900, 11300, 3300),
    "dc_a_source_entry": (300, 6000, 2600, 7350),
    "dc_b_source_entry": (6500, 6000, 9300, 7350),
    "lower_dc_cross_tie": (5200, 6500, 8200, 8200),
    "vital_ac_a_detail": (1500, 7700, 6500, 9150),
    "vital_ac_b_detail": (6800, 7700, 11600, 9150),
}


def emit(source_name: str, source_path: Path) -> None:
    with Image.open(source_path) as image:
        image = image.convert("RGB")
        for crop_name, box in FOCUS.items():
            crop = image.crop(box)
            crop.save(CROPS / f"{source_name}__{crop_name}.png")
            crop.resize((crop.width * 2, crop.height * 2), Image.Resampling.LANCZOS).save(
                CROPS / f"{source_name}__{crop_name}_2x.png"
            )


def main() -> None:
    emit("raw", RAW)
    emit("wire_nodes", NODES)
    emit("components", COMPONENTS)


if __name__ == "__main__":
    main()

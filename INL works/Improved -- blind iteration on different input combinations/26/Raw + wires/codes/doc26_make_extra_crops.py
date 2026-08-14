from pathlib import Path

from PIL import Image


BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\26\Raw + wires"
)
CROPS = BASE / "codes" / "crops"

SOURCES = {
    "raw": BASE / "raw -- synthetic_npp_electrical_schematic_v3(1).png",
    "wires_overlay": BASE / "wires_mask_overlay.png",
}

# Raw-sheet coordinate windows. These tighten the RCP dashed interlock areas,
# because the first broad focus crop clipped the RCP branch itself.
BOXES = {
    "zoom_rcp_a": (1230, 760, 1660, 1705),
    "zoom_rcp_b": (4505, 760, 4945, 1705),
}


def main() -> None:
    CROPS.mkdir(parents=True, exist_ok=True)
    for source_name, source_path in SOURCES.items():
        image = Image.open(source_path)
        for crop_name, box in BOXES.items():
            image.crop(box).save(CROPS / f"{source_name}__{crop_name}.png")
            print(f"{source_name}__{crop_name}.png {box}")


if __name__ == "__main__":
    main()

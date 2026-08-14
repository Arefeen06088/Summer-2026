from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\2\Raw")
SOURCE = BASE / "raw -- schematic_image_variant_b_100.png"
OUT = BASE / "results" / "crops"


def save_crop(img: Image.Image, name: str, box: tuple[int, int, int, int], scale: int = 2) -> None:
    crop = img.crop(box)
    if scale != 1:
        crop = crop.resize((crop.width * scale, crop.height * scale), Image.Resampling.LANCZOS)
    crop.save(OUT / f"{name}.png")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    img = Image.open(SOURCE)
    crops = {
        "top_bus_a": (900, 350, 5100, 1850),
        "top_bus_b": (5000, 350, 9100, 1850),
        "left_feeders": (700, 1500, 4100, 5300),
        "right_feeders": (5200, 1500, 9100, 5300),
        "a_mcc_feeders": (850, 1700, 3250, 5250),
        "a_dc_rps": (3100, 1650, 4550, 6500),
        "b_mcc_feeders": (5250, 1700, 7600, 5250),
        "b_dc_rps": (7600, 1650, 8800, 6500),
        "tie_ab": (4300, 1200, 5600, 1650),
        "common_loads_a_b": (4050, 1500, 9000, 5400),
        "rps_crosslink": (3300, 5100, 8350, 6650),
        "notes_title": (9000, 900, 10700, 6900),
    }
    for name, box in crops.items():
        save_crop(img, name, box)


if __name__ == "__main__":
    main()

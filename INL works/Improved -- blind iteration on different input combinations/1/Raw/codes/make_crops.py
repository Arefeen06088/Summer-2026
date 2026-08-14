from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\1\Raw")
SOURCE = BASE / "raw -- schematic_image_clean_100_connected.png"
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
        "full_left_trains_a_b": (430, 150, 2750, 980),
        "upper_train_a": (430, 155, 1600, 900),
        "upper_train_b": (1600, 155, 2800, 900),
        "upper_train_c": (2750, 155, 3720, 900),
        "mcc_train_a": (430, 820, 1600, 1810),
        "mcc_train_b": (1600, 820, 2800, 1810),
        "mcc_train_c": (2750, 820, 3720, 1810),
        "dc_ups_rps": (430, 1740, 2800, 2960),
        "dc_bus_a": (430, 1780, 1620, 2620),
        "dc_bus_b": (1600, 1780, 2800, 2620),
        "rps_controls": (430, 2300, 2800, 2960),
        "notes_legend_title": (3600, 190, 4680, 2980),
    }
    for name, box in crops.items():
        save_crop(img, name, box)


if __name__ == "__main__":
    main()

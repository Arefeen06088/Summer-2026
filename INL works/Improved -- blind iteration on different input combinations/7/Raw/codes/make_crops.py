from pathlib import Path

from PIL import Image


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\7\Raw")
RAW = BASE / "raw -- synthetic_npp_electrical_schematic_clean (1).png"
OUT = BASE / "results" / "crops"


def crop(image: Image.Image, name: str, box: tuple[int, int, int, int]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    image.crop(box).save(OUT / f"{name}.png")


def main() -> None:
    image = Image.open(RAW)
    crops = {
        "top_aux_standby_sources": (250, 240, 5700, 1650),
        "top_left_sources_detail": (250, 260, 3050, 1550),
        "top_right_sources_detail": (2900, 260, 5700, 1550),
        "train_a_load_centers": (360, 1500, 2920, 3120),
        "train_b_load_centers": (3140, 1500, 5900, 3120),
        "train_a_dc_control": (360, 3100, 2940, 4550),
        "train_b_dc_control": (3250, 3100, 5940, 4550),
        "train_a_load_detail": (560, 1800, 2550, 2960),
        "train_b_load_detail": (3350, 1800, 5580, 2960),
        "dc_cross_ties_detail": (1500, 3300, 5600, 4560),
        "train_a_dc_relay_detail": (1450, 3500, 3850, 4520),
        "train_b_dc_relay_detail": (3850, 3500, 6100, 4520),
        "legend_title": (5850, 420, 7100, 4620),
    }
    for name, box in crops.items():
        crop(image, name, box)


if __name__ == "__main__":
    main()

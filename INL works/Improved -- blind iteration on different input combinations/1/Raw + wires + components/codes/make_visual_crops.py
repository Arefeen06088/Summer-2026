from pathlib import Path

from PIL import Image, ImageDraw


BASE = Path(__file__).resolve().parents[1]
RESULTS = BASE / "results" / "visual_crops"


REGIONS = [
    ("top_bus_A_and_source", (440, 160, 1650, 1120)),
    ("top_bus_B_and_source", (1680, 160, 2850, 1120)),
    ("top_bus_C_and_source", (2880, 160, 3840, 1120)),
    ("loads_480_A", (440, 1040, 1650, 1960)),
    ("loads_480_B", (1680, 1040, 2850, 1960)),
    ("loads_480_C", (2880, 1040, 3840, 1960)),
    ("dc_ups_rps", (440, 1900, 2920, 2920)),
]


def crop_and_scale(source_name: str, scale: int = 2) -> None:
    src = BASE / source_name
    image = Image.open(src).convert("RGB")
    out_dir = RESULTS / src.stem.replace(" ", "_")
    out_dir.mkdir(parents=True, exist_ok=True)

    overview = image.copy()
    draw = ImageDraw.Draw(overview)
    for label, box in REGIONS:
        draw.rectangle(box, outline=(255, 0, 0), width=6)
        draw.text((box[0] + 8, box[1] + 8), label, fill=(255, 0, 0))
        crop = image.crop(box)
        crop = crop.resize((crop.width * scale, crop.height * scale), Image.Resampling.LANCZOS)
        crop.save(out_dir / f"{label}.png")

    overview.save(out_dir / "crop_overview.png")


if __name__ == "__main__":
    crop_and_scale("raw -- schematic_image_clean_100_connected.png", scale=2)
    crop_and_scale("detected_components_and_logical_overlay.png", scale=2)

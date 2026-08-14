from pathlib import Path

from PIL import Image, ImageDraw


BASE = Path(__file__).resolve().parents[1]
RESULTS = BASE / "results" / "visual_crops"


REGIONS = [
    ("top_left_sources_and_bus", (1200, 320, 5200, 1740)),
    ("top_right_sources_and_bus", (5700, 320, 9200, 1740)),
    ("bus_tie_center", (4700, 1260, 5580, 1600)),
    ("left_train_loads", (720, 1520, 3820, 5480)),
    ("middle_cvcs_a_and_dc_a", (3380, 1520, 5300, 6620)),
    ("right_train_loads", (5120, 1520, 8400, 5480)),
    ("far_right_cvcs_b", (8200, 1520, 9300, 4800)),
    ("rps_dc_ac_bottom", (3300, 3420, 8800, 6700)),
]


def crop_and_scale(source_name: str, scale: int = 2) -> None:
    src = BASE / source_name
    image = Image.open(src).convert("RGB")
    out_dir = RESULTS / src.stem.replace(" ", "_")
    out_dir.mkdir(parents=True, exist_ok=True)

    overview = image.copy()
    draw = ImageDraw.Draw(overview)
    for label, box in REGIONS:
        draw.rectangle(box, outline=(255, 0, 0), width=10)
        draw.text((box[0] + 12, box[1] + 12), label, fill=(255, 0, 0))
        crop = image.crop(box)
        crop = crop.resize((crop.width * scale, crop.height * scale), Image.Resampling.LANCZOS)
        crop.save(out_dir / f"{label}.png")

    overview.save(out_dir / "crop_overview.png")


if __name__ == "__main__":
    crop_and_scale("raw -- schematic_image_variant_b_100.png", scale=2)
    crop_and_scale("detected_components_and_logical_overlay.png", scale=2)

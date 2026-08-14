from pathlib import Path

from PIL import Image, ImageDraw


BASE = Path(__file__).resolve().parents[1]
RESULTS = BASE / "results" / "visual_crops"


REGIONS = [
    ("top_left_sources_bus_a", (180, 220, 2600, 1250)),
    ("top_right_sources_bus_b", (2600, 220, 5100, 1250)),
    ("central_dc_ups", (2200, 520, 3400, 1850)),
    ("mccs_and_feed_buses", (520, 1260, 5060, 2280)),
    ("left_feeders_a1_a2", (260, 2020, 2660, 2920)),
    ("right_feeders_b1_b2", (2620, 2020, 5060, 2920)),
    ("bottom_interlocks_a", (1180, 2840, 2480, 3780)),
    ("bottom_interlocks_b", (3120, 2840, 4420, 3780)),
    ("bus_tie_and_ground", (2360, 430, 3180, 900)),
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
    crop_and_scale("raw -- synthetic_npp_100_component_electrical_schematic.png", scale=2)
    crop_and_scale("detected_components_and_logical_overlay.png", scale=2)

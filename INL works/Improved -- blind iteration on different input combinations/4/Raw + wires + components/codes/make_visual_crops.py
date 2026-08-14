from pathlib import Path

from PIL import Image, ImageDraw


BASE = Path(__file__).resolve().parents[1]
RESULTS = BASE / "results" / "visual_crops"


REGIONS = [
    ("top_left_sources_title", (260, 220, 1700, 760)),
    ("top_buses_full", (760, 620, 7350, 1180)),
    ("upper_left_source_and_loads", (360, 1020, 3050, 2250)),
    ("upper_mid_loads", (2850, 1030, 5450, 2250)),
    ("upper_right_loads", (5150, 1030, 7350, 2250)),
    ("left_service_transformer_path", (650, 2170, 1300, 3880)),
    ("central_dc_control_island", (4200, 2100, 7450, 3750)),
    ("control_island_train_a", (4200, 2050, 6900, 3050)),
    ("control_island_train_b", (4200, 2850, 6900, 3900)),
    ("control_island_relays_and_lc_b", (6350, 2300, 7700, 3900)),
    ("bottom_left_load_center", (920, 3740, 3700, 5200)),
    ("bottom_right_load_center", (4250, 3740, 6550, 5200)),
    ("bus_tie_and_bottom_bus", (3860, 3550, 5000, 4050)),
]


def crop_and_scale(source_name: str, scale: int = 2) -> None:
    src = BASE / source_name
    image = Image.open(src).convert("RGB")
    out_dir = RESULTS / src.stem.replace(" ", "_")
    out_dir.mkdir(parents=True, exist_ok=True)

    overview = image.copy()
    draw = ImageDraw.Draw(overview)
    for label, box in REGIONS:
        draw.rectangle(box, outline=(255, 0, 0), width=8)
        draw.text((box[0] + 12, box[1] + 12), label, fill=(255, 0, 0))
        crop = image.crop(box)
        crop = crop.resize((crop.width * scale, crop.height * scale), Image.Resampling.LANCZOS)
        crop.save(out_dir / f"{label}.png")

    overview.save(out_dir / "crop_overview.png")


if __name__ == "__main__":
    crop_and_scale("raw.png", scale=2)
    crop_and_scale("detected_components_and_logical_overlay.png", scale=2)
    crop_and_scale("wires_mask_overlay.png", scale=2)

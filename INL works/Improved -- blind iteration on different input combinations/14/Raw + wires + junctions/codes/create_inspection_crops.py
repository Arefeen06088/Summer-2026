from pathlib import Path
import importlib.util
import shutil
import sys
from PIL import Image, ImageOps


ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\14\Raw + wires + junctions")
RESULTS = ROOT / "results" / "inspection_crops"

SOURCES = {
    "raw": ROOT / "raw -- synthetic_npp_electrical_schematic_even_bus_spacing (1).png",
    "nodes": ROOT / "wire_nodes_overlay.png",
    "wires": ROOT / "wires_mask_overlay.png",
    "mask": ROOT / "wires_mask.png",
}

CROPS = {
    "upper_train_A_sources": (520, 260, 2780, 1580),
    "upper_train_B_sources": (3040, 260, 5320, 1580),
    "middle_train_A_480_feeders": (520, 1530, 2780, 2820),
    "middle_train_B_480_feeders": (3040, 1530, 5320, 2820),
    "lower_train_A_dc_ups": (520, 2730, 2840, 3900),
    "lower_train_B_dc_ups": (3040, 2730, 5320, 3900),
    "center_tie_verticals": (2600, 600, 3300, 3950),
    "bottom_terminal_blocks": (520, 3640, 2780, 4070),
    "right_notes_legend_title": (5350, 250, 6380, 3900),
    "full_active_area": (500, 250, 5330, 3920),
}


def save_crop(source_name: str, path: Path) -> None:
    with Image.open(path) as image:
        for crop_name, box in CROPS.items():
            crop = image.crop(box)
            crop.save(RESULTS / f"{source_name}_{crop_name}.png")

        overview = image.copy()
        overview.thumbnail((1800, 1200))
        overview.save(RESULTS / f"{source_name}_overview_1800.png")

        if source_name == "raw":
            gray = ImageOps.grayscale(image)
            for crop_name, box in CROPS.items():
                crop = ImageOps.autocontrast(gray.crop(box))
                crop.save(RESULTS / f"raw_gray_{crop_name}.png")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    for source_name, path in SOURCES.items():
        if path.exists():
            save_crop(source_name, path)
    sync_helpers_and_outputs()
    print(f"inspection crops written to {RESULTS}")


def run_module(path: Path) -> None:
    if not path.exists():
        return
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        return
    module = importlib.util.module_from_spec(spec)
    sys.modules[path.stem] = module
    spec.loader.exec_module(module)
    if hasattr(module, "main"):
        module.main()


def sync_helpers_and_outputs() -> None:
    codes = ROOT / "codes"
    codes.mkdir(parents=True, exist_ok=True)
    work = Path(r"C:\Asif_all_python_projects\INL\INL\doc14_work")
    for name in ["create_inspection_crops.py", "extract_and_validate_rounds.py", "estimate_token_usage.py"]:
        source = work / name
        if source.exists():
            shutil.copyfile(source, codes / name)

    run_module(work / "extract_and_validate_rounds.py")
    if (work / "subagent_round_transcript.md").exists():
        shutil.copyfile(work / "subagent_round_transcript.md", ROOT / "results" / "subagent_round_transcript.md")
    if any((ROOT / "results" / name).exists() or (work / name).exists() for name in ["diego_round1_output.txt", "jennifer_round1_review.txt"]):
        run_module(work / "estimate_token_usage.py")


if __name__ == "__main__":
    main()

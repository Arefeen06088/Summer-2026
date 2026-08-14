from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


WORK = Path(r"C:\Asif_all_python_projects\INL\INL\doc37_work")
ROOT = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\37\Raw + wires + junctions")
CODES = ROOT / "codes"
RESULTS = ROOT / "results"


def run(script: str) -> None:
    path = WORK / script
    if path.exists():
        subprocess.run([sys.executable, str(path)], check=True)


def copy_helpers() -> None:
    CODES.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)
    for name in ["create_inspection_crops.py", "extract_and_validate_rounds.py", "estimate_token_usage.py"]:
        source = WORK / name
        if source.exists():
            shutil.copyfile(source, CODES / name)
    shutil.copyfile(Path(__file__), CODES / Path(__file__).name)


def copy_round_artifacts() -> None:
    source_dir = WORK / "results"
    if not source_dir.exists():
        return
    for source in source_dir.glob("*.txt"):
        shutil.copyfile(source, RESULTS / source.name)
    for source in [source_dir / "subagent_round_transcript.md", WORK / "subagent_round_transcript.md"]:
        if source.exists():
            shutil.copyfile(source, RESULTS / source.name)


def main() -> None:
    copy_helpers()
    run("create_inspection_crops.py")
    copy_round_artifacts()
    run("extract_and_validate_rounds.py")
    run("estimate_token_usage.py")
    print(f"Doc 37 designated outputs refreshed in {RESULTS}")


if __name__ == "__main__":
    main()

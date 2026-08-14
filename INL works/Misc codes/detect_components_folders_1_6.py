"""Detect components in real diagrams for folders 1-6.

This script inspects each raw PNG diagram in
`C:\Asif_all_python_projects\INL\Labeled Real Diagram Layers\1..6`
(using only image processing, no OCR), and writes a component
overlay image into every subfolder whose name contains
"+ components".

The detection is heuristic: it uses connected components on the
binary linework, then filters by area, aspect ratio, and relative
box size to avoid most text blocks, title blocks, and pure wires.
"""

import os
from typing import List, Tuple

import cv2
import numpy as np

BASE_LAYER_DIR = r"C:\Asif_all_python_projects\INL\Labeled Real Diagram Layers"


def find_raw_image(folder_index: int) -> str:
    """Return path to the single PNG in the folder's Raw subdir."""
    folder_dir = os.path.join(BASE_LAYER_DIR, str(folder_index))
    raw_dir = os.path.join(folder_dir, "Raw")

    if not os.path.isdir(raw_dir):
        raise SystemExit(f"Raw dir not found for folder {folder_index}: {raw_dir}")

    pngs = [f for f in os.listdir(raw_dir) if f.lower().endswith(".png")]
    if not pngs:
        raise SystemExit(f"No PNG found in Raw dir for folder {folder_index}: {raw_dir}")
    if len(pngs) > 1:
        raise SystemExit(
            f"Expected exactly one PNG in Raw dir for folder {folder_index}, "
            f"found {len(pngs)}: {pngs}"
        )

    return os.path.join(raw_dir, pngs[0])


def find_component_dirs(folder_index: int) -> List[str]:
    """List subdirectories under the folder whose names contain '+ components'."""
    folder_dir = os.path.join(BASE_LAYER_DIR, str(folder_index))
    if not os.path.isdir(folder_dir):
        raise SystemExit(f"Folder dir not found: {folder_dir}")

    comp_dirs: List[str] = []
    for name in os.listdir(folder_dir):
        full = os.path.join(folder_dir, name)
        if os.path.isdir(full) and "+ components" in name.lower():
            comp_dirs.append(full)

    return comp_dirs


def classify_component(
    area: int,
    width: int,
    height: int,
    image_area: int,
    image_h: int,
    image_w: int,
) -> str:
    """Heuristically classify a connected component as a component or ignore.

    Rules are tuned to reduce false positives from text and pure wires:
    - Ignore very small areas (likely individual characters or tiny marks).
    - Ignore huge areas and boxes that span a large fraction of the page
      (title blocks, big frames).
    - Ignore very skinny or extremely elongated boxes (wires, text lines).
    - Keep moderately sized, roughly rectangular blobs.
    """

    # Minimum size in pixels: tuned based on the real diagrams.
    min_area = 1000
    if area < min_area:
        return ""

    # Do not treat very large page-spanning regions as components.
    max_area = int(image_area * 0.015)  # about 1.5% of the page
    if area > max_area:
        return ""

    # Require a reasonable box size so we skip tiny specks.
    if width < 20 or height < 20:
        return ""

    aspect = width / float(height)

    # Skip strongly elongated boxes (likely wires or text lines).
    if aspect > 4.0 or aspect < 0.25:
        return ""

    # Skip boxes that are a large fraction of the page dimensions
    # (headers, big notes, title blocks).
    if width > image_w * 0.4 or height > image_h * 0.4:
        return ""

    return "component"


def detect_components(image_path: str) -> Tuple[cv2.Mat, List[Tuple[int, int, int, int, str]]]:
    """Detect components and return overlay image and bounding boxes.

    Returns (overlay_image, boxes) where boxes is a list of
    (x, y, w, h, label) with label currently always 'component'.
    """

    img = cv2.imread(image_path)
    if img is None:
        raise SystemExit(f"Could not read image: {image_path}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Emphasize dark linework and symbols by inverting a binary Otsu
    # threshold. Text is also dark, but many small text components will
    # be filtered out by area/shape rules.
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    # Mild morphological cleanup to join nearby strokes without
    # over-merging everything.
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=1)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)

    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(binary, connectivity=8)

    image_h, image_w = gray.shape
    image_area = image_h * image_w

    boxes: List[Tuple[int, int, int, int, str]] = []
    for label in range(1, num_labels):  # skip background
        x, y, w, h, area = stats[label]
        cls = classify_component(area, w, h, image_area, image_h, image_w)
        if not cls:
            continue
        boxes.append((x, y, w, h, cls))

    overlay = img.copy()
    orange = (0, 140, 255)  # BGR

    for x, y, w, h, cls in boxes:
        cv2.rectangle(overlay, (x, y), (x + w, y + h), orange, 2)

    return overlay, boxes


def write_overlays_for_folder(folder_index: int) -> None:
    """Generate component overlay for one folder and write into +components dirs."""
    try:
        image_path = find_raw_image(folder_index)
    except SystemExit as exc:
        print(f"[ERROR] Folder {folder_index}: {exc}")
        return

    comp_dirs = find_component_dirs(folder_index)
    if not comp_dirs:
        print(f"[SKIP] No '+ components' dirs for folder {folder_index}")
        return

    print(f"[INFO] Detecting components for folder {folder_index} from {image_path}")
    overlay, boxes = detect_components(image_path)
    print(f"[INFO] Folder {folder_index}: detected {len(boxes)} candidate components")

    filename = os.path.basename(image_path)
    base_no_ext, _ = os.path.splitext(filename)
    out_name = f"{base_no_ext}_components_overlay.png"

    for out_dir in comp_dirs:
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, out_name)
        cv2.imwrite(out_path, overlay)
        print(f"[INFO] Wrote overlay to {out_path}")


def main() -> None:
    # Process folders 1 through 6 under BASE_LAYER_DIR.
    for folder_index in range(1, 7):
        folder_dir = os.path.join(BASE_LAYER_DIR, str(folder_index))
        if not os.path.isdir(folder_dir):
            print(f"[SKIP] Folder dir does not exist: {folder_dir}")
            continue
        write_overlays_for_folder(folder_index)


if __name__ == "__main__":
    main()

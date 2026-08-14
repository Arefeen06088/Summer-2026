import os
from typing import List, Tuple

import cv2
import numpy as np

BASE_LAYER_DIR = r"C:\Asif_all_python_projects\INL\Labeled Real Diagram Layers"


def find_raw_image(layer_index: int) -> str:
    """Return path to the single PNG in the layer's Raw folder."""
    layer_dir = os.path.join(BASE_LAYER_DIR, str(layer_index))
    raw_dir = os.path.join(layer_dir, "Raw")

    if not os.path.isdir(raw_dir):
        raise SystemExit(f"Raw dir not found for layer {layer_index}: {raw_dir}")

    pngs = [f for f in os.listdir(raw_dir) if f.lower().endswith(".png")]
    if not pngs:
        raise SystemExit(f"No PNG found in Raw dir for layer {layer_index}: {raw_dir}")
    if len(pngs) > 1:
        raise SystemExit(
            f"Expected exactly one PNG in Raw dir for layer {layer_index}, "
            f"found {len(pngs)}: {pngs}"
        )

    return os.path.join(raw_dir, pngs[0])


def find_component_dirs(layer_index: int) -> List[str]:
    """List subdirectories under the layer whose names contain '+ components'."""
    layer_dir = os.path.join(BASE_LAYER_DIR, str(layer_index))
    if not os.path.isdir(layer_dir):
        raise SystemExit(f"Layer dir not found: {layer_dir}")

    comp_dirs: List[str] = []
    for name in os.listdir(layer_dir):
        full = os.path.join(layer_dir, name)
        if os.path.isdir(full) and "+ components" in name.lower():
            comp_dirs.append(full)

    return comp_dirs


def classify_component(area: int, width: int, height: int, image_area: int) -> str:
    """Classify connected component as 'component', 'busbar', or '' (ignore)."""
    if area < image_area * 0.00002:
        return ""
    if area > image_area * 0.05:
        return ""
    if width < 3 or height < 3:
        return ""

    aspect = width / float(height)
    if aspect >= 10.0 or aspect <= 0.1:
        return "busbar"
    return "component"


def detect_components(image_path: str) -> Tuple[np.ndarray, List[Tuple[int, int, int, int, str]]]:
    """Detect components and bus bars and return overlay image and boxes."""
    img = cv2.imread(image_path)
    if img is None:
        raise SystemExit(f"Could not read image: {image_path}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=1)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)

    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(binary, connectivity=8)
    image_area = img.shape[0] * img.shape[1]

    boxes: List[Tuple[int, int, int, int, str]] = []
    for label in range(1, num_labels):
        x, y, w, h, area = stats[label]
        cls = classify_component(area, w, h, image_area)
        if not cls:
            continue
        boxes.append((x, y, w, h, cls))

    overlay = img.copy()
    orange = (0, 140, 255)
    green = (0, 180, 0)

    for x, y, w, h, cls in boxes:
        if cls == "component":
            color = orange
        else:
            color = green
        cv2.rectangle(overlay, (x, y), (x + w, y + h), color, 2)

    return overlay, boxes


def write_overlays_for_layer(layer_index: int) -> None:
    image_path = find_raw_image(layer_index)
    comp_dirs = find_component_dirs(layer_index)
    if not comp_dirs:
        print(f"[SKIP] No '+ components' dirs for layer {layer_index}")
        return

    print(f"[INFO] Detecting components for layer {layer_index} from {image_path}")
    overlay, boxes = detect_components(image_path)
    print(f"[INFO] Layer {layer_index}: detected {len(boxes)} candidate components/bus bars")

    filename = os.path.basename(image_path)
    base_no_ext, _ = os.path.splitext(filename)
    out_name = f"{base_no_ext}_components_overlay.png"

    for out_dir in comp_dirs:
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, out_name)
        cv2.imwrite(out_path, overlay)
        print(f"[INFO] Wrote overlay to {out_path}")


def main() -> None:
    write_overlays_for_layer(1)


if __name__ == "__main__":
    main()

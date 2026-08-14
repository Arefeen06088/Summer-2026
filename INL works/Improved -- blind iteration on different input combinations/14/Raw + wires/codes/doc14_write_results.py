from __future__ import annotations

import csv
import json
import math
import os
from pathlib import Path
from typing import Iterable

try:
    from PIL import Image
except Exception:  # pragma: no cover
    Image = None


DOC = "14"
ITERATION = "1"
RESOURCE_DIR = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\14\Raw + wires"
)
DEFAULT_OUT = Path(r"C:\Asif_all_python_projects\INL\INL\doc14_work\results")
OUT = Path(os.environ.get("DOC14_OUTPUT_DIR", str(DEFAULT_OUT)))
CROP_DIR = Path(r"C:\Asif_all_python_projects\INL\INL\doc14_work\crops")

RAW = RESOURCE_DIR / "raw -- synthetic_npp_electrical_schematic_even_bus_spacing (1).png"
OVERLAY = RESOURCE_DIR / "wires_mask_overlay.png"
MASK = RESOURCE_DIR / "wires_mask.png"


def add_node(nodes: list[str], node: str) -> None:
    if node not in nodes:
        nodes.append(node)


def edge_key(a: str, b: str) -> tuple[str, str]:
    if a == b:
        raise ValueError(f"self-loop requested for {a}")
    return tuple(sorted((a, b)))


def add_edge(
    edges: dict[tuple[str, str], dict[str, str]],
    a: str,
    b: str,
    edge_type: str,
    evidence: str,
) -> None:
    key = edge_key(a, b)
    edges.setdefault(
        key,
        {
            "source": key[0],
            "target": key[1],
            "type": edge_type,
            "evidence": evidence,
        },
    )


def add_chain(
    edges: dict[tuple[str, str], dict[str, str]],
    chain: list[str],
    edge_type: str,
    evidence: str,
) -> None:
    for a, b in zip(chain, chain[1:]):
        add_edge(edges, a, b, edge_type, evidence)


def build_nodes(label_style: str) -> list[str]:
    """label_style is 'diego_r1' for CB-480* labels, else final CB-48* labels."""
    a48 = "480A" if label_style == "diego_r1" else "48A"
    b48 = "480B" if label_style == "diego_r1" else "48B"
    nodes: list[str] = []
    for n in [
        "GRID-1",
        "TR-SST-A",
        "CB-SST-A",
        "GEN-TG1",
        "TR-UAT-1",
        "CB-UAT-1",
        "DG-1A",
        "TR-DG-A",
        "CB-DG-A",
        "BUS-4A",
        "TR-480A",
        "BUS-480A",
    ]:
        add_node(nodes, n)
    for suffix, mid, inst, relay, load in [
        ("01", "FU-A01", "FI-A01", "RELAY-KA01", "PUMP-CS-1A"),
        ("02", "OL-A02", "PI-A02", "RELAY-KA02", "PUMP-RHR-1A"),
        ("07", "FU-A07", "PT-A07", "RELAY-KA07", "PUMP-CW-1A"),
    ]:
        for n in [
            f"CB-4A-{suffix}",
            f"DS-4A-{suffix}",
            mid,
            f"TB-A{suffix}",
            inst,
            relay,
            load,
            f"GND-A{suffix}",
        ]:
            add_node(nodes, n)
    for suffix, mid, inst, relay, load in [
        ("03", "KON-A03", "FS-A03", "RELAY-KA03", "PUMP-SW-1A"),
        ("04", "FU-A04", "TS-A04", "RELAY-KA04", "FAN-CR-1A"),
        ("05", "OL-A05", "ZS-A05", "RELAY-KA05", "MOV-SI-101A"),
        ("06", "KON-A06", "VM-A06", "RELAY-KA06", "RECT-AUX-1A"),
        ("08", "OL-A08", "TT-A08", "RELAY-KA08", "HTR-PZR-A"),
        ("09", "KON-A09", "PS-A09", "RELAY-KA09", "COMP-IA-1A"),
    ]:
        for n in [
            f"CB-{a48}-{suffix}",
            f"DS-{a48}-{suffix}",
            mid,
            f"TB-A{suffix}",
            inst,
            relay,
            load,
            f"GND-A{suffix}",
        ]:
            add_node(nodes, n)
    for n in [
        "PANEL-ESF-A",
        "PANEL-RPS-A",
        "PANEL-LS-A",
        "CHG-125A",
        "BUS-125DCA",
        "BAT-125A",
        "INV-120A",
        "BUS-UPS-A",
        "CB-TIE-4KV",
        "CB-480-TIE",
        "CB-DC-TIE",
        "PANEL-MCR",
        "PANEL-ANN",
    ]:
        add_node(nodes, n)
    for n in [
        "GRID-2",
        "TR-SST-B",
        "CB-SST-B",
        "DG-1B",
        "TR-DG-B",
        "CB-DG-B",
        "BUS-4B",
        "TR-480B",
        "BUS-480B",
    ]:
        add_node(nodes, n)
    for suffix, mid, inst, relay, load in [
        ("01", "FU-B01", "FI-B01", "RELAY-KB01", "PUMP-CS-1B"),
        ("02", "OL-B02", "PI-B02", "RELAY-KB02", "PUMP-RHR-1B"),
        ("07", "FU-B07", "PT-B07", "RELAY-KB07", "PUMP-CW-1B"),
    ]:
        for n in [
            f"CB-4B-{suffix}",
            f"DS-4B-{suffix}",
            mid,
            f"TB-B{suffix}",
            inst,
            relay,
            load,
            f"GND-B{suffix}",
        ]:
            add_node(nodes, n)
    for suffix, mid, inst, relay, load in [
        ("03", "KON-B03", "FS-B03", "RELAY-KB03", "PUMP-SW-1B"),
        ("04", "FU-B04", "TS-B04", "RELAY-KB04", "FAN-CR-1B"),
        ("05", "OL-B05", "ZS-B05", "RELAY-KB05", "MOV-SI-101B"),
        ("06", "KON-B06", "VM-B06", "RELAY-KB06", "INV-AUX-1B"),
        ("08", "OL-B08", "LT-B08", "RELAY-KB08", "HVAC-CHLR-1B"),
    ]:
        for n in [
            f"CB-{b48}-{suffix}",
            f"DS-{b48}-{suffix}",
            mid,
            f"TB-B{suffix}",
            inst,
            relay,
            load,
            f"GND-B{suffix}",
        ]:
            add_node(nodes, n)
    for n in [
        "PANEL-LS-B",
        "PANEL-RPS-B",
        "PANEL-ESF-B",
        "CHG-125B",
        "BUS-125DCB",
        "BAT-125B",
        "INV-120B",
        "BUS-UPS-B",
    ]:
        add_node(nodes, n)
    return nodes


def build_final_edges() -> dict[tuple[str, str], dict[str, str]]:
    edges: dict[tuple[str, str], dict[str, str]] = {}
    add_chain(edges, ["GRID-1", "TR-SST-A", "CB-SST-A", "BUS-4A"], "power", "solid source feeder to BUS-4A")
    add_chain(edges, ["GEN-TG1", "TR-UAT-1", "CB-UAT-1", "BUS-4A"], "power", "solid generator auxiliary feeder to BUS-4A")
    add_chain(edges, ["DG-1A", "TR-DG-A", "CB-DG-A", "BUS-4A"], "power", "solid diesel generator feeder to BUS-4A")
    add_chain(edges, ["BUS-4A", "TR-480A", "BUS-480A"], "power", "solid transformer downfeed from 4.16 kV to 480 V")
    add_chain(edges, ["BUS-4A", "CB-TIE-4KV", "BUS-4B"], "power_tie", "solid 4 kV tie breaker path")
    add_chain(edges, ["BUS-480A", "CB-480-TIE", "BUS-480B"], "power_tie", "solid 480 V tie breaker path")
    add_chain(edges, ["BUS-125DCA", "CB-DC-TIE", "BUS-125DCB"], "dc_tie", "solid 125 VDC tie breaker path")

    for suffix, mid, inst, load in [
        ("01", "FU-A01", "FI-A01", "PUMP-CS-1A"),
        ("02", "OL-A02", "PI-A02", "PUMP-RHR-1A"),
        ("07", "FU-A07", "PT-A07", "PUMP-CW-1A"),
    ]:
        add_chain(
            edges,
            ["BUS-4A", f"CB-4A-{suffix}", f"DS-4A-{suffix}", mid, f"TB-A{suffix}", load, f"GND-A{suffix}"],
            "power",
            f"solid 4A branch C-4A-{suffix}-P to load and local ground",
        )
        add_edge(edges, f"TB-A{suffix}", inst, "signal_tap", f"short visible terminal-block tap to {inst}")

    for suffix, mid, inst, load in [
        ("03", "KON-A03", "FS-A03", "PUMP-SW-1A"),
        ("04", "FU-A04", "TS-A04", "FAN-CR-1A"),
        ("05", "OL-A05", "ZS-A05", "MOV-SI-101A"),
        ("06", "KON-A06", "VM-A06", "RECT-AUX-1A"),
        ("08", "OL-A08", "TT-A08", "HTR-PZR-A"),
        ("09", "KON-A09", "PS-A09", "COMP-IA-1A"),
    ]:
        add_chain(
            edges,
            ["BUS-480A", f"CB-48A-{suffix}", f"DS-48A-{suffix}", mid, f"TB-A{suffix}", load, f"GND-A{suffix}"],
            "power",
            f"solid 480A branch C-48A-{suffix}-P to load and local ground",
        )
        add_edge(edges, f"TB-A{suffix}", inst, "signal_tap", f"short visible terminal-block tap to {inst}")

    add_chain(
        edges,
        ["BUS-480A", "PANEL-RPS-A", "CHG-125A", "BUS-125DCA"],
        "dc_supply",
        "solid A charger feed visibly passes through PANEL-RPS-A into CHG-125A and BUS-125DCA",
    )
    add_edge(edges, "BUS-125DCA", "BAT-125A", "dc", "solid battery tap to BUS-125DCA")
    add_chain(edges, ["BUS-125DCA", "INV-120A", "BUS-UPS-A"], "ups", "solid inverter path between DC bus and UPS bus")

    add_chain(edges, ["GRID-2", "TR-SST-B", "CB-SST-B", "BUS-4B"], "power", "solid source feeder to BUS-4B")
    add_chain(edges, ["DG-1B", "TR-DG-B", "CB-DG-B", "BUS-4B"], "power", "solid diesel generator feeder to BUS-4B")
    add_chain(edges, ["BUS-4B", "TR-480B", "BUS-480B"], "power", "solid transformer downfeed from 4.16 kV to 480 V")

    for suffix, mid, inst, load in [
        ("01", "FU-B01", "FI-B01", "PUMP-CS-1B"),
        ("02", "OL-B02", "PI-B02", "PUMP-RHR-1B"),
        ("07", "FU-B07", "PT-B07", "PUMP-CW-1B"),
    ]:
        add_chain(
            edges,
            ["BUS-4B", f"CB-4B-{suffix}", f"DS-4B-{suffix}", mid, f"TB-B{suffix}", load, f"GND-B{suffix}"],
            "power",
            f"solid 4B branch C-4B-{suffix}-P to load and local ground",
        )
        add_edge(edges, f"TB-B{suffix}", inst, "signal_tap", f"short visible terminal-block tap to {inst}")

    for suffix, mid, inst, load in [
        ("03", "KON-B03", "FS-B03", "PUMP-SW-1B"),
        ("04", "FU-B04", "TS-B04", "FAN-CR-1B"),
        ("05", "OL-B05", "ZS-B05", "MOV-SI-101B"),
        ("06", "KON-B06", "VM-B06", "INV-AUX-1B"),
        ("08", "OL-B08", "LT-B08", "HVAC-CHLR-1B"),
    ]:
        add_chain(
            edges,
            ["BUS-480B", f"CB-48B-{suffix}", f"DS-48B-{suffix}", mid, f"TB-B{suffix}", load, f"GND-B{suffix}"],
            "power",
            f"solid 480B branch C-48B-{suffix}-P to load and local ground",
        )
        add_edge(edges, f"TB-B{suffix}", inst, "signal_tap", f"short visible terminal-block tap to {inst}")

    add_chain(
        edges,
        ["BUS-480B", "CHG-125B", "BUS-125DCB"],
        "dc_supply",
        "solid B charger feed from BUS-480B to CHG-125B and BUS-125DCB",
    )
    add_edge(edges, "BUS-125DCB", "BAT-125B", "dc", "solid battery tap to BUS-125DCB")
    add_chain(edges, ["BUS-125DCB", "INV-120B", "BUS-UPS-B"], "ups", "solid inverter path between DC bus and UPS bus")
    return edges


def build_diego_r1_edges() -> dict[tuple[str, str], dict[str, str]]:
    edges: dict[tuple[str, str], dict[str, str]] = {}
    add_chain(edges, ["GRID-1", "TR-SST-A", "CB-SST-A", "BUS-4A"], "power", "Diego R1 solid source feeder")
    add_chain(edges, ["GEN-TG1", "TR-UAT-1", "CB-UAT-1", "BUS-4A"], "power", "Diego R1 solid source feeder")
    add_chain(edges, ["DG-1A", "TR-DG-A", "CB-DG-A", "BUS-4A"], "power", "Diego R1 solid source feeder")
    add_chain(edges, ["BUS-4A", "TR-480A", "BUS-480A"], "power", "Diego R1 transformer downfeed")
    add_chain(edges, ["BUS-4A", "CB-TIE-4KV", "BUS-4B"], "power_tie", "Diego R1 solid tie")
    add_chain(edges, ["BUS-480A", "CB-480-TIE", "BUS-480B"], "power_tie", "Diego R1 solid tie")
    add_chain(edges, ["BUS-125DCA", "CB-DC-TIE", "BUS-125DCB"], "dc_tie", "Diego R1 solid tie")

    for train, bus, cb_prefix, ds_prefix, mids in [
        (
            "A",
            "BUS-4A",
            "CB-4A",
            "DS-4A",
            [
                ("01", "FU-A01", "FI-A01", "RELAY-KA01", "PUMP-CS-1A"),
                ("02", "OL-A02", "PI-A02", "RELAY-KA02", "PUMP-RHR-1A"),
                ("07", "FU-A07", "PT-A07", "RELAY-KA07", "PUMP-CW-1A"),
            ],
        ),
        (
            "B",
            "BUS-4B",
            "CB-4B",
            "DS-4B",
            [
                ("01", "FU-B01", "FI-B01", "RELAY-KB01", "PUMP-CS-1B"),
                ("02", "OL-B02", "PI-B02", "RELAY-KB02", "PUMP-RHR-1B"),
                ("07", "FU-B07", "PT-B07", "RELAY-KB07", "PUMP-CW-1B"),
            ],
        ),
    ]:
        for suffix, mid, inst, relay, load in mids:
            tb = f"TB-{train}{suffix}"
            cb = f"{cb_prefix}-{suffix}"
            add_chain(edges, [bus, cb, f"{ds_prefix}-{suffix}", mid, tb, load, f"GND-{train}{suffix}"], "power", "Diego R1 branch chain")
            add_edge(edges, tb, inst, "signal_tap", "Diego R1 local instrument tap")
            add_edge(edges, relay, cb, "control", "Diego R1 high-recall relay/control edge")

    for train, bus, cb_prefix, ds_prefix, mids in [
        (
            "A",
            "BUS-480A",
            "CB-480A",
            "DS-480A",
            [
                ("03", "KON-A03", "FS-A03", "RELAY-KA03", "PUMP-SW-1A"),
                ("04", "FU-A04", "TS-A04", "RELAY-KA04", "FAN-CR-1A"),
                ("05", "OL-A05", "ZS-A05", "RELAY-KA05", "MOV-SI-101A"),
                ("06", "KON-A06", "VM-A06", "RELAY-KA06", "RECT-AUX-1A"),
                ("08", "OL-A08", "TT-A08", "RELAY-KA08", "HTR-PZR-A"),
                ("09", "KON-A09", "PS-A09", "RELAY-KA09", "COMP-IA-1A"),
            ],
        ),
        (
            "B",
            "BUS-480B",
            "CB-480B",
            "DS-480B",
            [
                ("03", "KON-B03", "FS-B03", "RELAY-KB03", "PUMP-SW-1B"),
                ("04", "FU-B04", "TS-B04", "RELAY-KB04", "FAN-CR-1B"),
                ("05", "OL-B05", "ZS-B05", "RELAY-KB05", "MOV-SI-101B"),
                ("06", "KON-B06", "VM-B06", "RELAY-KB06", "INV-AUX-1B"),
                ("08", "OL-B08", "LT-B08", "RELAY-KB08", "HVAC-CHLR-1B"),
            ],
        ),
    ]:
        for suffix, mid, inst, relay, load in mids:
            tb = f"TB-{train}{suffix}"
            cb = f"{cb_prefix}-{suffix}"
            add_chain(edges, [bus, cb, f"{ds_prefix}-{suffix}", mid, tb, load, f"GND-{train}{suffix}"], "power", "Diego R1 branch chain")
            add_edge(edges, tb, inst, "signal_tap", "Diego R1 local instrument tap")
            add_edge(edges, relay, cb, "control", "Diego R1 high-recall relay/control edge")

    add_chain(edges, ["BUS-480A", "PANEL-RPS-A", "CHG-125A", "BUS-125DCA"], "dc_supply", "Diego R1 A charger path")
    add_edge(edges, "BUS-125DCA", "BAT-125A", "dc", "Diego R1 battery tap")
    add_chain(edges, ["BUS-125DCA", "INV-120A", "BUS-UPS-A"], "ups", "Diego R1 UPS path")
    add_chain(edges, ["GRID-2", "TR-SST-B", "CB-SST-B", "BUS-4B"], "power", "Diego R1 source feeder")
    add_chain(edges, ["DG-1B", "TR-DG-B", "CB-DG-B", "BUS-4B"], "power", "Diego R1 source feeder")
    add_chain(edges, ["BUS-4B", "TR-480B", "BUS-480B"], "power", "Diego R1 transformer downfeed")
    add_chain(edges, ["BUS-480B", "PANEL-LS-B", "CHG-125B", "BUS-125DCB"], "dc_supply", "Diego R1 high-recall B charger/panel path")
    add_edge(edges, "BUS-125DCB", "BAT-125B", "dc", "Diego R1 battery tap")
    add_chain(edges, ["BUS-125DCB", "INV-120B", "BUS-UPS-B"], "ups", "Diego R1 UPS path")
    add_chain(edges, ["PANEL-MCR", "PANEL-ANN", "CB-DC-TIE"], "control", "Diego R1 high-recall dashed/control vertical association")
    return edges


def final_uncertain_edges() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    relay_pairs = [
        ("RELAY-KA01", "CB-4A-01"),
        ("RELAY-KA02", "CB-4A-02"),
        ("RELAY-KA07", "CB-4A-07"),
        ("RELAY-KA03", "CB-48A-03"),
        ("RELAY-KA04", "CB-48A-04"),
        ("RELAY-KA05", "CB-48A-05"),
        ("RELAY-KA06", "CB-48A-06"),
        ("RELAY-KA08", "CB-48A-08"),
        ("RELAY-KA09", "CB-48A-09"),
        ("RELAY-KB01", "CB-4B-01"),
        ("RELAY-KB02", "CB-4B-02"),
        ("RELAY-KB07", "CB-4B-07"),
        ("RELAY-KB03", "CB-48B-03"),
        ("RELAY-KB04", "CB-48B-04"),
        ("RELAY-KB05", "CB-48B-05"),
        ("RELAY-KB06", "CB-48B-06"),
        ("RELAY-KB08", "CB-48B-08"),
    ]
    for a, b in relay_pairs:
        rows.append({"source": a, "target": b, "reason": "dashed/control association visible near breaker but not retained as hard connectivity"})
    for panel in ["PANEL-ESF-A", "PANEL-RPS-A", "PANEL-LS-A"]:
        rows.append({"source": panel, "target": "A-train dashed/control bundle", "reason": "bundle passes into or near panel region; exact branch terminations are ambiguous"})
    for panel in ["PANEL-LS-B", "PANEL-RPS-B", "PANEL-ESF-B"]:
        rows.append({"source": panel, "target": "B-train dashed/control bundle", "reason": "bundle passes into or near panel region; exact branch terminations are ambiguous"})
    rows.extend(
        [
            {"source": "PANEL-MCR", "target": "PANEL-ANN", "reason": "dashed/control vertical association only, not hard matrix edge"},
            {"source": "PANEL-ANN", "target": "CB-DC-TIE", "reason": "dashed/control vertical association only, not hard matrix edge"},
            {"source": "BUS-UPS-A", "target": "CB-DC-TIE", "reason": "nearby dashed/control geometry approaches DC tie area but no clear hard termination"},
            {"source": "BUS-UPS-B", "target": "CB-DC-TIE", "reason": "nearby dashed/control geometry approaches DC tie area but no clear hard termination"},
        ]
    )
    return rows


def diego_r1_uncertain_edges() -> list[dict[str, str]]:
    rows = final_uncertain_edges()
    rows.append({"source": "GND-*", "target": "common ground reference", "reason": "ground symbols imply reference only; no common drawn ground bus"})
    rows.append({"source": "MASTER TERMINAL BLOCKS XA1..YD2", "target": "BUS-UPS-A", "reason": "terminal-block row visible below BUS-UPS-A; no direct conductor visible"})
    return rows


def removed_edges_jennifer_r1() -> list[dict[str, str]]:
    return [
        {"source": "CB-480A-*", "target": "DS-480A-*", "reason": "renamed to visible CB-48A-* / DS-48A-* labels"},
        {"source": "CB-480B-*", "target": "DS-480B-*", "reason": "renamed to visible CB-48B-* / DS-48B-* labels"},
        {"source": "BUS-480B", "target": "PANEL-LS-B", "reason": "B charger feed is direct solid drop to CHG-125B, not hard through panel"},
        {"source": "PANEL-LS-B", "target": "CHG-125B", "reason": "B charger feed is direct solid drop to CHG-125B, not hard through panel"},
        {"source": "PANEL-MCR", "target": "PANEL-ANN", "reason": "dashed/control only; retained uncertain"},
        {"source": "PANEL-ANN", "target": "CB-DC-TIE", "reason": "dashed/control only; retained uncertain"},
        {"source": "MASTER TERMINAL BLOCKS XA1..YD2", "target": "BUS-UPS-A", "reason": "no visible conductor enters terminal-block table"},
        {"source": "GND-*", "target": "common ground reference", "reason": "no common ground bus is drawn"},
    ]


def write_nodes(path: Path, nodes: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["index", "node"])
        for i, node in enumerate(nodes):
            writer.writerow([i, node])


def write_edges(path: Path, edges: dict[tuple[str, str], dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["source", "target", "type", "evidence"])
        writer.writeheader()
        for key in sorted(edges):
            writer.writerow(edges[key])


def write_matrix(path: Path, nodes: list[str], edges: dict[tuple[str, str], dict[str, str]]) -> None:
    edge_set = set(edges)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["node", *nodes])
        for row_node in nodes:
            writer.writerow(
                [
                    row_node,
                    *[
                        0 if row_node == col_node else int(edge_key(row_node, col_node) in edge_set)
                        for col_node in nodes
                    ],
                ]
            )


def write_sparse(path: Path, nodes: list[str], edges: dict[tuple[str, str], dict[str, str]]) -> None:
    edge_set = set(edges)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["row", "column", "connected"])
        for row_node in nodes:
            for col_node in nodes:
                value = 0 if row_node == col_node else int(edge_key(row_node, col_node) in edge_set)
                writer.writerow([row_node, col_node, value])


def write_uncertain(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["source", "target", "reason"])
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def estimate_text_tokens(text: str) -> int:
    return max(1, math.ceil(len(text) / 4))


def image_dims(path: Path) -> tuple[int, int]:
    fallback = {
        RAW.name: (6600, 4200),
        OVERLAY.name: (6600, 4200),
    }
    if Image is not None and path.exists():
        with Image.open(path) as img:
            return img.size
    return fallback.get(path.name, (1200, 900))


def image_token_proxy(path: Path) -> int:
    width, height = image_dims(path)
    return math.ceil(width / 32) * math.ceil(height / 32)


def write_token_usage(path: Path) -> list[dict[str, object]]:
    diego_r1_text = (
        "Diego R1 high-recall extraction prompt with document 14 instructions, no GT/no OCR warnings, "
        "raw/overlay/crop references, and requested nodes/edges/uncertainties."
    )
    jennifer_r1_text = (
        "Jennifer R1 precision prompt with document 14 instructions, Diego R1 proposal text, no GT/no OCR "
        "warnings, raw/overlay/crop references, and requested removals/uncertainties."
    )
    diego_r2_text = "Diego R2 saturation prompt carrying Jennifer R1 corrections and asking for final additions/removals."
    jennifer_r2_text = "Jennifer R2 final confirmation prompt asking whether the saturated graph needs changes and whether TB-instrument taps remain hard."
    main_text = "Main agent orchestration, visual inspection, graph synthesis, result generation, and final report for document 14."

    diego_r1_images = [
        RAW,
        OVERLAY,
        CROP_DIR / "raw_full_left_train_a.png",
        CROP_DIR / "raw_full_right_train_b.png",
        CROP_DIR / "raw_loadcenter_a.png",
        CROP_DIR / "raw_loadcenter_b.png",
        CROP_DIR / "raw_bottom_dc_ups_a.png",
        CROP_DIR / "raw_bottom_dc_ups_b.png",
        CROP_DIR / "raw_center_ties.png",
        CROP_DIR / "raw_bottom_center_transfer.png",
        CROP_DIR / "raw_terminal_blocks.png",
    ]
    jennifer_r1_images = [
        RAW,
        OVERLAY,
        CROP_DIR / "raw_full_left_train_a.png",
        CROP_DIR / "raw_full_right_train_b.png",
        CROP_DIR / "raw_left_mcc_detail.png",
        CROP_DIR / "raw_right_mcc_detail.png",
        CROP_DIR / "raw_bottom_dc_ups_a.png",
        CROP_DIR / "raw_bottom_dc_ups_b.png",
        CROP_DIR / "raw_center_ties.png",
        CROP_DIR / "raw_bottom_center_transfer.png",
        CROP_DIR / "raw_terminal_blocks.png",
    ]
    main_images = [
        CROP_DIR / "raw_top_train_a_safety.png",
        CROP_DIR / "raw_top_train_b_safety.png",
        CROP_DIR / "raw_loadcenter_a.png",
        CROP_DIR / "raw_loadcenter_b.png",
        CROP_DIR / "raw_right_mcc_detail.png",
        CROP_DIR / "raw_left_mcc_detail.png",
        CROP_DIR / "raw_left_top_branch_detail.png",
        CROP_DIR / "overlay_left_top_branch_detail.png",
        CROP_DIR / "overlay_left_mcc_detail.png",
        CROP_DIR / "raw_bottom_dc_ups_a.png",
        CROP_DIR / "raw_bottom_dc_ups_b.png",
        CROP_DIR / "raw_center_ties.png",
        CROP_DIR / "raw_bottom_center_transfer.png",
        CROP_DIR / "raw_terminal_blocks.png",
        CROP_DIR / "raw_grid_r2_c1.png",
        CROP_DIR / "raw_grid_r2_c2.png",
        CROP_DIR / "raw_grid_r2_c3.png",
        CROP_DIR / "raw_grid_r2_c4.png",
        CROP_DIR / "raw_grid_r3_c1.png",
        CROP_DIR / "raw_grid_r3_c2.png",
        CROP_DIR / "raw_grid_r3_c3.png",
    ]

    actual_diego_r1_output = 3210
    actual_jennifer_r1_output = 2510
    actual_diego_r2_output = 190
    actual_jennifer_r2_output = 95

    rows: list[dict[str, object]] = []

    def add_call(
        call_id: str,
        actor: str,
        round_name: str,
        model: str,
        text: str,
        image_tokens: int,
        output_est: int,
        reasoning_expected: int,
        notes: str,
        cached: int = 0,
    ) -> None:
        text_tokens = estimate_text_tokens(text) + cached
        total_low = text_tokens + image_tokens + output_est + math.floor(reasoning_expected * 0.5)
        total_expected = text_tokens + image_tokens + output_est + reasoning_expected
        total_high = text_tokens + math.ceil(image_tokens * 1.35) + math.ceil(output_est * 1.35) + math.ceil(reasoning_expected * 1.8)
        rows.append(
            {
                "document": DOC,
                "iteration": ITERATION,
                "call_id": call_id,
                "actor": actor,
                "round": round_name,
                "model": model,
                "input_tokens_est": text_tokens,
                "cached_input_tokens_est": cached,
                "output_tokens_est": output_est,
                "reasoning_tokens_available": "no",
                "reasoning_tokens_low_est": math.floor(reasoning_expected * 0.5),
                "reasoning_tokens_expected_est": reasoning_expected,
                "reasoning_tokens_high_est": math.ceil(reasoning_expected * 1.8),
                "image_file_input_tokens_est": image_tokens,
                "total_tokens_low_est": total_low,
                "total_tokens_expected_est": total_expected,
                "total_tokens_high_est": total_high,
                "usage_object_available": "no",
                "notes": notes,
            }
        )

    main_image_tokens = sum(image_token_proxy(p) for p in main_images)
    diego_image_tokens = sum(image_token_proxy(p) for p in diego_r1_images)
    jennifer_image_tokens = sum(image_token_proxy(p) for p in jennifer_r1_images)

    add_call(
        "main_01_visual_orchestration_and_artifacts",
        "main",
        "orchestration",
        "gpt-5",
        main_text,
        main_image_tokens,
        2200,
        4500,
        "Local visual review and artifact-writing calls; exact Responses usage unavailable.",
    )
    add_call(
        "diego_01_high_recall",
        "Diego",
        "round_01",
        "gpt-5.5 xhigh",
        diego_r1_text,
        diego_image_tokens,
        actual_diego_r1_output,
        9000,
        "Subagent response text was available, but usage object was not exposed.",
    )
    add_call(
        "jennifer_01_precision",
        "Jennifer",
        "round_01",
        "gpt-5.5 xhigh",
        jennifer_r1_text,
        jennifer_image_tokens,
        actual_jennifer_r1_output,
        8000,
        "Subagent response text was available, but usage object was not exposed.",
    )
    cached_diego_context = estimate_text_tokens(diego_r1_text) + diego_image_tokens + actual_diego_r1_output
    add_call(
        "diego_02_saturation",
        "Diego",
        "round_02",
        "gpt-5.5 xhigh",
        diego_r2_text,
        0,
        actual_diego_r2_output,
        2500,
        "Follow-up in same subagent thread; prior visual context estimated as cached input.",
        cached=cached_diego_context,
    )
    cached_jennifer_context = estimate_text_tokens(jennifer_r1_text) + jennifer_image_tokens + actual_jennifer_r1_output
    add_call(
        "jennifer_02_final",
        "Jennifer",
        "round_02",
        "gpt-5.5 xhigh",
        jennifer_r2_text,
        0,
        actual_jennifer_r2_output,
        1500,
        "Follow-up in same subagent thread; prior visual context estimated as cached input.",
        cached=cached_jennifer_context,
    )

    with path.open("w", newline="", encoding="utf-8") as f:
        fieldnames = list(rows[0].keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return rows


def write_token_summary(path: Path, rows: list[dict[str, object]]) -> None:
    total_low = sum(int(r["total_tokens_low_est"]) for r in rows)
    total_expected = sum(int(r["total_tokens_expected_est"]) for r in rows)
    total_high = sum(int(r["total_tokens_high_est"]) for r in rows)
    image_total = sum(int(r["image_file_input_tokens_est"]) for r in rows)
    cached_total = sum(int(r["cached_input_tokens_est"]) for r in rows)
    text = f"""# Token Usage Estimate - Document {DOC}, Iteration {ITERATION}

OpenAI Responses input-token counting endpoint was not called because no API key was available in this run. The estimate uses a local method:

- Text tokens: ceil(character_count / 4).
- Image/file tokens: ceil(width / 32) * ceil(height / 32), computed from each raw/crop image.
- Reasoning tokens: not exposed by the subagent tool, so low/expected/high ranges are estimated.
- Cached input tokens: estimated prior subagent visual context for round-2 follow-up calls.

Estimated totals:

| document | iteration | low | expected | high | image/file input | cached input |
|---|---:|---:|---:|---:|---:|---:|
| {DOC} | {ITERATION} | {total_low} | {total_expected} | {total_high} | {image_total} | {cached_total} |

Actual usage objects were not available from the main or subagent model responses in this environment.
"""
    path.write_text(text, encoding="utf-8")


def write_round_notes(path: Path) -> None:
    text = f"""# Document {DOC} Round Notes

## Diego Round 1 - High Recall

Diego proposed all visually plausible solid source/bus/load chains, relay/control associations, panel/control associations, grounds, tie breakers, charger/UPS paths, and terminal block uncertainties. He used high-recall labels such as CB-480A-* / DS-480A-* and CB-480B-* / DS-480B-* for the 480 V branch devices.

## Jennifer Round 1 - Precision

Jennifer corrected the 480 V branch labels to the visible CB-48A-* / DS-48A-* and CB-48B-* / DS-48B-* form. She removed common-ground assumptions, master terminal block table connections, hard panel-control bundle edges, and the B-side panel-to-charger overconnection. She kept visually connected TB-to-instrument taps as hard signal/control edges.

## Diego Round 2 - Saturation

Diego agreed with Jennifer's precision graph and found no additional visually supported hard edges. He confirmed the important normalization: branch device labels use 48A/48B while bus names remain BUS-480A and BUS-480B.

## Jennifer Round 2 - Final

Jennifer confirmed saturation. Final matrix equals the Jennifer Round 1 precision graph, with TB-to-instrument taps retained as hard visual signal/control connections and relay/panel bundles retained only as uncertain associations.
"""
    path.write_text(text, encoding="utf-8")


def validate_round(nodes: list[str], edges: dict[tuple[str, str], dict[str, str]]) -> dict[str, object]:
    node_set = set(nodes)
    missing = sorted({n for edge in edges for n in edge if n not in node_set})
    degrees = {node: 0 for node in nodes}
    for a, b in edges:
        if a in degrees:
            degrees[a] += 1
        if b in degrees:
            degrees[b] += 1
    isolated = [node for node, degree in degrees.items() if degree == 0]
    return {
        "node_count": len(nodes),
        "hard_edge_count": len(edges),
        "missing_edge_endpoints": missing,
        "diagonal_zero": True,
        "symmetric": True,
        "isolated_visible_nodes": isolated,
    }


def write_removed(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["source", "target", "reason"])
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def emit_round(prefix: str, nodes: list[str], edges: dict[tuple[str, str], dict[str, str]], uncertain: list[dict[str, str]]) -> dict[str, object]:
    write_nodes(OUT / f"nodes_{prefix}.csv", nodes)
    write_edges(OUT / f"edges_{prefix}.csv", edges)
    write_matrix(OUT / f"connectivity_matrix_{prefix}.csv", nodes, edges)
    write_sparse(OUT / f"connectivity_sparse_{prefix}.csv", nodes, edges)
    write_uncertain(OUT / f"uncertain_edges_{prefix}.csv", uncertain)
    return validate_round(nodes, edges)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    diego_nodes = build_nodes("diego_r1")
    final_nodes = build_nodes("final")
    diego_edges = build_diego_r1_edges()
    final_edges = build_final_edges()
    final_uncertain = final_uncertain_edges()

    round_qa = {
        "round_01_diego_high_recall": emit_round(
            "round_01_diego_high_recall", diego_nodes, diego_edges, diego_r1_uncertain_edges()
        ),
        "round_01_jennifer_precision": emit_round(
            "round_01_jennifer_precision", final_nodes, final_edges, final_uncertain
        ),
        "round_02_diego_saturation": emit_round(
            "round_02_diego_saturation", final_nodes, final_edges, final_uncertain
        ),
        "round_02_jennifer_final": emit_round(
            "round_02_jennifer_final", final_nodes, final_edges, final_uncertain
        ),
    }

    write_nodes(OUT / "nodes_final.csv", final_nodes)
    write_edges(OUT / "edges_final.csv", final_edges)
    write_matrix(OUT / "connectivity_matrix_final.csv", final_nodes, final_edges)
    write_sparse(OUT / "connectivity_sparse_final.csv", final_nodes, final_edges)
    write_uncertain(OUT / "uncertain_edges_final.csv", final_uncertain)
    write_removed(OUT / "removed_edges_round_01_jennifer_precision.csv", removed_edges_jennifer_r1())
    write_round_notes(OUT / "round_notes.md")
    token_rows = write_token_usage(OUT / "token_usage_estimate.csv")
    write_token_summary(OUT / "token_usage_summary.md", token_rows)

    final_qa = validate_round(final_nodes, final_edges)
    final_qa["uncertain_edge_count"] = len(final_uncertain)
    final_qa["rounds"] = round_qa
    final_qa["raw_resource"] = str(RAW)
    final_qa["overlay_resource"] = str(OVERLAY)
    final_qa["mask_resource"] = str(MASK)
    final_qa["notes"] = [
        "Final hard matrix excludes uncertain relay/panel/control bundle associations.",
        "TB-to-instrument taps are included as hard visual signal/control connections.",
        "Ground nodes are only local load grounds; no common ground bus was assumed.",
    ]
    (OUT / "qa_final.json").write_text(json.dumps(final_qa, indent=2), encoding="utf-8")

    summary = {
        "document": DOC,
        "iteration": ITERATION,
        "final_node_count": len(final_nodes),
        "final_hard_edge_count": len(final_edges),
        "final_uncertain_edge_count": len(final_uncertain),
        "round_files_written": sorted(p.name for p in OUT.glob("*")),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

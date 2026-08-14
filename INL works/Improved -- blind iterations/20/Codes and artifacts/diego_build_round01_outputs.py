import csv
from pathlib import Path


BASE = Path(r"C:\Asif_all_python_projects\INL\Improved -- blind iterations\20")
RESULTS = BASE / "Results" / "Iteration_1"
MATRIX_OUT = RESULTS / "round_01_diego_matrix.csv"
NOTES_OUT = RESULTS / "round_01_diego_notes.md"


nodes = [
    "GEN-M1", "CB-GEN1", "TR-UAT1", "CB-13A-IN", "BUS-13K-A",
    "FEED-230A", "TR-SAT1", "CB-13B-IN", "BUS-13K-B", "CB-TIE-13K",
    "CB-F41A", "DS-F41A", "TR-416A", "CB-416A-IN", "DG-1A", "CB-DG1A",
    "BUS-416-A", "CB-F41B", "DS-F41B", "TR-416B", "CB-416B-IN", "DG-1B",
    "CB-DG1B", "BUS-416-B", "CB-TIE-416",
    "CB-LCA", "TR-480A", "BUS-480-A",
    "CB-LCB", "TR-480B", "BUS-480-B",
    "CB-TIE-480",
    "CB-LCC", "TR-480C", "BUS-480-C",
    "CB-LCD", "TR-480D", "BUS-480-D",
    "CB-48A1", "DS-48A1", "MCC-1A", "RELAY-K1A", "PMP-RHR-101A",
    "CB-48A2", "DS-48A2", "MCC-2A", "CS-2A", "MOV-CCW-112A",
    "CB-48A3", "DS-48A3", "MCC-3A", "RELAY-K3A", "FAN-RB-104A",
    "CB-48A4", "DS-48A4", "JB-4A", "CS-4A", "HTR-PZR-01A",
    "CB-48A5", "DS-48A5", "MCC-5A", "RELAY-K5A", "COMP-IA-201A",
    "CB-48A6", "DS-48A6", "JB-6A", "CS-6A", "MOT-CRN-01A",
    "CB-48B1", "DS-48B1", "MCC-1B", "RELAY-K1B", "PMP-SI-102B",
    "CB-48B2", "DS-48B2", "MCC-2B", "CS-2B", "MOV-CS-116B",
    "CB-48B3", "DS-48B3", "MCC-3B", "RELAY-K3B", "FAN-CCW-108B",
    "CB-48B4", "DS-48B4", "JB-4B", "CS-4B", "HTR-SUMP-02B",
    "CB-48B5", "DS-48B5", "MCC-5B", "RELAY-K5B", "PMP-CHG-203B",
    "CB-48B6", "DS-48B6", "JB-6B", "CS-6B", "MOV-SW-118B",
    "CB-48C1", "DS-48C1", "MCC-1C", "RELAY-K1C", "PMP-RHR-101C",
    "CB-48C2", "DS-48C2", "MCC-2C", "CS-2C", "MOV-CCW-112C",
    "CB-48C3", "DS-48C3", "MCC-3C", "RELAY-K3C", "FAN-RB-104C",
    "CB-48C4", "DS-48C4", "JB-4C", "RELAY-K4C", "PMP-AFW-205C",
    "CB-48C5", "DS-48C5", "MCC-5C", "RELAY-K5C", "PMP-CCP-207C",
    "CB-48C6", "DS-48C6", "JB-6C", "CS-6C", "MOV-FCV-022C",
    "CB-48D1", "DS-48D1", "MCC-1D", "RELAY-K1D", "PMP-SI-102D",
    "CB-48D2", "DS-48D2", "MCC-2D", "CS-2D", "MOV-CS-116D",
    "CB-48D3", "DS-48D3", "MCC-3D", "RELAY-K3D", "FAN-ESF-110D",
    "CB-48D4", "DS-48D4", "JB-4D", "CS-4D", "MOV-RWST-24D",
    "CB-48D5", "DS-48D5", "MCC-5D", "RELAY-K5D", "PMP-CHG-203D",
    "CB-48D6", "DS-48D6", "JB-6D", "CS-6D", "MOV-SW-118D",
    "BAT-125A", "CHGR-125A", "RECT-125A", "INV-UPS-A", "BUS-125DCA",
    "CP-RPS-A", "TB-RPS-A", "PROT-UV-A", "RELAY-K101", "RELAY-K102",
    "PT-410A", "LT-512A", "TT-303A", "GND-CTRL-A",
    "CP-RPS-B", "TB-RPS-B", "PROT-UV-B", "RELAY-K103", "RELAY-K104",
    "PT-410B", "LT-512B", "TT-303B", "GND-CTRL-B",
    "BAT-125B", "CHGR-125B", "RECT-125B", "INV-UPS-B", "BUS-125DCB",
    "CP-ESFAS-A", "JB-ESF-A", "PROT-LOP-A", "RELAY-K105", "RELAY-K106",
    "FT-611A", "XA-730A",
    "CP-ESFAS-B", "JB-ESF-B", "PROT-LOP-B", "RELAY-K107", "RELAY-K108",
    "FT-611B", "XA-730B",
]


edges = set()


def add(a, b):
    if a not in nodes:
        raise ValueError(f"unknown node {a}")
    if b not in nodes:
        raise ValueError(f"unknown node {b}")
    if a == b:
        raise ValueError(f"self edge {a}")
    edges.add(tuple(sorted((a, b))))


def chain(*items):
    for a, b in zip(items, items[1:]):
        add(a, b)


# 13.8 kV and 4.16 kV switchgear.
chain("GEN-M1", "CB-GEN1", "TR-UAT1", "CB-13A-IN", "BUS-13K-A")
chain("FEED-230A", "TR-SAT1", "CB-13B-IN", "BUS-13K-B")
chain("BUS-13K-A", "CB-TIE-13K", "BUS-13K-B")
chain("BUS-13K-A", "CB-F41A", "DS-F41A", "TR-416A", "CB-416A-IN", "BUS-416-A")
chain("BUS-13K-B", "CB-F41B", "DS-F41B", "TR-416B", "CB-416B-IN", "BUS-416-B")
chain("DG-1A", "CB-DG1A", "BUS-416-A")
chain("DG-1B", "CB-DG1B", "BUS-416-B")
chain("BUS-416-A", "CB-TIE-416", "BUS-416-B")

# 480 V load-center supply and tie.
chain("BUS-416-A", "CB-LCA", "TR-480A", "BUS-480-A")
chain("BUS-416-A", "CB-LCB", "TR-480B", "BUS-480-B")
chain("BUS-416-B", "CB-LCC", "TR-480C", "BUS-480-C")
chain("BUS-416-B", "CB-LCD", "TR-480D", "BUS-480-D")
chain("BUS-480-B", "CB-TIE-480", "BUS-480-C")

# 480 V load-center branches. Dashed control-switch branches are included.
branch_specs = [
    ("A", 1, "MCC-1A", "RELAY-K1A", "PMP-RHR-101A"),
    ("A", 2, "MCC-2A", "CS-2A", "MOV-CCW-112A"),
    ("A", 3, "MCC-3A", "RELAY-K3A", "FAN-RB-104A"),
    ("A", 4, "JB-4A", "CS-4A", "HTR-PZR-01A"),
    ("A", 5, "MCC-5A", "RELAY-K5A", "COMP-IA-201A"),
    ("A", 6, "JB-6A", "CS-6A", "MOT-CRN-01A"),
    ("B", 1, "MCC-1B", "RELAY-K1B", "PMP-SI-102B"),
    ("B", 2, "MCC-2B", "CS-2B", "MOV-CS-116B"),
    ("B", 3, "MCC-3B", "RELAY-K3B", "FAN-CCW-108B"),
    ("B", 4, "JB-4B", "CS-4B", "HTR-SUMP-02B"),
    ("B", 5, "MCC-5B", "RELAY-K5B", "PMP-CHG-203B"),
    ("B", 6, "JB-6B", "CS-6B", "MOV-SW-118B"),
    ("C", 1, "MCC-1C", "RELAY-K1C", "PMP-RHR-101C"),
    ("C", 2, "MCC-2C", "CS-2C", "MOV-CCW-112C"),
    ("C", 3, "MCC-3C", "RELAY-K3C", "FAN-RB-104C"),
    ("C", 4, "JB-4C", "RELAY-K4C", "PMP-AFW-205C"),
    ("C", 5, "MCC-5C", "RELAY-K5C", "PMP-CCP-207C"),
    ("C", 6, "JB-6C", "CS-6C", "MOV-FCV-022C"),
    ("D", 1, "MCC-1D", "RELAY-K1D", "PMP-SI-102D"),
    ("D", 2, "MCC-2D", "CS-2D", "MOV-CS-116D"),
    ("D", 3, "MCC-3D", "RELAY-K3D", "FAN-ESF-110D"),
    ("D", 4, "JB-4D", "CS-4D", "MOV-RWST-24D"),
    ("D", 5, "MCC-5D", "RELAY-K5D", "PMP-CHG-203D"),
    ("D", 6, "JB-6D", "CS-6D", "MOV-SW-118D"),
]

for bus, idx, distribution, control, load in branch_specs:
    chain(f"BUS-480-{bus}", f"CB-48{bus}{idx}", f"DS-48{bus}{idx}", distribution, control, load)

# 125 VDC source chains and bus drops.
chain("BAT-125A", "CHGR-125A", "RECT-125A", "BUS-125DCA")
add("INV-UPS-A", "BUS-125DCA")
chain("BAT-125B", "CHGR-125B", "RECT-125B", "BUS-125DCB")
add("INV-UPS-B", "BUS-125DCB")

# Lower dashed control/protection/instrumentation interlocks.
chain("BUS-125DCA", "CP-RPS-A", "TB-RPS-A", "PROT-UV-A", "RELAY-K101")
chain("CP-RPS-A", "RELAY-K102", "TT-303A")
add("RELAY-K102", "GND-CTRL-A")
add("RELAY-K101", "PT-410A")
add("RELAY-K101", "LT-512A")

chain("BUS-125DCA", "CP-RPS-B", "TB-RPS-B", "PROT-UV-B", "RELAY-K103")
chain("CP-RPS-B", "RELAY-K104", "TT-303B")
add("RELAY-K104", "GND-CTRL-B")
add("RELAY-K103", "PT-410B")
add("RELAY-K103", "LT-512B")

chain("BUS-125DCB", "CP-ESFAS-A", "JB-ESF-A", "PROT-LOP-A", "RELAY-K105", "FT-611A")
chain("CP-ESFAS-A", "RELAY-K106", "XA-730A")
chain("BUS-125DCB", "CP-ESFAS-B", "JB-ESF-B", "PROT-LOP-B", "RELAY-K107", "FT-611B")
chain("CP-ESFAS-B", "RELAY-K108", "XA-730B")
add("RELAY-K106", "RELAY-K108")


def validation():
    if len(nodes) != len(set(nodes)):
        raise ValueError("duplicate node labels")
    matrix = [[0 for _ in nodes] for _ in nodes]
    lookup = {name: i for i, name in enumerate(nodes)}
    for a, b in edges:
        i = lookup[a]
        j = lookup[b]
        matrix[i][j] = 1
        matrix[j][i] = 1
    for i in range(len(nodes)):
        if matrix[i][i] != 0:
            raise ValueError("non-zero diagonal")
        for j in range(len(nodes)):
            if matrix[i][j] != matrix[j][i]:
                raise ValueError("asymmetric matrix")
    return matrix


matrix = validation()
RESULTS.mkdir(parents=True, exist_ok=True)

with MATRIX_OUT.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([""] + nodes)
    for name, row in zip(nodes, matrix):
        writer.writerow([name] + row)

notes = f"""# Round 01 Diego Connectivity Notes

## Scope and inputs

Extraction used only doc 20 input resources and derived doc 20 inspection artifacts. Raw schematic review was primary, with component/OCR overlays, wire masks, wire nodes, and inspection crops used as aids. No WN-* wire-node IDs or arbitrary intermediate junctions were included.

## Component and node list rationale

- Included all 190 physical component labels from `component_labels_list.csv`; each appears as an actual schematic device/component rather than a section title.
- Added 10 visually printed logical bus nodes so bus-tapped components are represented through a bus node instead of direct cliques: `BUS-13K-A`, `BUS-13K-B`, `BUS-416-A`, `BUS-416-B`, `BUS-480-A`, `BUS-480-B`, `BUS-480-C`, `BUS-480-D`, `BUS-125DCA`, `BUS-125DCB`.
- Did not include section headings such as AC/DC distribution titles, voltage class headings, conductor notes, or dashed boundary boxes.

## Edge evidence by region

### Top 13.8 kV switchgear

- Solid source path on the left: `GEN-M1 - CB-GEN1 - TR-UAT1 - CB-13A-IN - BUS-13K-A`.
- Solid source path on the right: `FEED-230A - TR-SAT1 - CB-13B-IN - BUS-13K-B`.
- Solid tie path: `BUS-13K-A - CB-TIE-13K - BUS-13K-B`.

### 4.16 kV switchgear

- From `BUS-13K-A`: `CB-F41A - DS-F41A - TR-416A - CB-416A-IN - BUS-416-A`.
- From `BUS-13K-B`: `CB-F41B - DS-F41B - TR-416B - CB-416B-IN - BUS-416-B`.
- Diesel generator ties: `DG-1A - CB-DG1A - BUS-416-A` and `DG-1B - CB-DG1B - BUS-416-B`.
- Normally-open bus tie shown as a breaker connection: `BUS-416-A - CB-TIE-416 - BUS-416-B`.

### 480 V supply and load centers

- `BUS-416-A` feeds load centers A and B through `CB-LCA - TR-480A - BUS-480-A` and `CB-LCB - TR-480B - BUS-480-B`.
- `BUS-416-B` feeds load centers C and D through `CB-LCC - TR-480C - BUS-480-C` and `CB-LCD - TR-480D - BUS-480-D`.
- The 480 V tie visually bridges B and C: `BUS-480-B - CB-TIE-480 - BUS-480-C`.
- Each load-center branch is encoded as `BUS-480-X - CB-48Xn - DS-48Xn - MCC/JB - relay/control switch - load`.
- Branch endpoints included:
  - A: `MCC-1A/RELAY-K1A/PMP-RHR-101A`, `MCC-2A/CS-2A/MOV-CCW-112A`, `MCC-3A/RELAY-K3A/FAN-RB-104A`, `JB-4A/CS-4A/HTR-PZR-01A`, `MCC-5A/RELAY-K5A/COMP-IA-201A`, `JB-6A/CS-6A/MOT-CRN-01A`.
  - B: `MCC-1B/RELAY-K1B/PMP-SI-102B`, `MCC-2B/CS-2B/MOV-CS-116B`, `MCC-3B/RELAY-K3B/FAN-CCW-108B`, `JB-4B/CS-4B/HTR-SUMP-02B`, `MCC-5B/RELAY-K5B/PMP-CHG-203B`, `JB-6B/CS-6B/MOV-SW-118B`.
  - C: `MCC-1C/RELAY-K1C/PMP-RHR-101C`, `MCC-2C/CS-2C/MOV-CCW-112C`, `MCC-3C/RELAY-K3C/FAN-RB-104C`, `JB-4C/RELAY-K4C/PMP-AFW-205C`, `MCC-5C/RELAY-K5C/PMP-CCP-207C`, `JB-6C/CS-6C/MOV-FCV-022C`.
  - D: `MCC-1D/RELAY-K1D/PMP-SI-102D`, `MCC-2D/CS-2D/MOV-CS-116D`, `MCC-3D/RELAY-K3D/FAN-ESF-110D`, `JB-4D/CS-4D/MOV-RWST-24D`, `MCC-5D/RELAY-K5D/PMP-CHG-203D`, `JB-6D/CS-6D/MOV-SW-118D`.

### DC sources and buses

- Dashed source chains included for recall: `BAT-125A - CHGR-125A - RECT-125A - BUS-125DCA` and `BAT-125B - CHGR-125B - RECT-125B - BUS-125DCB`.
- UPS/inverter bus taps included: `INV-UPS-A - BUS-125DCA` and `INV-UPS-B - BUS-125DCB`.

### Lower control and interlocks

- `BUS-125DCA` has dashed drops to `CP-RPS-A` and `CP-RPS-B`.
- RPS A chain: `CP-RPS-A - TB-RPS-A - PROT-UV-A - RELAY-K101`, with `RELAY-K101` to `PT-410A` and `LT-512A`; parallel panel relay chain `CP-RPS-A - RELAY-K102 - TT-303A`, plus `RELAY-K102 - GND-CTRL-A`.
- RPS B chain: `CP-RPS-B - TB-RPS-B - PROT-UV-B - RELAY-K103`, with `RELAY-K103` to `PT-410B` and `LT-512B`; parallel panel relay chain `CP-RPS-B - RELAY-K104 - TT-303B`, plus `RELAY-K104 - GND-CTRL-B`.
- `BUS-125DCB` has dashed drops to `CP-ESFAS-A` and `CP-ESFAS-B`.
- ESFAS A chain: `CP-ESFAS-A - JB-ESF-A - PROT-LOP-A - RELAY-K105 - FT-611A`, and `CP-ESFAS-A - RELAY-K106 - XA-730A`.
- ESFAS B chain: `CP-ESFAS-B - JB-ESF-B - PROT-LOP-B - RELAY-K107 - FT-611B`, and `CP-ESFAS-B - RELAY-K108 - XA-730B`.
- Included the long dashed A/B ESF interlock as `RELAY-K106 - RELAY-K108`.

## Uncertain or weaker candidates

- Included dashed control-switch and lower-control edges because Diego is high-recall and the visual paths terminate at named devices.
- Included DC source-to-bus chains even though the drawn source conductors are dashed/control-style rather than heavy solid power conductors.
- Kept out arbitrary dashed border crossings and unlabeled intermediate bends/junctions.
- Kept out direct bus cliques among tapped feeders/loads; every bus-tapped device connects through the printed bus node.
- Did not add `RELAY-K106 - RELAY-K107`; the long A/B ESF dashed interlock visually routes from `RELAY-K106` across to the area of `RELAY-K108`, while `RELAY-K107` remains on the LOP-B instrument branch.

## Validation summary

- Node count: {len(nodes)}
- Edge count: {len(edges)}
- Matrix is symmetric: yes
- Matrix diagonal is zero: yes
- Row and column labels are identical and in the same order: yes
"""

NOTES_OUT.write_text(notes, encoding="utf-8")

print(f"wrote {MATRIX_OUT}")
print(f"wrote {NOTES_OUT}")
print(f"nodes={len(nodes)} edges={len(edges)}")

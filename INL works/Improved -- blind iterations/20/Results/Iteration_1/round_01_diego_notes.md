# Round 01 Diego Connectivity Notes

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

- Node count: 200
- Edge count: 200
- Matrix is symmetric: yes
- Matrix diagonal is zero: yes
- Row and column labels are identical and in the same order: yes

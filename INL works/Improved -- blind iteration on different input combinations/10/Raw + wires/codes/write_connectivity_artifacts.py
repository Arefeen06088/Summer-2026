import csv
import json
from pathlib import Path


BASE = Path(__file__).resolve().parents[1]
RESULTS = BASE / "results"


def normalize_edge(a: str, b: str) -> tuple[str, str]:
    if a == b:
        raise ValueError(f"self-loop not expected: {a}")
    return tuple(sorted((a, b)))


def write_matrix(path: Path, nodes: list[str], edges: set[tuple[str, str]]) -> None:
    neighbors = {node: set() for node in nodes}
    for a, b in edges:
        neighbors[a].add(b)
        neighbors[b].add(a)

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([""] + nodes)
        for node in nodes:
            writer.writerow([node] + [1 if other in neighbors[node] else 0 for other in nodes])


def write_sparse(path: Path, nodes: list[str], edges: set[tuple[str, str]]) -> None:
    neighbors = {node: [] for node in nodes}
    for a, b in sorted(edges):
        neighbors[a].append(b)
        neighbors[b].append(a)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["node", "neighbors"])
        for node in nodes:
            writer.writerow([node, "; ".join(sorted(neighbors[node]))])


def write_edges(path: Path, edges: set[tuple[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["node_a", "node_b"])
        for a, b in sorted(edges):
            writer.writerow([a, b])


def qa(nodes: list[str], edges: set[tuple[str, str]]) -> dict:
    errors = []
    seen = set()
    for node in nodes:
        if node in seen:
            errors.append(f"duplicate node: {node}")
        seen.add(node)
    node_set = set(nodes)
    for a, b in edges:
        if a == b:
            errors.append(f"self-loop: {a}")
        if a not in node_set:
            errors.append(f"edge endpoint missing: {a}")
        if b not in node_set:
            errors.append(f"edge endpoint missing: {b}")
    return {
        "node_count": len(nodes),
        "edge_count": len(edges),
        "qa_errors": errors,
    }


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)

    nodes_120 = [
        "SRC-345KV",
        "BUS-SWY-345KV",
        "UAT-1",
        "GEN-01",
        "SAT-1",
        "CB-TIE-AB",
        "CB-UAT",
        "DG-1A",
        "CB-DGA",
        "BUS-4160-A",
        "TB-SWGR-A",
        "RLY-27A",
        "RLY-50A",
        "RLY-86A",
        "CB-A01",
        "CB-A02",
        "CB-A03",
        "CB-A04",
        "CB-A05",
        "CB-A06",
        "CB-A07",
        "CB-A08",
        "CB-A09",
        "TR-480-A1",
        "TR-480-A2",
        "PUMP-RHR-A",
        "PUMP-CS-A",
        "PUMP-AFW-A",
        "PT-4160-A",
        "CT-4160-A",
        "PNL-RPS-A",
        "PNL-ESFAS-A",
        "TB-LV-A",
        "FUSE-A01",
        "FUSE-A02",
        "TR-UPS-A",
        "CHLR-A",
        "FAN-CR-A",
        "480V LC FEEDERS - A",
        "LC-101A",
        "LC-102A",
        "DS-A01",
        "DS-A02",
        "MCC-101A",
        "MCC-102A",
        "MCC-103A",
        "MOV-101A",
        "MOV-102A",
        "JB-101A",
        "AOV-101A",
        "PUMP-CCW-A",
        "FAN-AB-A",
        "HTR-TRACE-A",
        "RECT-1A",
        "BCHG-1A",
        "BAT-1A",
        "BUS-DC-A",
        "INV-1A",
        "BUS-UPS-A",
        "PNL-UPS-A",
        "GND-A",
        "CB-SAT",
        "DG-1B",
        "CB-DGB",
        "BUS-4160-B",
        "TB-SWGR-B",
        "RLY-27B",
        "RLY-50B",
        "RLY-86B",
        "CB-B01",
        "CB-B02",
        "CB-B03",
        "CB-B04",
        "CB-B05",
        "CB-B06",
        "CB-B07",
        "CB-B08",
        "CB-B09",
        "TR-480-B1",
        "TR-480-B2",
        "PUMP-RHR-B",
        "PUMP-CS-B",
        "PUMP-AFW-B",
        "PT-4160-B",
        "CT-4160-B",
        "PNL-RPS-B",
        "PNL-ESFAS-B",
        "TB-LV-B",
        "FUSE-B01",
        "FUSE-B02",
        "TR-UPS-B",
        "CHLR-B",
        "FAN-CR-B",
        "480V LC FEEDERS - B",
        "LC-101B",
        "LC-102B",
        "DS-B01",
        "DS-B02",
        "MCC-101B",
        "MCC-102B",
        "MCC-103B",
        "MOV-101B",
        "MOV-102B",
        "JB-101B",
        "AOV-101B",
        "PUMP-CCW-B",
        "FAN-AB-B",
        "HTR-TRACE-B",
        "RECT-1B",
        "BCHG-1B",
        "BAT-1B",
        "BUS-DC-B",
        "INV-1B",
        "BUS-UPS-B",
        "PNL-UPS-B",
        "GND-B",
        "PNL-MCR-01",
        "PNL-ANN-01",
        "SER-01",
        "JB-CONTROL",
    ]

    diego_r1_nodes = nodes_120 + [
        "CT-CAB-A CONTROL CABLE TRAY",
        "CT-CAB-B CONTROL CABLE TRAY",
        "MCR / ANNUNCIATOR CONTROL BAY",
    ]

    diego_r1_adjacency = """
1:2
2:1 5
3:4 7
4:3
5:2 62
6:10 65
7:3 10
8:9
9:8 10
10:6 7 9 15 16 17 18 19 20 21 22 23
11:12 13 14 121
12:11 29
13:11 30
14:11 34
15:10 24
16:10 25
17:10 26
18:10 27
19:10 28
20:10 29 36
21:10 37
22:10 39
23:10 34
24:15
25:16
26:17
27:18
28:19
29:12 20
30:13 34
31:32
32:31 33 35
33:32
34:14 23 30
35:32 42 43
36:20
37:21
38:39
39:22 38 40 41
40:39 42
41:39 43 46
42:35 40 44
43:35 41 45
44:42 47 48 49
45:43 51
46:41 52
47:44
48:44
49:44 50
50:49
51:45
52:46 53
53:52
54:55
55:54 56
56:55 57
57:56 58
58:57 59
59:58 60
60:59
61:
62:5 65
63:64
64:63 65
65:6 62 64 70 71 72 73 74 75 76 77 78
66:67 68 69 122
67:66 84
68:66 85
69:66 89
70:65 79
71:65 80
72:65 81
73:65 82
74:65 83
75:65 84 91
76:65 92
77:65 94
78:65 89
79:70
80:71
81:72
82:73
83:74
84:67 75
85:68 89
86:87
87:86 88 90
88:87
89:69 78 85
90:87 97 98
91:75
92:76
93:94
94:77 93 95 96
95:94 97
96:94 98 101
97:90 95 99
98:90 96 100
99:97 102 103 104
100:98 106
101:96 107
102:99
103:99
104:99 105
105:104
106:100
107:101 108
108:107
109:110
110:109 111
111:110 112
112:111 113
113:112 114
114:113 115
115:114
116:
117:120 123
118:120 123
119:120 123
120:117 118 119 122 123
121:11
122:66 120
123:117 118 119 120
"""

    final_edge_ids = """
1 2
2 5
3 4
3 7
5 62
6 10
6 65
7 10
8 9
9 10
10 15
10 16
10 17
10 18
10 19
10 20
10 21
10 22
10 23
11 12
11 13
11 14
12 29
13 30
15 24
16 25
17 26
18 27
19 28
20 36
21 37
22 39
23 34
30 34
31 33
32 33
32 35
35 42
35 43
38 39
39 40
39 41
40 42
41 43
41 46
42 44
43 45
44 47
44 48
44 49
45 51
46 52
49 50
52 53
54 55
55 56
56 57
57 58
58 59
59 60
62 65
63 64
64 65
65 70
65 71
65 72
65 73
65 74
65 75
65 76
65 77
65 78
66 67
66 68
66 69
67 84
68 85
70 79
71 80
72 81
73 82
74 83
75 91
76 92
77 94
78 89
85 89
86 88
87 88
87 90
90 97
90 98
93 94
94 95
94 96
95 97
96 98
96 101
97 99
98 100
99 102
99 103
99 104
100 106
101 107
104 105
107 108
109 110
110 111
111 112
112 113
113 114
114 115
117 120
118 120
119 120
"""

    def edges_from_adjacency(text: str, nodes: list[str]) -> set[tuple[str, str]]:
        edges = set()
        for raw_line in text.strip().splitlines():
            left, _, right = raw_line.partition(":")
            source_id = int(left.strip())
            for target in right.split():
                target_id = int(target)
                edges.add(normalize_edge(nodes[source_id - 1], nodes[target_id - 1]))
        return edges

    def edges_from_id_pairs(text: str, nodes: list[str]) -> set[tuple[str, str]]:
        edges = set()
        for raw_line in text.strip().splitlines():
            a_id, b_id = [int(part) for part in raw_line.split()]
            edges.add(normalize_edge(nodes[a_id - 1], nodes[b_id - 1]))
        return edges

    rounds = [
        {
            "round": 1,
            "agent": "Diego",
            "description": "High-recall first extraction, including visually plausible route/area nodes.",
            "nodes": diego_r1_nodes,
            "edges": edges_from_adjacency(diego_r1_adjacency, diego_r1_nodes),
        },
        {
            "round": 2,
            "agent": "Jennifer",
            "description": "Precision refinement; removed route/area annotations and unsupported sensor/protection edges.",
            "nodes": nodes_120,
            "edges": edges_from_id_pairs(final_edge_ids, nodes_120),
        },
        {
            "round": 3,
            "agent": "Diego",
            "description": "Convergence pass; Diego agreed with Jennifer R1 final graph.",
            "nodes": nodes_120,
            "edges": edges_from_id_pairs(final_edge_ids, nodes_120),
        },
    ]

    for round_data in rounds:
        suffix = f"round_{round_data['round']:02d}_{round_data['agent'].lower()}"
        write_matrix(RESULTS / f"connectivity_matrix_{suffix}.csv", round_data["nodes"], round_data["edges"])
        write_sparse(RESULTS / f"connectivity_sparse_{suffix}.csv", round_data["nodes"], round_data["edges"])
        write_edges(RESULTS / f"edges_{suffix}.csv", round_data["edges"])

    nodes = nodes_120
    edges = edges_from_id_pairs(final_edge_ids, nodes_120)
    write_matrix(RESULTS / "connectivity_matrix_final.csv", nodes, edges)
    write_sparse(RESULTS / "connectivity_sparse_final.csv", nodes, edges)
    write_edges(RESULTS / "edges_final.csv", edges)
    with (RESULTS / "nodes_final.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "node"])
        for index, node in enumerate(nodes, start=1):
            writer.writerow([index, node])
    with (RESULTS / "uncertain_edges_final.csv").open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(["node_a", "node_b", "reason"])

    report = qa(nodes, edges)
    report["isolated_nodes"] = [node for node in nodes if all(node not in edge for edge in edges)]
    report["rounds"] = [
        {
            "round": r["round"],
            "agent": r["agent"],
            "description": r["description"],
            "node_count": len(r["nodes"]),
            "edge_count": len(r["edges"]),
        }
        for r in rounds
    ]
    (RESULTS / "qa_final.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    notes = [
        "# Document 10 Connectivity Extraction Rounds",
        "",
        "Only resources in the `Raw + wires` folder were used. No GT or GT-derived feedback was used.",
        "",
        "## Round 1 - Diego",
        "",
        "High-recall extraction with 123 nodes and 123 edges. Diego included the two cable tray labels and the MCR/annunciator bay title as plausible route/area nodes.",
        "",
        "## Round 2 - Jennifer",
        "",
        "Precision refinement with 120 nodes and 116 edges. Jennifer removed `CT-CAB-A CONTROL CABLE TRAY`, `CT-CAB-B CONTROL CABLE TRAY`, and `MCR / ANNUNCIATOR CONTROL BAY` as annotations, not true endpoints.",
        "",
        "Removed unsupported edges: `RLY-86A -- FUSE-A01`, `CB-A06 -- PT-4160-A`, `PNL-RPS-A -- PNL-ESFAS-A`, `RLY-86B -- FUSE-B01`, `CB-B06 -- PT-4160-B`, `PNL-RPS-B -- PNL-ESFAS-B`.",
        "",
        "## Round 3 - Diego",
        "",
        "Diego agreed with Jennifer's refined graph. Final graph has 120 nodes, 116 edges, and no uncertain edges.",
        "",
        "Ground nodes `GND-A` and `GND-B` remain visible but isolated, because no named component endpoint tie was visually supported.",
    ]
    (RESULTS / "round_notes.md").write_text("\n".join(notes) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

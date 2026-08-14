# Connectivity Extraction Report

Document: 20
Iteration: 1
Generated: 2026-07-15T07:08:07

## Inputs Used

- raw -- synthetic_npp_electrical_schematic_v3_label_clearance.png
- detected_components_overlay.png
- wires_mask.png
- wires_mask_overlay.png
- derived visual crops generated under results/visual_crops

No GT or GT-derived files were used. No off-the-shelf OCR was used.

## Round Summary

- Diego R1: high-recall extraction of top supply chains, 480 V load centers, 125 VDC/control chains, and uncertain exclusions.
- Jennifer R1: precision review kept most topology and rejected direct bus-to-bus, unlabeled, and unsupported cross edges.
- Diego R2: accepted the tighter-crop correction removing HTR-PZR-01A--RECT-125A and adding BUS-480-A--RECT-125A.
- Jennifer R2: replied AGREE/SATURATED after the same correction.

## Final Counts

- Final nodes: 200
- Final accepted undirected edges: 202
- Uncertain/excluded candidate edges: 21

## Key Precision Decisions

- Tie breakers are explicit intermediate nodes, so BUS-13K-A/B, BUS-416-A/B, and BUS-480-B/C are not directly connected.
- BUS-480-A directly feeds RECT-125A by a solid tap; HTR-PZR-01A is only on the dashed A4 control branch.
- BUS-480-C feeds RECT-125B by a separate solid route; MOV-FCV-022C and CB-48C6 do not feed that rectifier.
- BUS-125DCA feeds CP-RPS-A and CP-RPS-B; BUS-125DCB feeds CP-ESFAS-A and CP-ESFAS-B by dashed DC taps with black dots.
- ESFAS A/B interlock is only RELAY-K106--RELAY-K108; no sensor or annunciator cross-taps are visible.

## Token Usage

Expected estimated total tokens across main-agent and subagent calls: 194260. See token_usage_estimate.md and usage_estimate.json for call-level low/expected/high estimates.

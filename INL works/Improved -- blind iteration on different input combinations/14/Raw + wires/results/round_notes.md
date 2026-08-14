# Document 14 Round Notes

## Diego Round 1 - High Recall

Diego proposed all visually plausible solid source/bus/load chains, relay/control associations, panel/control associations, grounds, tie breakers, charger/UPS paths, and terminal block uncertainties. He used high-recall labels such as CB-480A-* / DS-480A-* and CB-480B-* / DS-480B-* for the 480 V branch devices.

## Jennifer Round 1 - Precision

Jennifer corrected the 480 V branch labels to the visible CB-48A-* / DS-48A-* and CB-48B-* / DS-48B-* form. She removed common-ground assumptions, master terminal block table connections, hard panel-control bundle edges, and the B-side panel-to-charger overconnection. She kept visually connected TB-to-instrument taps as hard signal/control edges.

## Diego Round 2 - Saturation

Diego agreed with Jennifer's precision graph and found no additional visually supported hard edges. He confirmed the important normalization: branch device labels use 48A/48B while bus names remain BUS-480A and BUS-480B.

## Jennifer Round 2 - Final

Jennifer confirmed saturation. Final matrix equals the Jennifer Round 1 precision graph, with TB-to-instrument taps retained as hard visual signal/control connections and relay/panel bundles retained only as uncertain associations.

# Jennifer Round 2 Precision Review

Jennifer removed the low-confidence sensing-source edges `MCC-21A--VT-21A`, `MCC-21B--VT-21B`, `MCC-21A--CT-21A`, and `MCC-21B--CT-21B` because the dashed CT/VT signal paths are visible but no terminal dot or conductor endpoint supports those direct MCC associations.

She also removed `DC-BUS-21A--RPS-PNL-A` and `DC-BUS-21B--RPS-PNL-B`; the dashed RPS terminal drops pass near or across the DC buses without a solid DC junction. `VOLTAGE-SIG-A`, `VOLTAGE-SIG-B`, `TRIP-MPA1`, and `TRIP-MPB1` were removed as matrix nodes and retained only as edge evidence/labels. Cable IDs, voltage ratings, source labels, bus-load labels, and control-lane labels were excluded as non-component text.

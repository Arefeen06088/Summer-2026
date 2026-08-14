from __future__ import annotations

import csv
import json
import shutil
from pathlib import Path


DOCUMENT = "38"
ITERATION = "1"
BASE = Path(
    r"C:\Asif_all_python_projects\INL\Improved -- blind iteration on different input combinations\38\Raw + wires + components + junctions"
)
RESULTS = BASE / "results"
CODES = BASE / "codes"

SOURCE_FILES = [
    "raw -- synthetic_npp_schematic_improved.png",
    "detected_components_and_logical_overlay.png",
    "wires_mask.png",
    "wires_mask_overlay.png",
    "wire_nodes.csv",
    "wire_nodes_overlay.png",
]


DIEGO_R1_NODES = [
    "GEN-U2A",
    "CB-101",
    "TR-UAT-2A",
    "DG-2A",
    "CB-103",
    "BUS-4160A",
    "CB-201A",
    "TR-201A",
    "CB-301A",
    "BUS-480A",
    "CB-401A",
    "MCC-2A1",
    "PUMP-RHR2A",
    "PUMP-CCW2A",
    "PUMP-SW2A",
    "FAN-CR2A",
    "MOV-RHR141A",
    "MOV-SI221A",
    "TR-CPT-A",
    "CHGR-2A",
    "BAT-125A/S-125DC-A",
    "BUS-125VDC-TRAIN-A",
    "INV-2A",
    "BUS-120AC-A",
    "RELAY-86A",
    "RELAY-27A",
    "RPS-PNL-A",
    "CB-105",
    "TR-SUT-2B",
    "CB-102",
    "BUS-4160B",
    "DG-2B",
    "CB-104",
    "CB-201B",
    "TR-201B",
    "CB-301B",
    "BUS-480B",
    "CB-401B",
    "MCC-2B1",
    "PUMP-RHR2B",
    "PUMP-CCW2B",
    "PUMP-SW2B",
    "FAN-CR2B",
    "MOV-RHR142B",
    "MOV-SI222B",
    "TR-CPT-B",
    "CHGR-2B",
    "BAT-125B/S-125DC-B",
    "BUS-125VDC-TRAIN-B",
    "INV-2B",
    "BUS-120AC-B",
    "RELAY-86B",
    "RELAY-27B",
    "RPS-PNL-B",
    "UNIT_MAIN_GENERATOR_LABEL",
    "STARTUP_AUX_XFMR_SOURCE_LABEL",
    "TO_UNIT_AUX_BUS_CONT_LABEL",
    "TO_STATION_YARD_CONT_LABEL",
    "GND-STA",
    "A_CONTROL_CABLES_2A-C72_2A-C86",
    "B_CONTROL_CABLES_2B-C72_2B-C86",
]


DIEGO_R1_EDGES = [
    ("GEN-U2A", "CB-101", "solid_power", "high", "solid line from generator symbol to CB-101"),
    ("CB-101", "TR-UAT-2A", "solid_power", "high", "solid line from CB-101 to TR-UAT-2A"),
    ("TR-UAT-2A", "BUS-4160A", "solid_power", "high", "transformer output drops to BUS-4160A"),
    ("DG-2A", "CB-103", "solid_power", "high", "solid ESF diesel A line to CB-103"),
    ("CB-103", "BUS-4160A", "solid_power", "high", "CB-103 output joins BUS-4160A vertical feeder"),
    ("BUS-4160A", "CB-105", "bus_tie_open", "high", "N.O. bus tie breaker"),
    ("CB-105", "BUS-4160B", "bus_tie_open", "high", "N.O. bus tie to BUS-4160B"),
    ("BUS-4160A", "CB-201A", "breaker_feeder", "high", "tap from 4.16 kV ESF DIV I bus"),
    ("CB-201A", "TR-201A", "transformer_feeder", "high", "vertical solid conductor through feeder transformer stack"),
    ("TR-201A", "CB-301A", "transformer_feeder", "high", "transformer low side to CB-301A"),
    ("CB-301A", "BUS-480A", "solid_power", "high", "CB-301A lands on BUS-480A"),
    ("BUS-480A", "CB-401A", "breaker_feeder", "high", "BUS-480A tap to CB-401A"),
    ("CB-401A", "MCC-2A1", "solid_power", "high", "CB-401A output drops into MCC-2A1"),
    ("MCC-2A1", "PUMP-RHR2A", "load_feeder", "high", "MCC bucket 01 / 2A-F1 solid feeder"),
    ("MCC-2A1", "PUMP-CCW2A", "load_feeder", "high", "MCC bucket 02 / 2A-F2 solid feeder"),
    ("MCC-2A1", "PUMP-SW2A", "load_feeder", "high", "MCC bucket 03 / 2A-F3 solid feeder"),
    ("MCC-2A1", "FAN-CR2A", "load_feeder", "high", "MCC bucket 04 / 2A-F4 solid feeder"),
    ("MCC-2A1", "MOV-RHR141A", "load_feeder", "high", "MCC bucket 05 / 2A-F5 solid feeder"),
    ("MCC-2A1", "MOV-SI221A", "load_feeder", "high", "MCC bucket 06 / 2A-F6 solid feeder"),
    ("BUS-480A", "TR-CPT-A", "solid_power", "high", "left BUS-480A side feeder drops to TR-CPT-A"),
    ("BUS-480A", "CHGR-2A", "solid_power", "high", "same lower left 480 feeder branches to CHGR-2A input"),
    ("CHGR-2A", "BUS-125VDC-TRAIN-A", "dc_output", "high", "charger bottom terminal lands on 125 VDC Train A"),
    ("BAT-125A/S-125DC-A", "BUS-125VDC-TRAIN-A", "dc_bus", "high", "battery symbol/terminal on 125 VDC Train A"),
    ("BUS-125VDC-TRAIN-A", "INV-2A", "dc_input", "high", "solid tap from 125 VDC Train A to inverter DC side"),
    ("INV-2A", "BUS-120AC-A", "ac_output", "high", "inverter output aligns with BUS-120AC-A"),
    ("BUS-120AC-A", "RPS-PNL-A", "solid_power", "high", "solid vertical from BUS-120AC-A to RPS-PNL-A"),
    ("BUS-125VDC-TRAIN-A", "RELAY-86A", "dashed_control", "medium", "dashed indication from 125 VDC Train A area to Relay-86A"),
    ("BUS-120AC-A", "RELAY-27A", "uv_monitor", "medium", "Relay-27A labeled UV BUS A near BUS-120AC-A"),
    ("RPS-PNL-A", "RELAY-27A", "dashed_control", "medium", "dashed control loop between RPS-PNL-A and Relay-27A"),
    ("TR-CPT-A", "BUS-120AC-A", "possible_ac_supply", "low", "functional transformer label, but visual continuity ambiguous"),
    ("TR-SUT-2B", "CB-102", "solid_power", "high", "solid line from startup aux transformer to CB-102"),
    ("CB-102", "BUS-4160B", "solid_power", "high", "CB-102 output drops to BUS-4160B"),
    ("DG-2B", "CB-104", "solid_power", "high", "solid ESF diesel B line to CB-104"),
    ("CB-104", "BUS-4160B", "solid_power", "high", "CB-104 output joins BUS-4160B vertical feeder"),
    ("BUS-4160B", "CB-201B", "breaker_feeder", "high", "tap from 4.16 kV ESF DIV II bus"),
    ("CB-201B", "TR-201B", "transformer_feeder", "high", "vertical solid conductor through feeder transformer stack"),
    ("TR-201B", "CB-301B", "transformer_feeder", "high", "transformer low side to CB-301B"),
    ("CB-301B", "BUS-480B", "solid_power", "high", "CB-301B lands on BUS-480B"),
    ("BUS-480B", "CB-401B", "breaker_feeder", "high", "BUS-480B tap to CB-401B"),
    ("CB-401B", "MCC-2B1", "solid_power", "high", "CB-401B output drops into MCC-2B1"),
    ("MCC-2B1", "PUMP-RHR2B", "load_feeder", "high", "MCC bucket 01 / 2B-F1 solid feeder"),
    ("MCC-2B1", "PUMP-CCW2B", "load_feeder", "high", "MCC bucket 02 / 2B-F2 solid feeder"),
    ("MCC-2B1", "PUMP-SW2B", "load_feeder", "high", "MCC bucket 03 / 2B-F3 solid feeder"),
    ("MCC-2B1", "FAN-CR2B", "load_feeder", "high", "MCC bucket 04 / 2B-F4 solid feeder"),
    ("MCC-2B1", "MOV-RHR142B", "load_feeder", "high", "MCC bucket 05 / 2B-F5 solid feeder"),
    ("MCC-2B1", "MOV-SI222B", "load_feeder", "high", "MCC bucket 06 / 2B-F6 solid feeder"),
    ("BUS-480B", "TR-CPT-B", "solid_power", "high", "right BUS-480B side feeder drops to TR-CPT-B"),
    ("BUS-480B", "CHGR-2B", "solid_power", "high", "same lower right 480 feeder branches to CHGR-2B input"),
    ("CHGR-2B", "BUS-125VDC-TRAIN-B", "dc_output", "high", "charger bottom terminal lands on 125 VDC Train B"),
    ("BAT-125B/S-125DC-B", "BUS-125VDC-TRAIN-B", "dc_bus", "high", "battery symbol/terminal on 125 VDC Train B"),
    ("BUS-125VDC-TRAIN-B", "INV-2B", "dc_input", "high", "solid tap from 125 VDC Train B to inverter DC side"),
    ("INV-2B", "BUS-120AC-B", "ac_output", "high", "inverter output aligns with BUS-120AC-B"),
    ("BUS-120AC-B", "RPS-PNL-B", "solid_power", "high", "solid vertical from BUS-120AC-B to RPS-PNL-B"),
    ("BUS-125VDC-TRAIN-B", "RELAY-86B", "dashed_control", "medium", "dashed/control tap from 125 VDC Train B area to Relay-86B"),
    ("BUS-120AC-B", "RELAY-27B", "uv_monitor", "medium", "Relay-27B labeled UV BUS B at BUS-120AC-B"),
    ("RPS-PNL-B", "RELAY-27B", "dashed_control", "medium", "dashed control loop between RPS-PNL-B and Relay-27B"),
    ("TR-CPT-B", "BUS-120AC-B", "possible_ac_supply", "low", "functional transformer label with visually ambiguous continuity in first pass"),
    ("UNIT_MAIN_GENERATOR_LABEL", "TR-UAT-2A", "label_context", "low", "text label above TR-UAT-2A"),
    ("STARTUP_AUX_XFMR_SOURCE_LABEL", "TR-SUT-2B", "label_context", "low", "text label above TR-SUT-2B"),
    ("TO_UNIT_AUX_BUS_CONT_LABEL", "GEN-U2A", "continuation_label", "low", "continuation box near GEN-U2A"),
    ("TO_STATION_YARD_CONT_LABEL", "BUS-4160B", "continuation_label", "low", "upper-right continuation box"),
    ("A_CONTROL_CABLES_2A-C72_2A-C86", "RPS-PNL-A", "dashed_control", "low", "dashed control cable/riser path surrounds left RPS area"),
    ("A_CONTROL_CABLES_2A-C72_2A-C86", "RELAY-27A", "dashed_control", "low", "dashed path visually reaches Relay-27A area"),
    ("A_CONTROL_CABLES_2A-C72_2A-C86", "GND-STA", "station_ground", "low", "dotted/dashed left-side path descends to GND-STA"),
    ("B_CONTROL_CABLES_2B-C72_2B-C86", "RPS-PNL-B", "dashed_control", "low", "dashed control cable/riser path surrounds right RPS area"),
    ("B_CONTROL_CABLES_2B-C72_2B-C86", "RELAY-27B", "dashed_control", "low", "dashed path visually reaches Relay-27B area"),
    ("B_CONTROL_CABLES_2B-C72_2B-C86", "RELAY-86B", "dashed_control", "low", "dashed horizontal/control line passes Relay-86B area"),
]


FINAL_NODES = [
    "GEN-U2A",
    "CB-101",
    "TR-UAT-2A",
    "DG-2A",
    "CB-103",
    "BUS-4160A",
    "CB-105",
    "TR-SUT-2B",
    "CB-102",
    "BUS-4160B",
    "DG-2B",
    "CB-104",
    "CB-201A",
    "TR-201A",
    "CB-301A",
    "BUS-480A",
    "CB-401A",
    "MCC-2A1",
    "PUMP-RHR2A",
    "PUMP-CCW2A",
    "PUMP-SW2A",
    "FAN-CR2A",
    "MOV-RHR141A",
    "MOV-SI221A",
    "TR-CPT-A",
    "CHGR-2A",
    "BAT-125A/S-125DC-A",
    "BUS-125VDC-TRAIN-A",
    "INV-2A",
    "BUS-120AC-A",
    "RELAY-86A",
    "RELAY-27A",
    "RPS-PNL-A",
    "CB-201B",
    "TR-201B",
    "CB-301B",
    "BUS-480B",
    "CB-401B",
    "MCC-2B1",
    "PUMP-RHR2B",
    "PUMP-CCW2B",
    "PUMP-SW2B",
    "FAN-CR2B",
    "MOV-RHR142B",
    "MOV-SI222B",
    "TR-CPT-B",
    "CHGR-2B",
    "BAT-125B/S-125DC-B",
    "BUS-125VDC-TRAIN-B",
    "INV-2B",
    "BUS-120AC-B",
    "RELAY-86B",
    "RELAY-27B",
    "RPS-PNL-B",
]


FINAL_EDGES = [
    ("GEN-U2A", "CB-101", "solid_power", "high", "visible solid feeder"),
    ("CB-101", "TR-UAT-2A", "solid_power", "high", "visible solid feeder"),
    ("TR-UAT-2A", "BUS-4160A", "solid_power", "high", "transformer vertical feeder to bus"),
    ("DG-2A", "CB-103", "solid_power", "high", "visible diesel feeder"),
    ("CB-103", "BUS-4160A", "solid_power", "high", "breaker output joins 4160A bus"),
    ("BUS-4160A", "CB-105", "solid_power", "high", "solid bus-tie path shown open"),
    ("CB-105", "BUS-4160B", "solid_power", "high", "solid bus-tie path shown open"),
    ("TR-SUT-2B", "CB-102", "solid_power", "high", "visible source transformer feeder"),
    ("CB-102", "BUS-4160B", "solid_power", "high", "breaker output to 4160B bus"),
    ("DG-2B", "CB-104", "solid_power", "high", "visible diesel feeder"),
    ("CB-104", "BUS-4160B", "solid_power", "high", "breaker output joins 4160B bus"),
    ("BUS-4160A", "CB-201A", "solid_power", "high", "vertical branch from 4160A bus"),
    ("CB-201A", "TR-201A", "solid_power", "high", "stacked feeder"),
    ("TR-201A", "CB-301A", "solid_power", "high", "stacked feeder"),
    ("CB-301A", "BUS-480A", "solid_power", "high", "feeder lands on 480A bus"),
    ("BUS-480A", "CB-401A", "solid_power", "high", "vertical branch from 480A bus"),
    ("CB-401A", "MCC-2A1", "solid_power", "high", "breaker feeds MCC"),
    ("BUS-480A", "TR-CPT-A", "solid_power", "high", "480A tap feeds CPT input"),
    ("BUS-480A", "CHGR-2A", "solid_power", "medium_high", "480A tap branches to charger input"),
    ("MCC-2A1", "PUMP-RHR2A", "solid_power", "high", "MCC bucket 01 feeder"),
    ("MCC-2A1", "PUMP-CCW2A", "solid_power", "high", "MCC bucket 02 feeder"),
    ("MCC-2A1", "PUMP-SW2A", "solid_power", "high", "MCC bucket 03 feeder"),
    ("MCC-2A1", "FAN-CR2A", "solid_power", "high", "MCC bucket 04 feeder"),
    ("MCC-2A1", "MOV-RHR141A", "solid_power", "high", "MCC bucket 05 feeder"),
    ("MCC-2A1", "MOV-SI221A", "solid_power", "high", "MCC bucket 06 feeder"),
    ("CHGR-2A", "BUS-125VDC-TRAIN-A", "solid_dc", "high", "charger output lands on DC train"),
    ("BAT-125A/S-125DC-A", "BUS-125VDC-TRAIN-A", "solid_dc", "high", "battery symbol terminal on train bus"),
    ("BUS-125VDC-TRAIN-A", "INV-2A", "solid_dc", "high", "vertical DC feed to inverter"),
    ("INV-2A", "BUS-120AC-A", "solid_ac", "high", "inverter output to 120AC bus"),
    ("BUS-120AC-A", "RPS-PNL-A", "solid_ac", "high", "solid vertical feed to RPS panel"),
    ("BUS-125VDC-TRAIN-A", "RELAY-86A", "dashed_control", "medium", "dashed vertical terminates at relay"),
    ("RPS-PNL-A", "RELAY-27A", "dashed_control", "medium", "dashed panel relay connection"),
    ("BUS-4160B", "CB-201B", "solid_power", "high", "vertical branch from 4160B bus"),
    ("CB-201B", "TR-201B", "solid_power", "high", "stacked feeder"),
    ("TR-201B", "CB-301B", "solid_power", "high", "stacked feeder"),
    ("CB-301B", "BUS-480B", "solid_power", "high", "feeder lands on 480B bus"),
    ("BUS-480B", "CB-401B", "solid_power", "high", "vertical branch from 480B bus"),
    ("CB-401B", "MCC-2B1", "solid_power", "high", "breaker feeds MCC"),
    ("BUS-480B", "TR-CPT-B", "solid_power", "high", "480B tap feeds CPT input"),
    ("BUS-480B", "CHGR-2B", "solid_power", "medium_high", "480B tap branches to charger input"),
    ("MCC-2B1", "PUMP-RHR2B", "solid_power", "high", "MCC bucket 01 feeder"),
    ("MCC-2B1", "PUMP-CCW2B", "solid_power", "high", "MCC bucket 02 feeder"),
    ("MCC-2B1", "PUMP-SW2B", "solid_power", "high", "MCC bucket 03 feeder"),
    ("MCC-2B1", "FAN-CR2B", "solid_power", "high", "MCC bucket 04 feeder"),
    ("MCC-2B1", "MOV-RHR142B", "solid_power", "high", "MCC bucket 05 feeder"),
    ("MCC-2B1", "MOV-SI222B", "solid_power", "high", "MCC bucket 06 feeder"),
    ("CHGR-2B", "BUS-125VDC-TRAIN-B", "solid_dc", "high", "charger output lands on DC train"),
    ("BAT-125B/S-125DC-B", "BUS-125VDC-TRAIN-B", "solid_dc", "high", "battery symbol terminal on train bus"),
    ("BUS-125VDC-TRAIN-B", "INV-2B", "solid_dc", "high", "vertical DC feed to inverter"),
    ("INV-2B", "BUS-120AC-B", "solid_ac", "high", "inverter output to 120AC bus"),
    ("TR-CPT-B", "BUS-120AC-B", "solid_ac", "high", "CPT output vertical ties to bus"),
    ("BUS-120AC-B", "RPS-PNL-B", "solid_ac", "high", "solid vertical feed to RPS panel"),
    ("BUS-125VDC-TRAIN-B", "RELAY-86B", "dashed_control", "medium", "dashed vertical terminates at relay"),
    ("BUS-120AC-B", "RELAY-27B", "solid_control", "medium_high", "relay visibly tied at 120AC bus"),
    ("RPS-PNL-B", "RELAY-27B", "dashed_control", "medium", "dashed panel relay connection"),
]


EXCLUSIONS = [
    ("UNIT_MAIN_GENERATOR_LABEL", "source/context text, not a component node"),
    ("STARTUP_AUX_XFMR_SOURCE_LABEL", "source/context text, not a component node"),
    ("TO_UNIT_AUX_BUS_CONT_LABEL", "continuation box text without a clear terminal in this sheet"),
    ("TO_STATION_YARD_CONT_LABEL", "continuation box text without a clear terminal in this sheet"),
    ("A_CONTROL_CABLES_2A-C72_2A-C86", "dashed cable path labels/callouts, not equipment nodes"),
    ("B_CONTROL_CABLES_2B-C72_2B-C86", "dashed cable path labels/callouts, not equipment nodes"),
    ("GND-STA", "station-ground reference on dotted/dashed indication; excluded from component connectivity"),
    ("TR-CPT-A--BUS-120AC-A", "A-side CPT output visually terminates and does not join BUS-120AC-A"),
    ("RELAY-86A--RPS-PNL-A", "no direct visual termination from relay to panel"),
    ("RELAY-86B--RPS-PNL-B", "no direct visual termination from relay to panel"),
    ("BUS-120AC-A--RELAY-27A", "not visibly connected; only RPS-PNL-A dashed connection retained"),
]


ROUND_DEFINITIONS = [
    {
        "round": "round_01_diego",
        "agent": "Diego",
        "role": "high-recall extractor",
        "status": "candidate graph; included low-confidence labels, cable paths, ground reference, and possible CPT output edges",
        "nodes": DIEGO_R1_NODES,
        "edges": DIEGO_R1_EDGES,
    },
    {
        "round": "round_02_jennifer",
        "agent": "Jennifer",
        "role": "precision reviewer/refiner",
        "status": "refined graph; removed label/path/ground nodes and unsupported A-side CPT output edge",
        "nodes": FINAL_NODES,
        "edges": FINAL_EDGES,
    },
    {
        "round": "round_03_diego",
        "agent": "Diego",
        "role": "convergence reviewer",
        "status": "agreed with Jennifer round 2 unchanged",
        "nodes": FINAL_NODES,
        "edges": FINAL_EDGES,
    },
    {
        "round": "round_04_jennifer_final",
        "agent": "Jennifer",
        "role": "final saturation reviewer",
        "status": "SATURATED: final graph is Jennifer round 2 unchanged",
        "nodes": FINAL_NODES,
        "edges": FINAL_EDGES,
    },
]


TOKEN_CALLS = [
    {
        "model_call": "main-01-orchestration-and-visual-prep",
        "caller": "main agent",
        "round": "prep",
        "input_tokens_est": 7200,
        "cached_input_tokens_est": 0,
        "image_file_input_tokens_est": 0,
        "output_tokens_low": 500,
        "output_tokens_expected": 950,
        "output_tokens_high": 1600,
        "reasoning_tokens_low": 900,
        "reasoning_tokens_expected": 1600,
        "reasoning_tokens_high": 2800,
        "usage_status": "not exposed by local Codex environment",
        "counting_endpoint_status": "not called; API key unavailable",
        "notes": "source inventory, crop generation, local visual triage",
    },
    {
        "model_call": "subagent-diego-01-high-recall",
        "caller": "Diego",
        "round": "round_01_diego",
        "input_tokens_est": 3300,
        "cached_input_tokens_est": 0,
        "image_file_input_tokens_est": 12000,
        "output_tokens_low": 4200,
        "output_tokens_expected": 6000,
        "output_tokens_high": 8000,
        "reasoning_tokens_low": 1300,
        "reasoning_tokens_expected": 2600,
        "reasoning_tokens_high": 4800,
        "usage_status": "response usage object not exposed",
        "counting_endpoint_status": "not called; API key unavailable",
        "notes": "high-recall extraction from raw/overlay/crops",
    },
    {
        "model_call": "subagent-jennifer-02-precision-review",
        "caller": "Jennifer",
        "round": "round_02_jennifer",
        "input_tokens_est": 7800,
        "cached_input_tokens_est": 0,
        "image_file_input_tokens_est": 9000,
        "output_tokens_low": 3300,
        "output_tokens_expected": 5000,
        "output_tokens_high": 7000,
        "reasoning_tokens_low": 1200,
        "reasoning_tokens_expected": 2300,
        "reasoning_tokens_high": 4200,
        "usage_status": "response usage object not exposed",
        "counting_endpoint_status": "not called; API key unavailable",
        "notes": "precision review and final candidate graph",
    },
    {
        "model_call": "subagent-diego-03-convergence",
        "caller": "Diego",
        "round": "round_03_diego",
        "input_tokens_est": 5200,
        "cached_input_tokens_est": 0,
        "image_file_input_tokens_est": 2500,
        "output_tokens_low": 150,
        "output_tokens_expected": 450,
        "output_tokens_high": 900,
        "reasoning_tokens_low": 500,
        "reasoning_tokens_expected": 900,
        "reasoning_tokens_high": 1700,
        "usage_status": "response usage object not exposed",
        "counting_endpoint_status": "not called; API key unavailable",
        "notes": "checked Jennifer refinements",
    },
    {
        "model_call": "subagent-jennifer-04-saturation",
        "caller": "Jennifer",
        "round": "round_04_jennifer_final",
        "input_tokens_est": 900,
        "cached_input_tokens_est": 0,
        "image_file_input_tokens_est": 0,
        "output_tokens_low": 20,
        "output_tokens_expected": 60,
        "output_tokens_high": 180,
        "reasoning_tokens_low": 50,
        "reasoning_tokens_expected": 180,
        "reasoning_tokens_high": 450,
        "usage_status": "response usage object not exposed",
        "counting_endpoint_status": "not called; API key unavailable",
        "notes": "confirmed saturated graph unchanged",
    },
    {
        "model_call": "main-02-result-writing-and-final-report",
        "caller": "main agent",
        "round": "writeup",
        "input_tokens_est": 7600,
        "cached_input_tokens_est": 0,
        "image_file_input_tokens_est": 0,
        "output_tokens_low": 650,
        "output_tokens_expected": 1200,
        "output_tokens_high": 2100,
        "reasoning_tokens_low": 800,
        "reasoning_tokens_expected": 1500,
        "reasoning_tokens_high": 2900,
        "usage_status": "not exposed by local Codex environment",
        "counting_endpoint_status": "not called; API key unavailable",
        "notes": "writes round matrices and final summary",
    },
]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def edge_pairs(edges: list[tuple[str, str, str, str, str]]) -> list[tuple[str, str]]:
    return [(a, b) for a, b, *_ in edges]


def build_matrix(nodes: list[str], edges: list[tuple[str, str]]) -> list[list[int]]:
    node_set = set(nodes)
    missing = sorted({node for edge in edges for node in edge if node not in node_set})
    if missing:
        raise ValueError(f"Edges reference missing nodes: {missing}")
    idx = {node: i for i, node in enumerate(nodes)}
    matrix = [[0 for _ in nodes] for _ in nodes]
    for a, b in edges:
        if a == b:
            matrix[idx[a]][idx[b]] = 1
        else:
            matrix[idx[a]][idx[b]] = 1
            matrix[idx[b]][idx[a]] = 1
    return matrix


def write_matrix(path: Path, nodes: list[str], edges: list[tuple[str, str]]) -> None:
    matrix = build_matrix(nodes, edges)
    for i, row in enumerate(matrix):
        if row[i] != 0:
            raise ValueError(f"Unexpected nonzero diagonal for {nodes[i]}")
        for j, value in enumerate(row):
            if value != matrix[j][i]:
                raise ValueError(f"Matrix not symmetric at {nodes[i]} / {nodes[j]}")
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["node", *nodes])
        for node, row in zip(nodes, matrix):
            writer.writerow([node, *row])


def write_edges(path: Path, edges: list[tuple[str, str, str, str, str]]) -> None:
    write_csv(
        path,
        [
            {
                "source": a,
                "target": b,
                "edge_type": edge_type,
                "confidence": confidence,
                "evidence": evidence,
            }
            for a, b, edge_type, confidence, evidence in edges
        ],
        ["source", "target", "edge_type", "confidence", "evidence"],
    )


def write_rounds() -> None:
    rows = []
    for rd in ROUND_DEFINITIONS:
        prefix = rd["round"]
        nodes = list(rd["nodes"])
        edges = list(rd["edges"])
        write_edges(RESULTS / f"{prefix}_edges.csv", edges)
        write_matrix(RESULTS / f"{prefix}_matrix.csv", nodes, edge_pairs(edges))
        write_csv(
            RESULTS / f"{prefix}_node_order.csv",
            [{"index": i, "node": node} for i, node in enumerate(nodes)],
            ["index", "node"],
        )
        rows.append(
            {
                "round": prefix,
                "agent": rd["agent"],
                "role": rd["role"],
                "node_count": len(nodes),
                "edge_count": len(edges),
                "status": rd["status"],
            }
        )
    write_csv(RESULTS / "rounds_summary.csv", rows, ["round", "agent", "role", "node_count", "edge_count", "status"])


def write_final() -> None:
    write_edges(RESULTS / "final_edges.csv", FINAL_EDGES)
    write_matrix(RESULTS / "final_connectivity_matrix.csv", FINAL_NODES, edge_pairs(FINAL_EDGES))
    write_csv(
        RESULTS / "final_node_order.csv",
        [{"index": i, "node": node} for i, node in enumerate(FINAL_NODES)],
        ["index", "node"],
    )
    write_csv(
        RESULTS / "uncertain_or_excluded_edges.csv",
        [{"item": item, "reason": reason} for item, reason in EXCLUSIONS],
        ["item", "reason"],
    )


def total_for_call(call: dict[str, object], band: str) -> int:
    return (
        int(call["input_tokens_est"])
        + int(call["image_file_input_tokens_est"])
        + int(call[f"output_tokens_{band}"])
        + int(call[f"reasoning_tokens_{band}"])
    )


def token_rows() -> list[dict[str, object]]:
    rows = []
    for call in TOKEN_CALLS:
        rows.append(
            {
                "document": DOCUMENT,
                "iteration": ITERATION,
                "round": call["round"],
                "caller": call["caller"],
                "model_call": call["model_call"],
                "input_tokens_est": call["input_tokens_est"],
                "cached_input_tokens_est": call["cached_input_tokens_est"],
                "image_file_input_tokens_est": call["image_file_input_tokens_est"],
                "output_tokens_low": call["output_tokens_low"],
                "output_tokens_expected": call["output_tokens_expected"],
                "output_tokens_high": call["output_tokens_high"],
                "reasoning_tokens_low": call["reasoning_tokens_low"],
                "reasoning_tokens_expected": call["reasoning_tokens_expected"],
                "reasoning_tokens_high": call["reasoning_tokens_high"],
                "total_tokens_low": total_for_call(call, "low"),
                "total_tokens_expected": total_for_call(call, "expected"),
                "total_tokens_high": total_for_call(call, "high"),
                "usage_status": call["usage_status"],
                "counting_endpoint_status": call["counting_endpoint_status"],
                "notes": call["notes"],
            }
        )
    return rows


def write_tokens() -> dict[str, object]:
    rows = token_rows()
    fields = [
        "document",
        "iteration",
        "round",
        "caller",
        "model_call",
        "input_tokens_est",
        "cached_input_tokens_est",
        "image_file_input_tokens_est",
        "output_tokens_low",
        "output_tokens_expected",
        "output_tokens_high",
        "reasoning_tokens_low",
        "reasoning_tokens_expected",
        "reasoning_tokens_high",
        "total_tokens_low",
        "total_tokens_expected",
        "total_tokens_high",
        "usage_status",
        "counting_endpoint_status",
        "notes",
    ]
    write_csv(RESULTS / "token_usage_estimate.csv", rows, fields)
    summary = {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "method": "local estimate because no API key was available for the OpenAI Responses input-token counting endpoint",
        "text_token_estimator": "approximate prompt/message token count from observed prompt sizes; fallback about 4 characters per token",
        "image_file_token_estimator": "standard high-detail vision tile heuristic applied qualitatively to raw/overlay/crop payloads",
        "usage_objects": "not exposed by the local Codex main/subagent tool responses",
        "calls": len(rows),
        "input_tokens_est": sum(int(r["input_tokens_est"]) for r in rows),
        "cached_input_tokens_est": sum(int(r["cached_input_tokens_est"]) for r in rows),
        "image_file_input_tokens_est": sum(int(r["image_file_input_tokens_est"]) for r in rows),
        "output_tokens_low": sum(int(r["output_tokens_low"]) for r in rows),
        "output_tokens_expected": sum(int(r["output_tokens_expected"]) for r in rows),
        "output_tokens_high": sum(int(r["output_tokens_high"]) for r in rows),
        "reasoning_tokens_low": sum(int(r["reasoning_tokens_low"]) for r in rows),
        "reasoning_tokens_expected": sum(int(r["reasoning_tokens_expected"]) for r in rows),
        "reasoning_tokens_high": sum(int(r["reasoning_tokens_high"]) for r in rows),
        "total_tokens_low": sum(int(r["total_tokens_low"]) for r in rows),
        "total_tokens_expected": sum(int(r["total_tokens_expected"]) for r in rows),
        "total_tokens_high": sum(int(r["total_tokens_high"]) for r in rows),
    }
    summary_fields = [
        "document",
        "iteration",
        "method",
        "text_token_estimator",
        "image_file_token_estimator",
        "usage_objects",
        "calls",
        "input_tokens_est",
        "cached_input_tokens_est",
        "image_file_input_tokens_est",
        "output_tokens_low",
        "output_tokens_expected",
        "output_tokens_high",
        "reasoning_tokens_low",
        "reasoning_tokens_expected",
        "reasoning_tokens_high",
        "total_tokens_low",
        "total_tokens_expected",
        "total_tokens_high",
    ]
    write_csv(RESULTS / "token_usage_summary.csv", [summary], summary_fields)
    (RESULTS / "token_usage_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def write_source_inventory() -> None:
    rows = []
    for name in SOURCE_FILES:
        path = BASE / name
        rows.append({"file": name, "exists": path.exists(), "bytes": path.stat().st_size if path.exists() else ""})
    write_csv(RESULTS / "source_inventory.csv", rows, ["file", "exists", "bytes"])


def write_report(token_summary: dict[str, object]) -> None:
    edge_lines = "\n".join(f"- {a} -- {b} ({edge_type}, {confidence})" for a, b, edge_type, confidence, _ in FINAL_EDGES)
    exclusion_lines = "\n".join(f"- {item}: {reason}" for item, reason in EXCLUSIONS)
    report = f"""# Document 38 Connectivity Extraction

## Scope

Only resources inside:

`{BASE}`

were used. No Ground Truth files, GT-derived feedback, OCR sibling folders, validation metrics, or off-the-shelf OCR outputs were used. Existing validation files in the results folder were not used as extraction evidence.

## Multi-Agent Rounds

1. Diego round 1: high-recall graph with plausible label/path/ground nodes retained.
2. Jennifer round 2: precision graph; removed label/path/ground nodes and unsupported A-side CPT output edge.
3. Diego round 3: agreed with Jennifer unchanged.
4. Jennifer round 4: confirmed saturation unchanged.

## Final Result

- Final nodes: {len(FINAL_NODES)}
- Final undirected edges: {len(FINAL_EDGES)}
- Matrix: `final_connectivity_matrix.csv`
- Edge list: `final_edges.csv`

## Final Edges

{edge_lines}

## Excluded Or Collapsed Items

{exclusion_lines}

## Token Accounting

The OpenAI Responses input-token counting endpoint was not called because no API key was available. Response `usage` objects for the main agent and subagents were not exposed by the local tooling. Token counts are therefore local low/expected/high estimates.

- Estimated total low: {token_summary["total_tokens_low"]}
- Estimated total expected: {token_summary["total_tokens_expected"]}
- Estimated total high: {token_summary["total_tokens_high"]}
- Estimated image/file input tokens: {token_summary["image_file_input_tokens_est"]}

Detailed estimates are in `token_usage_estimate.csv`; grouped totals are in `token_usage_summary.csv` and `token_usage_summary.json`.
"""
    (RESULTS / "extraction_report.md").write_text(report, encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    CODES.mkdir(parents=True, exist_ok=True)
    write_source_inventory()
    write_rounds()
    write_final()
    token_summary = write_tokens()
    write_report(token_summary)
    summary = {
        "document": DOCUMENT,
        "iteration": ITERATION,
        "base": str(BASE),
        "allowed_sources_only": True,
        "used_ground_truth": False,
        "used_ocr": False,
        "final_node_count": len(FINAL_NODES),
        "final_edge_count": len(FINAL_EDGES),
        "rounds": [
            {
                "round": rd["round"],
                "agent": rd["agent"],
                "role": rd["role"],
                "node_count": len(rd["nodes"]),
                "edge_count": len(rd["edges"]),
                "status": rd["status"],
            }
            for rd in ROUND_DEFINITIONS
        ],
        "token_summary": token_summary,
    }
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    shutil.copy2(Path(__file__), CODES / Path(__file__).name)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

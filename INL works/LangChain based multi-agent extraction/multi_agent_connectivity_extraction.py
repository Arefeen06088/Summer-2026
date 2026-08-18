"""
multi_agent_connectivity_extraction.py

Two independent LangChain agents:
    - Diego
    - Jennifer

Both agents:
    - Use the same GPT-5.1-gov-va model.
    - Receive the same diagram resources.
    - Work independently.
    - Cannot read each other's output folders.
    - Produce their own connectivity matrix.

Install:
    pip install -U langchain langchain-openai pillow

Python:
    Recommended Python 3.11+
"""

from __future__ import annotations

import base64
import csv
import json
import os
import shutil
import tomllib

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict

from typing import Dict

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

ENV_PATH = Path(
    r"C:\Users\AREFA\.codex\.env"
)

load_dotenv(ENV_PATH)


# ============================================================
# 1. THINGS YOU NEED TO CHANGE
# ============================================================

# ------------------------------------------------------------
# A. PATH TO YOUR EXISTING CONFIG FILE
# ------------------------------------------------------------

CONFIG_PATH = Path(
    r"C:\Users\AREFA\.codex\config.toml"
)


# ------------------------------------------------------------
# B. RESOURCE FOLDER
# ------------------------------------------------------------
#
# This folder contains:
#
#   raw diagram
#   component layer
#   wire layer
#   text layer
#   junction/node layer
#
# Example:
#
# C:\...\Resources\Document_1\
#     raw.png
#     component_layer.png
#     wire_layer.png
#     text_layer.png
#     junction_node_layer.png
#

RESOURCE_FOLDER = Path(
    r"C:\Asif_all_python_projects\INL\LangChain based multi-agent extraction\Resources"
)


# ------------------------------------------------------------
# C. RESULT FOLDER
# ------------------------------------------------------------

RESULTS_ROOT = Path(
    r"C:\Asif_all_python_projects\INL\LangChain based multi-agent extraction\Results"
)


# ------------------------------------------------------------
# D. RESOURCE FILENAMES
# ------------------------------------------------------------
#
# Change the filenames on the RIGHT only if your actual files
# use different names.
#

RESOURCE_FILES = {
    "raw": "raw.png",
    "component": "component_layer.png",
    "wire": "wire_layer.png",
    "text": "text_layer.png",
    "node": "junction_node_layer.png",
}




# ============================================================
# 3. AGENT NAMES
# ============================================================

AGENT_NAMES = [
    "Diego",
    "Jennifer",
]


# ============================================================
# 4. CONFIG LOADING
# ============================================================

def load_model_config() -> dict:
    """
    Load the existing TOML model configuration.

    Expected structure:

    model = "gpt-5-1-gov-va"
    model_provider = "inl-litellm"
    model_reasoning_effort = "high"

    [model_providers.inl-litellm]
    name = "INL LiteLLM"
    base_url = "https://litellm.inl.gov/v1"
    env_key = "INL_LITELLM_API_KEY"
    wire_api = "responses"
    """

    if not CONFIG_PATH.exists():
        raise FileNotFoundError(
            f"Config file does not exist:\n{CONFIG_PATH}"
        )

    with CONFIG_PATH.open("rb") as f:
        config = tomllib.load(f)

    required_top_level = [
        "model",
        "model_provider",
    ]

    for key in required_top_level:
        if key not in config:
            raise KeyError(
                f"Missing '{key}' in config file."
            )

    provider_name = config["model_provider"]

    providers = config.get(
        "model_providers",
        {}
    )

    if provider_name not in providers:
        raise KeyError(
            f"Provider '{provider_name}' was not found "
            f"under [model_providers] in the config."
        )

    provider = providers[provider_name]

    required_provider_keys = [
        "base_url",
        "env_key",
    ]

    for key in required_provider_keys:
        if key not in provider:
            raise KeyError(
                f"Missing '{key}' in provider "
                f"configuration '{provider_name}'."
            )

    return config


# ============================================================
# 5. CREATE THE LANGCHAIN MODEL
# ============================================================

def create_model() -> ChatOpenAI:
    """
    Create ChatOpenAI using values from the TOML config.
    """

    config = load_model_config()

    model_name = config["model"]

    provider_name = config[
        "model_provider"
    ]

    reasoning_effort = config.get(
        "model_reasoning_effort",
        "high"
    )

    provider = config[
        "model_providers"
    ][provider_name]

    base_url = provider[
        "base_url"
    ]

    env_key_name = provider[
        "env_key"
    ]

    wire_api = provider.get(
        "wire_api",
        "responses"
    )

    # --------------------------------------------------------
    # Actual API key is stored in the environment variable
    # named by env_key in the config.
    # --------------------------------------------------------

    api_key = os.getenv(
        env_key_name
    )

    if not api_key:
        raise RuntimeError(
            f"The environment variable "
            f"'{env_key_name}' is not set."
        )

    # --------------------------------------------------------
    # Your config explicitly specifies:
    #
    # wire_api = "responses"
    #
    # Therefore we enable LangChain's Responses API.
    # --------------------------------------------------------

    use_responses_api = (
        wire_api.lower()
        == "responses"
    )

    model = ChatOpenAI(
        model=model_name,

        api_key=api_key,

        base_url=base_url,

        use_responses_api=(
            use_responses_api
        ),

        # Recommended for Responses API output handling.
        output_version="responses/v1",

        # Useful with non-OpenAI gateways/proxies when
        # performing multi-turn tool loops.
        use_previous_response_id=True,

        # Responses API reasoning configuration.
        reasoning={
            "effort": reasoning_effort,
        },

        # Extraction benefits from deterministic behavior.
        temperature=0,

        # Network resilience.
        max_retries=3,

        timeout=600,
    )

    return model


# ============================================================
# 6. OUTPUT PATH HELPERS
# ============================================================

def agent_output_folder(
    agent_name: str,
) -> Path:

    return (
        RESULTS_ROOT
        / agent_name
    )


def agent_working_folder(
    agent_name: str,
) -> Path:

    return (
        agent_output_folder(
            agent_name
        )
        / "artifacts"
    )


# ============================================================
# 7. RESOURCE VALIDATION
# ============================================================

def resolve_resource_paths() -> Dict[str, Path]:
    """
    Verify and return all required resource paths.
    """

    if not RESOURCE_FOLDER.exists():
        raise FileNotFoundError(
            "Resource folder does not exist:\n"
            f"{RESOURCE_FOLDER}"
        )

    resources: Dict[str, Path] = {}

    for (
        resource_name,
        filename,
    ) in RESOURCE_FILES.items():

        path = (
            RESOURCE_FOLDER
            / filename
        )

        if not path.exists():
            raise FileNotFoundError(
                f"Missing required "
                f"{resource_name} file:\n"
                f"{path}"
            )

        resources[
            resource_name
        ] = path.resolve()

    return resources


# ============================================================
# 8. PATH SECURITY
# ============================================================

def is_inside(
    child: Path,
    parent: Path,
) -> bool:

    try:
        child.resolve().relative_to(
            parent.resolve()
        )
        return True

    except ValueError:
        return False


# ============================================================
# 9. IMAGE ENCODING
# ============================================================

SUPPORTED_IMAGE_FORMATS = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
}


def make_image_content(
    image_path: Path,
) -> dict:
    """
    Convert a local image to an OpenAI/LangChain multimodal
    image content block.
    """

    image_path = (
        image_path.resolve()
    )

    suffix = (
        image_path
        .suffix
        .lower()
    )

    if suffix not in (
        SUPPORTED_IMAGE_FORMATS
    ):
        raise ValueError(
            f"Unsupported image format:\n"
            f"{image_path}"
        )

    mime_type = (
        SUPPORTED_IMAGE_FORMATS[
            suffix
        ]
    )

    encoded = (
        base64.b64encode(
            image_path.read_bytes()
        )
        .decode("ascii")
    )

    return {
        "type": "image_url",
        "image_url": {
            "url": (
                f"data:{mime_type};"
                f"base64,{encoded}"
            )
        },
    }




# ============================================================
# 11. EXTRACTION PROMPT
# ============================================================

SUBAGENT_PROMPT = r"""
You are {agent_name}, an independent extractor responsible for
recovering the electrical connectivity represented in the supplied
engineering diagram.

You must perform the extraction independently.

Do not inspect, use, infer from, or access the output of any other
extractor.


RESOURCE FOLDER
===============

All available diagram resources are stored in:

{resource_folder}


The resources are:

RAW DIAGRAM:
{raw_path}

COMPONENT LAYER:
{component_path}

WIRE LAYER:
{wire_path}

TEXT LAYER:
{text_path}

JUNCTION/NODE LAYER:
{node_path}


ABOUT THE RESOURCES
===================

There are NO example diagrams or example extraction layers.

The supplied layers belong to the same raw diagram and must be used
together to infer the final electrical connectivity.


RAW DIAGRAM
===========

The raw diagram is the original engineering diagram.

Use it as the primary visual source whenever another layer is
ambiguous.


COMPONENT LAYER
===============

The component layer identifies components and busbars.

Use this layer to understand component locations and boundaries.


WIRE LAYER
==========

The wire layer traces valid wires.

Use the wire paths to determine how components, terminals, and
busbars are connected.


TEXT LAYER
==========

The text layer identifies text regions.

Use the raw diagram together with the text layer to determine
component identifiers and associate labels with the appropriate
components.


JUNCTION/NODE LAYER
===================

The junction/node layer identifies wire topology information,
including endpoints, T-junctions, and junctions.

Use this information to distinguish true electrical connections from
simple graphical crossings.


PRIMARY TASK
============

Using ALL supplied resources, reconstruct the electrical connectivity
represented by the engineering diagram.

Determine which components are directly electrically connected.

Trace wire paths carefully through:

- endpoints
- junctions
- T-junctions
- busbars
- component terminals


Do not infer connectivity merely from physical proximity.


IMPORTANT CONNECTION RULES
==========================

A valid electrical connection exists when components are connected by
a visually supported conductive path.

A graphical crossing does NOT automatically represent an electrical
connection.

Use the junction/node layer and raw diagram to determine whether
intersecting wires actually connect.

When multiple components connect to the same electrically continuous
busbar, treat them according to the actual electrical topology shown
in the diagram.

Be careful with:

- wire crossings
- true junctions
- T-junctions
- endpoints
- busbars
- multiple terminals
- closely spaced wires
- closely spaced components
- dashed graphical lines
- table borders
- title block lines
- drawing frames
- notes
- arrows
- non-electrical annotation lines


VISUAL INSPECTION
=================

You will receive five images corresponding to the same engineering
diagram:

1. Raw diagram
2. Component layer
3. Wire layer
4. Text layer
5. Junction/node layer

Inspect and compare the corresponding regions across all five images.

Use the raw diagram together with the extracted layers to understand
the complete electrical topology.


OCR RESTRICTION
===============

Do NOT use:

- TesseractOCR
- RapidOCR
- EasyOCR
- PaddleOCR
- or any other off-the-shelf OCR library.

Use the multimodal visual understanding capability of the provided
GPT model to interpret the diagram.


OUTPUT 1: CONNECTIVITY MATRIX
=============================

Create a square symmetric adjacency matrix.

Save it exactly at:

{matrix_path}

The filename MUST end with:

_matrix.csv


MATRIX FORMAT
=============

Rows:
Component identifiers.

Columns:
The identical component identifiers in the identical order.

Cell values:

1 = direct electrical connection

0 = no direct electrical connection


The diagonal should contain 0.

Example:

,COMP-A,COMP-B,COMP-C
COMP-A,0,1,0
COMP-B,1,0,1
COMP-C,0,1,0


DIRECT CONNECTIVITY
===================

Represent direct electrical connectivity rather than graph
transitive closure.

For example:

COMP-A ---- COMP-B ---- COMP-C

means:

COMP-A -> COMP-B = 1
COMP-B -> COMP-C = 1
COMP-A -> COMP-C = 0

unless COMP-A and COMP-C are actually part of the same direct
electrical node according to the source diagram.


OUTPUT 2: EDGE LIST
===================

Also create:

{edge_list_path}

Use exactly these columns:

source,target


Example:

source,target
COMP-A,COMP-B
COMP-B,COMP-C


Each undirected connection should normally appear only once in the
edge list.


OUTPUT 3: EXTRACTION NOTES
==========================

Create:

{notes_path}

Record concise notes about:

- ambiguous connections
- assumptions
- uncertain component identifiers
- difficult wire paths
- any visual uncertainty that could affect the matrix


VALIDATION
==========

Before finishing, verify:

1. Every component appears in both matrix rows and columns.

2. Row labels and column labels are identical.

3. Row and column ordering is identical.

4. The matrix is square.

5. The matrix is symmetric.

6. The diagonal contains zero.

7. All matrix entries are either 0 or 1.

8. Every connection in the edge list exists in the matrix.

9. Every matrix connection is supported by the supplied diagram
   resources.

10. You have not invented connections merely to make the electrical
    network appear complete.


OUTPUT RESTRICTIONS
===================

Your final output directory is:

{output_folder}

Your temporary working directory is:

{working_folder}

Write final deliverables only into your assigned output folder.

Write temporary artifacts only into your assigned working folder.

Do not search for or read another extractor's folder.


BLIND EXTRACTION
================

You are:

{agent_name}

Another extractor may independently perform the same task.

Your result must remain completely independent from theirs.
"""


# ============================================================
# 12. LANGCHAIN TOOLS
# ============================================================

def build_agent_tools(
    resource_folder: Path,
    working_folder: Path,
    output_folder: Path,
):

    resource_root = (
        resource_folder.resolve()
    )

    working_root = (
        working_folder.resolve()
    )

    output_root = (
        output_folder.resolve()
    )

    readable_roots = [
        resource_root,
        working_root,
        output_root,
    ]

    writable_roots = [
        working_root,
        output_root,
    ]

    @tool
    def list_resource_files() -> str:
        """
        List all files available in the shared resource folder.
        """

        records = []

        for path in sorted(
            resource_root.rglob("*")
        ):

            if path.is_file():

                records.append(
                    str(
                        path.relative_to(
                            resource_root
                        )
                    )
                )

        if not records:
            return (
                "Resource folder is empty."
            )

        return "\n".join(
            records
        )

    @tool
    def read_text_file(
        file_path: str,
    ) -> str:
        """
        Read a text, CSV, JSON, or similar plain-text file.

        Access is restricted to the shared resource folder and this
        agent's own working/output folders.
        """

        path = (
            Path(file_path)
            .resolve()
        )

        if not any(
            is_inside(
                path,
                root,
            )
            for root
            in readable_roots
        ):
            return (
                "READ DENIED: path is outside "
                "the allowed directories."
            )

        if not path.exists():
            return (
                f"File does not exist:\n"
                f"{path}"
            )

        try:

            return path.read_text(
                encoding="utf-8",
                errors="replace",
            )[:300_000]

        except Exception as exc:

            return (
                "Unable to read file:\n"
                f"{exc}"
            )

    @tool
    def write_text_file(
        file_path: str,
        content: str,
    ) -> str:
        """
        Write a CSV, TXT, JSON, or other plain-text artifact.

        Writing is restricted to this agent's working and final
        output folders.
        """

        path = (
            Path(file_path)
            .resolve()
        )

        if not any(
            is_inside(
                path,
                root,
            )
            for root
            in writable_roots
        ):
            return (
                "WRITE DENIED: path is outside "
                "the agent's assigned directories."
            )

        try:

            path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            path.write_text(
                content,
                encoding="utf-8",
            )

            return (
                "Successfully wrote:\n"
                f"{path}"
            )

        except Exception as exc:

            return (
                "Unable to write file:\n"
                f"{exc}"
            )

    @tool
    def inspect_csv(
        file_path: str,
    ) -> str:
        """
        Inspect the dimensions and first rows of a CSV created by
        this agent.
        """

        path = (
            Path(file_path)
            .resolve()
        )

        if not any(
            is_inside(
                path,
                root,
            )
            for root
            in writable_roots
        ):
            return (
                "CSV inspection denied."
            )

        if not path.exists():
            return (
                f"CSV does not exist:\n"
                f"{path}"
            )

        try:

            with path.open(
                "r",
                encoding="utf-8-sig",
                newline="",
            ) as f:

                rows = list(
                    csv.reader(f)
                )

            if not rows:
                return "CSV is empty."

            max_columns = max(
                len(row)
                for row in rows
            )

            return json.dumps(
                {
                    "path": str(path),
                    "number_of_rows": (
                        len(rows)
                    ),
                    "maximum_columns": (
                        max_columns
                    ),
                    "preview": (
                        rows[:10]
                    ),
                },
                indent=2,
            )

        except Exception as exc:

            return (
                "CSV inspection failed:\n"
                f"{exc}"
            )

    @tool
    def validate_adjacency_matrix(
        file_path: str,
    ) -> str:
        """
        Validate a binary adjacency matrix CSV created by this agent.

        Checks:
        - square matrix
        - same row and column labels
        - same ordering
        - binary values
        - symmetry
        - zero diagonal
        """

        path = (
            Path(file_path)
            .resolve()
        )

        if not any(
            is_inside(
                path,
                root,
            )
            for root
            in writable_roots
        ):
            return (
                "Matrix validation denied."
            )

        if not path.exists():
            return (
                f"Matrix does not exist:\n"
                f"{path}"
            )

        try:

            with path.open(
                "r",
                encoding="utf-8-sig",
                newline="",
            ) as f:

                rows = list(
                    csv.reader(f)
                )

            errors = []

            if len(rows) < 2:
                return json.dumps(
                    {
                        "valid": False,
                        "errors": [
                            "Matrix has insufficient rows."
                        ],
                    },
                    indent=2,
                )

            column_labels = (
                rows[0][1:]
            )

            row_labels = [
                row[0]
                for row in rows[1:]
                if row
            ]

            if (
                len(row_labels)
                != len(column_labels)
            ):
                errors.append(
                    "The matrix is not square."
                )

            if (
                row_labels
                != column_labels
            ):
                errors.append(
                    "Row and column labels differ "
                    "or use different ordering."
                )

            n = len(
                column_labels
            )

            matrix = []

            for row_index, row in enumerate(
                rows[1:]
            ):

                if len(row) != n + 1:

                    errors.append(
                        f"Row {row_index + 1} "
                        "has an incorrect number "
                        "of columns."
                    )

                    continue

                values = []

                for value in row[1:]:

                    value = value.strip()

                    if value not in {
                        "0",
                        "1",
                    }:

                        errors.append(
                            "Non-binary value found: "
                            f"{value}"
                        )

                        values.append(
                            None
                        )

                    else:

                        values.append(
                            int(value)
                        )

                matrix.append(
                    values
                )

            if (
                len(matrix) == n
                and all(
                    len(row) == n
                    for row in matrix
                )
            ):

                for i in range(n):

                    if (
                        matrix[i][i]
                        != 0
                    ):

                        errors.append(
                            "Non-zero diagonal at "
                            f"{row_labels[i]}"
                        )

                    for j in range(
                        i + 1,
                        n,
                    ):

                        if (
                            matrix[i][j]
                            != matrix[j][i]
                        ):

                            errors.append(
                                "Asymmetry found between "
                                f"{row_labels[i]} and "
                                f"{row_labels[j]}"
                            )

            return json.dumps(
                {
                    "valid": (
                        len(errors)
                        == 0
                    ),
                    "number_of_components": (
                        n
                    ),
                    "errors": (
                        errors[:100]
                    ),
                },
                indent=2,
            )

        except Exception as exc:

            return (
                "Matrix validation failed:\n"
                f"{exc}"
            )

    return [
        list_resource_files,
        read_text_file,
        write_text_file,
        inspect_csv,
        validate_adjacency_matrix,
    ]


# ============================================================
# 13. BUILD MULTIMODAL INPUT
# ============================================================

def build_multimodal_message(
    prompt: str,
    resources: Dict[str, Path],
) -> list:
    """
    Construct the multimodal message sent to each sub-agent.

    Each agent receives exactly five images:
        1. Raw diagram
        2. Component layer
        3. Wire layer
        4. Text layer
        5. Junction/node layer
    """

    content = [
        {
            "type": "text",
            "text": prompt,
        }
    ]

    labels = {
        "raw": "RAW DIAGRAM",
        "component": "COMPONENT LAYER",
        "wire": "WIRE LAYER",
        "text": "TEXT LAYER",
        "node": "JUNCTION / NODE LAYER",
    }

    layer_order = [
        "raw",
        "component",
        "wire",
        "text",
        "node",
    ]

    for layer_name in layer_order:

        image_path = resources[layer_name]

        content.append(
            {
                "type": "text",
                "text": (
                    f"\n\n=== {labels[layer_name]} ===\n"
                    f"Filename: {image_path.name}"
                ),
            }
        )

        content.append(
            make_image_content(image_path)
        )

    return content


# ============================================================
# 14. RUN ONE AGENT
# ============================================================

def run_subagent(
    agent_name: str,
    resources: Dict[str, Path],
) -> dict:

    output_folder = (
        agent_output_folder(
            agent_name
        )
    )

    working_folder = (
        agent_working_folder(
            agent_name
        )
    )

    output_folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    working_folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    # --------------------------------------------------------
    # Final files
    # --------------------------------------------------------

    matrix_path = (
        output_folder
        / f"{agent_name}_matrix.csv"
    )

    edge_list_path = (
        output_folder
        / f"{agent_name}_edges.csv"
    )

    notes_path = (
        output_folder
        / f"{agent_name}_notes.txt"
    )

    # --------------------------------------------------------
    # Fill extraction prompt
    # --------------------------------------------------------

    task_prompt = (
        SUBAGENT_PROMPT.format(
            agent_name=(
                agent_name
            ),

            resource_folder=(
                RESOURCE_FOLDER.resolve()
            ),

            raw_path=(
                resources["raw"]
            ),

            component_path=(
                resources["component"]
            ),

            wire_path=(
                resources["wire"]
            ),

            text_path=(
                resources["text"]
            ),

            node_path=(
                resources["node"]
            ),

            matrix_path=(
                matrix_path.resolve()
            ),

            edge_list_path=(
                edge_list_path.resolve()
            ),

            notes_path=(
                notes_path.resolve()
            ),

            output_folder=(
                output_folder.resolve()
            ),

            working_folder=(
                working_folder.resolve()
            ),
        )
    )

    # --------------------------------------------------------
    # System prompt
    # --------------------------------------------------------

    system_prompt = f"""
You are {agent_name}, an independent electrical connectivity
extraction sub-agent.

You are participating in a blind dual-extractor experiment.

You receive the same source resources as another extractor, but you
must work completely independently.

You may read:

1. The shared resource folder:
{RESOURCE_FOLDER.resolve()}

2. Your own output folder:
{output_folder.resolve()}

3. Your own working folder:
{working_folder.resolve()}

You must not inspect or access another extractor's directory.

Analyze the supplied images using multimodal visual reasoning.

Do not use external OCR engines.

Use the supplied tools to write the final CSV and notes files.

The extraction is not complete until the requested files physically
exist in your assigned output folder.

You MUST use the write_text_file tool to create each required output.
Do not return a final answer until all three required files have been
written successfully.

If you have determined the connectivity matrix in your reasoning,
that is not sufficient. The matrix, edge list, and notes must be
persisted to disk using the provided tools.

Before finishing, use the matrix validation tool to check your
generated connectivity matrix.
"""

    # --------------------------------------------------------
    # Create model
    # --------------------------------------------------------

    model = create_model()

    # --------------------------------------------------------
    # Create tools
    # --------------------------------------------------------

    tools = (
        build_agent_tools(
            resource_folder=(
                RESOURCE_FOLDER
            ),
            working_folder=(
                working_folder
            ),
            output_folder=(
                output_folder
            ),
        )
    )

    # --------------------------------------------------------
    # Create LangChain agent
    # --------------------------------------------------------

    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=(
            system_prompt
        ),
    )

    # --------------------------------------------------------
    # Build input
    # --------------------------------------------------------

    message_content = build_multimodal_message(
        prompt=task_prompt,
        resources=resources,
    )

    # --------------------------------------------------------
    # Execute
    # --------------------------------------------------------



    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": message_content,
                }
            ]
        }
    )

    # --------------------------------------------------------
    # Enforce required file creation
    # --------------------------------------------------------

    required_files = [
        matrix_path,
        edge_list_path,
        notes_path,
    ]

    missing_files = [
        path
        for path in required_files
        if not path.exists()
    ]

    if missing_files:

        missing_text = "\n".join(
            str(path)
            for path in missing_files
        )

        retry_message = f"""
    Your extraction is not complete.

    You returned from the previous step without creating all required
    output files.

    The following required files are still missing:

    {missing_text}

    Continue the SAME extraction task.

    Do not restart the analysis from scratch unless necessary.

    You MUST now use the available write_text_file tool to physically
    create all missing files in your assigned output directory.

    Required outputs:

    1. Connectivity matrix:
    {matrix_path}

    2. Edge list:
    {edge_list_path}

    3. Extraction notes:
    {notes_path}

    After writing the files:

    - use validate_adjacency_matrix on:
    {matrix_path}

    - correct the matrix if validation fails

    - verify that all three files physically exist

    Do not finish by merely displaying CSV content in your response.
    The files must be written to disk.
    """

        result = agent.invoke(
            {
                "messages": (
                    result["messages"]
                    + [
                        {
                            "role": "user",
                            "content": retry_message,
                        }
                    ]
                )
            }
        )

    final_message = result["messages"][-1]

    # --------------------------------------------------------
    # Verify actual files
    # --------------------------------------------------------

    return {
        "agent": (
            agent_name
        ),

        "success": (
            matrix_path.exists()
            and edge_list_path.exists()
            and notes_path.exists()
        ),

        "matrix": (
            str(matrix_path)
        ),

        "matrix_exists": (
            matrix_path.exists()
        ),

        "edge_list": (
            str(edge_list_path)
        ),

        "edge_list_exists": (
            edge_list_path.exists()
        ),

        "notes": (
            str(notes_path)
        ),

        "notes_exist": (
            notes_path.exists()
        ),

        "response": (
            str(
                final_message.content
            )
        ),
    }


# ============================================================
# 15. PREPARE CLEAN BLIND RUN
# ============================================================

def prepare_agent_directory(
    agent_name: str,
) -> None:
    """
    Delete previous output for the current iteration.

    This prevents a new extraction from accidentally inheriting
    earlier results.
    """

    folder = (
        agent_output_folder(
            agent_name
        )
    )

    if folder.exists():

        shutil.rmtree(
            folder
        )

    folder.mkdir(
        parents=True,
        exist_ok=True,
    )


# ============================================================
# 16. MAIN
# ============================================================

def main() -> None:

    print()
    print(
        "=" * 70
    )

    print(
        "MULTI-AGENT CONNECTIVITY EXTRACTION"
    )

    print(
        "=" * 70
    )

    # --------------------------------------------------------
    # Display configuration
    # --------------------------------------------------------

    config = (
        load_model_config()
    )

    provider_name = (
        config[
            "model_provider"
        ]
    )

    provider = (
        config[
            "model_providers"
        ][provider_name]
    )

    print()
    print(
        f"Model: "
        f"{config['model']}"
    )

    print(
        f"Provider: "
        f"{provider_name}"
    )

    print(
        f"Base URL: "
        f"{provider['base_url']}"
    )

    print(
        f"Wire API: "
        f"{provider.get('wire_api')}"
    )

    print(
        "Reasoning effort: "
        f"{config.get('model_reasoning_effort')}"
    )

    print(
        "API-key environment variable: "
        f"{provider['env_key']}"
    )

    # --------------------------------------------------------
    # Ensure key is available
    # --------------------------------------------------------

    env_key_name = (
        provider[
            "env_key"
        ]
    )

    if not os.getenv(
        env_key_name
    ):

        raise RuntimeError(
            "\nThe configuration is valid, but "
            f"'{env_key_name}' is not currently "
            "available as an environment variable."
        )

    # --------------------------------------------------------
    # Verify resources
    # --------------------------------------------------------

    resources = (
        resolve_resource_paths()
    )

    print()
    print(
        "Resources:"
    )

    for (
        resource_name,
        resource_path,
    ) in resources.items():

        print(
            f"  "
            f"{resource_name:<12}"
            f"{resource_path}"
        )

    # --------------------------------------------------------
    # Results folder
    # --------------------------------------------------------

    RESULTS_ROOT.mkdir(
        parents=True,
        exist_ok=True,
    )

    # --------------------------------------------------------
    # Clean previous current-iteration agent outputs
    # --------------------------------------------------------

    for agent_name in (
        AGENT_NAMES
    ):

        prepare_agent_directory(
            agent_name
        )

    # --------------------------------------------------------
    # Run both agents concurrently
    # --------------------------------------------------------

    results = []

    print()
    print(
        "Launching Diego and Jennifer..."
    )

    with ThreadPoolExecutor(
        max_workers=2
    ) as executor:

        futures = {
            executor.submit(
                run_subagent,
                agent_name,
                resources,
            ): agent_name

            for agent_name
            in AGENT_NAMES
        }

        for future in (
            as_completed(
                futures
            )
        ):

            agent_name = (
                futures[
                    future
                ]
            )

            print()
            print(
                "-" * 70
            )

            try:

                result = (
                    future.result()
                )

                results.append(
                    result
                )

                print(
                    f"{agent_name} completed."
                )

                print(
                    "Matrix exists: "
                    f"{result['matrix_exists']}"
                )

                print(
                    "Edge list exists: "
                    f"{result['edge_list_exists']}"
                )

                print(
                    "Notes exist: "
                    f"{result['notes_exist']}"
                )

                print(
                    "Matrix path:"
                )

                print(
                    result[
                        "matrix"
                    ]
                )

            except Exception as exc:

                result = {
                    "agent": (
                        agent_name
                    ),
                    "success": False,
                    "error": repr(
                        exc
                    ),
                }

                results.append(
                    result
                )

                print(
                    f"{agent_name} FAILED"
                )

                print(
                    repr(
                        exc
                    )
                )

    # --------------------------------------------------------
    # Save run summary
    # --------------------------------------------------------

    summary_path = (
        RESULTS_ROOT
        / "agent_run_summary.json"
    )

    summary_path.write_text(
        json.dumps(
            results,
            indent=2,
            default=str,
        ),
        encoding="utf-8",
    )

    print()
    print(
        "=" * 70
    )

    print(
        "FINISHED"
    )

    print(
        "=" * 70
    )

    print()
    print(
        "Summary:"
    )

    print(
        summary_path
    )


# ============================================================
# 17. ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
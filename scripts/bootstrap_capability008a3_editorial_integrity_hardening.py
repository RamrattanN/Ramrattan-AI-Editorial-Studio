#!/usr/bin/env python3
"""Bootstrap Capability 008A.3 - Editorial Integrity Hardening.

Preview changes nothing. ``--apply`` deterministically writes the bounded
editorial integrity increment and runs the complete validation suite.
``--sync-project`` reuses the approved issue and Project item.
"""

from __future__ import annotations

import argparse
import base64
import gzip
import importlib.util
import json
import subprocess
import sys
import textwrap
import time
from pathlib import Path
from typing import Any


EXPECTED_REPOSITORY = "Ramrattan-AI-Editorial-Studio"
EXPECTED_REMOTE = "RamrattanN/Ramrattan-AI-Editorial-Studio"
EXPECTED_BRANCH = "feature/capability-008a3-editorial-integrity-hardening"
REPOSITORY = "RamrattanN/Ramrattan-AI-Editorial-Studio"
OWNER = "RamrattanN"
PROJECT_NUMBER = 1
PROJECT_ID = "PVT_kwHOAuXHyM4BfHW9"
STATUS_FIELD_ID = "PVTSSF_lAHOAuXHyM4BfHW9zhZclQY"
IN_PROGRESS_OPTION_ID = "47fc9ee4"
ISSUE_TITLE = "Capability 008A.3 - Editorial Integrity Hardening"
SCRIPT_PATH = "scripts/bootstrap_capability008a3_editorial_integrity_hardening.py"
SENTINEL = "CAPABILITY_008A3_EDITORIAL_INTEGRITY_HARDENING_COMPLETE"


class CapabilityError(RuntimeError):
    """Raised when the bounded increment cannot proceed safely."""


def clean(value: str) -> str:
    """Dedent text and preserve one trailing newline."""
    return textwrap.dedent(value).strip() + "\n"


def decode(value: str) -> str:
    """Decode one deterministic gzip/base64 UTF-8 payload."""
    return gzip.decompress(base64.b64decode(value)).decode("utf-8")


EDITORIAL_INTAKE_RUNTIME = decode("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")
EDITORIAL_DISCERNMENT_RUNTIME = decode("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")
EDITORIAL_GUIDANCE_RUNTIME = decode("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")
EVIDENCE_VALIDATION_RUNTIME = decode("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")
EVIDENCE_VALIDATION_TESTS = decode("H4sIAAAAAAAAA81bbW/bOBL+nl8hCDjAXrhG072XRYF8cB11a1xqB7KTXlEUBC3RNjeypKWkpMHh/vvNUNQLJVqWG7dYf0htiRzOPPPKIWvb9ju2o488ygQNrJQlaWJtImFNaUzXPODps/X69W+W88h9FnrMuqcB92nKo3Bs2/bFxUZEewsesJTvmcX3cSRS+ftCfc9CniJZNTRJM59HxUDm8zQSnAbE54nHRLhnYTqqPeZhSh9YferYOKcg6BQvZ2EqSZUPlixJgOsDpLYZSIXyKTqDCws+1eSUbtlIPluuJr87ZD756CzrDxbuteOqBzgY/qRqBgcEcI0En+NfgCN/kwoaJhzBzF+OLoY6fwp18liirjM4DSjfj6qv8Aek3HBPjh3pQkyjcJPTa7xwefJgeOTC8uyJCfVK8XIb5RzrT13mRcLXnyEEWaI/U+YTKaIrhtJIfMuhXi7DM/Eq4ZT8jBSIIFIXFz7bWHLU4JdfvB0NtywZvi0mZCyxrqz/yp/4sXFmCuAwYb+1bDnv1aU9qgak7FuKr1Y7ZsUi2gq6B5sWzM885uMTD20o3Fpo6+P6TE/DHWgYtDFeLu7cqUMmy6XjrmaLeT7/fzV+x1mMUg4KWXLz2ai3X5rLfAXTqgloWnNyt/qwcInzn1vHnTnzqTPqHL64nc0rzt6WYxV7CUsBcpoF6cCmaSr4OpOMjAA7wGySpbtI2DnbgqWZCPNVQD05hUJphRoHCcQd0Ka1FVEWj6w+asynEE2bioymEL4nRzUeK2OG1037Hi/vbm8X7mpZG85Dn8UsRKpEcgzzcs5rJLN1wJMd84kkK/X55vWbf46sf42sy2Gdxx3zHgzjfqvGHTUOhbLuhhrc0mZMyl5hrB8U4XmMP6c0YQp51BI+J0rhhCdEIQ9EmJBBK4xS8sgEIuyTDfXSQcKCzbCyG/w5zsfPkkH5uO3mA3tiIYEMkpCMkBjU7RpahyzW7FT4AeE1Qdi3OOAeT4kXhejpKFEsGPD2yPwXMD6zonVOxEp3PAFnoNIPcEHABtVytRIZ6yFMh7cOv4e1FfBj7emztaMx2C2wBqmdeTRJ+3L0fuE608ly1QHrPk7VgoioYH8wL20D+sTTXZ11l/KEJYN7tFNHiEjUxppEAX9prqxZHvFoiOa4hgzLAskCUYk3eO7HjMu27FuNI4hqjIqQ+XabN2BJD8ZXJvTuQY3vZ841eT+Zrprst6yE0BCCQQxcg2sJ9mfGBTyrwmxTCizTdCYwHwxeYmWHpmh5QVqBjkgFaJKtMZI00dF/NmafpJJ63jHQKSUYGF/hp8oKVyU1UPLo4ASMFleyKsgzHOgw8WAaZCaKZcEmLy0hdP2R+VsZusYd5DqhMU+rBfIIcFhDzdQvhEPGvouNwe2xqMQgu7aqs4GXCYFZDvhrZqamHadPEaknxjxLJLl7Fv7b4ADCLuQUWFlnReo+aQc1INCIVYOygrBjwfdUPGMRUuRe8YpC7qiqDJtCOZ3qI9b2cHg8vOaMVoV4kheqjRq3dPReUVrRhH+iALIG6TKAo1HliAjOn5BRCyk0LWUx7iMgGWa4TXrT1KqAkRSDKHyBcVD1YnTHCFun4tWt8UcqOecCNfgEUbGpXngrYKdYf91DtyalNBWtjWko/XYCFcfk5uYzUaWic30mbVw2teFnWLvgBqhV/RaJb0/DTFZQkDQq0lhin1srrQhVKWJJYcO0lCy2/bFjnpXgxFw2q+Wn+szzea1BgS9V27HZaga6k4qTI6sBWyvAerAD5euAycJVUJ97svjuKl9/qJKVDKgmufk5olxjQrM1WQ4kS0V+feB1sXm7am3dpov5yp1cz6b13Vvx+WHmVK3ax45qAOjG0ECmZQ5ZWBqECgZ+xJJqL9aqds8Zh7PwIYyewrruR1YRk5LSVK/e0wDqkNH5wL2b13xUB6QomVV+2vME8wF4Roj5iyblRuHlwPSo+VWp3ITwfEjMFysyub29mU0n726cn1JxtMt/46rhoN4GGpU5FTbeNMwL/4bqeLhhQgpbbEzlJghMHOhRSOnPJGSgPtjWedGedTcbvnc/5DqT5WKOYJLZ/L3j9tsStXfGh0bezV1nubi5h4rtDki7q8lsvvr8A/dSp9h18THad2MlcxiuRQcMBnajNlvjM73YbltR8emwYV24frZcE65zzEsY6awYi88plWPFlO4rQB9CPraeCYQ2zHSPVT+8qAKxYdHtJacHPX1JU+eoq1qIAv+VsouRVW+OlhvLv0PlJDeWXRUiklGmdJjMGwOZ/oE3VYcRZeDVTyfGi7vV9eRQbj93yO3qa3ZK8V1Fb9FdKCTG07Ot4OnzX6LDUAxt2H5edvwU+z45xL3Q1KZ3LqShVsswylJfbsqNSBQ9Q2zCVgeGPxkf8NOezv6zHBOqErfAg1VVicCKYo8bOagRPVNxkoVdYEO1+cgTLHZ/MsKKLSPK8yg8qeo+huzdXAFbBAjtgPh4cMjbNhKgUS4rkSdTqAU8qUrwyG8T0G2i4SfPtFpnvjpygzq5BloFcR3qwwFHH6g4OnzkEURPRID8RJ7fB3ieT9KoaOh75TF7t2EobE7afp0n+lTXHlCKka7U8c3iU+/5lawj0z0DLK2vPxupoY0X9Pb0mZTuSKRBq4rTNFNuLYuptcFkHUR4ntqjCcO3ocy0YA0bHvqwAceddyvvxFTkFzdUmwdcfh/5TKD19FFtoU2jBocvUtLHxbXjgmue1Ns0qU1vcB5SIfk0W30grnM/cz4d9ossVEhBMNoDSPlaxcngjm93J8L2Mow+zH7/8OPxmTvO9ZIAMtc9Dmw12z3N7OsO09fqMfep91XiU2FqD7mIbtkYghkTbduvulBGZSa4K/8BAU6wTZbS4lKJzG99unwndZo6jWbp3DvuQbc6OQBis6ZfEDxFp7fVWGurVTWm0Pbl1eXXpnrDKKyU2mwrF0FOttPAPr5XzcUKRTfwL6v0zmh6PN/o0Pp4PUdEWQLbb5i5iyL/5R5zlsajZLPNnaw3z+w+OiSyWNpR7M+SmEH1HMqrkBCFJBN4juHx5OhmpWd+mEfSSf52KOSZb7AIedvxnFdYjJcpB8NxvtJAxtziVJ+CQ4Iig+ruaM/rWTQARWSh3EFAKolhAxCmYG07KgDgkNVvnXZfcmpeuh3X7rHW7rQeMg/jtdxTaOQlmoZgmsWwvarNO9Z2qobKyLtcTcy9tdq42ZzcuovfXWdpOCuqjZsuPt7eOCunc9C7m8X0380Fh4crplw5IQXLzG//CIi8BFXnFRbRobQcMQVSdQsZPCN/pl9fNjtLnQbofSA5GspeuvyKLXSd9uBSNtp+HVmwl/9HF1WTLqvb01+q5b52rKcRadloKeKnSDwkMYWU27qgbQIeN21Cwa9ap/BD4P0xPImAiMQj9T6RfhWwtv/0vrPkUBFwpiRMmteWmrfAB6YL4xjv3owOGG77WEVungn7BlKGSCmkcbKLyltyyQOPweBgYCGbWrppbHJtiL9mlhrjvvz6FYaaWTwdNOTxKFTqNj1ao8FX20VtXdgCDMGimLVSTyl6b/VcHuDhZMmBKQviOhTmrauHBwG47GsbqmqpICCYJCF7rLOUlLYhA9G5IVHRsWk2JoI9xPpeIm3F6IlM2fLl114m9VTEnVxqAHNPeZhgEkzBu6AKF9G+OwnLy4PYI2/8VxU9fnL5H1quGv/BpZ0C1XU4kkYx967scrwkIHv6husUVVyN1lj8YBfSdvDcFsJxKrIkBTnT3XPZdjLQkAzKbmrm57eebe1uZH4snBhm1ovqbQT7heL6j0VDC3swXtBccHjR/qaQHGM39xGRrrmeriVZUOaDG29axADLB2VOfWxRtyTzGqMmO1gH8o1FZCFAiHV1ZdmEoB0RYueWUtaB+BQE+z+bPVJ3uDUAAA==")
ADR_013 = decode("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")
ARCHITECTURE_BASELINE_V08 = decode("H4sIAAAAAAAAA21WTVPkNhC961eoiqtxZqEqy3UCbKAqCRTskiPIcttWsCVHkmeY/fV5LXkMM+SyO+iru997/doncu11ZyLpOHmSv6lAvbEkT+XZ6uzXcnVRrr5sVhdCnJzIx6jiFIS4nLwnGyXVJjpvVC+NjdR6E3ey2j+w7cjKSzWqyvS8sVpdrMtzaYKscWBDnuoyvbqEvL0S4uUg6ksOO43kA9UUjva/5v0HUsFZ2TiPnxsTjLNC3A5jTwNn+TmHU3m9ZH67ZH6jfE3W2FZOtiYv11cPp6sv5znJ643BpqYDtIR4Im8aQ7X8pnTk2pSVpLzFymWvzLAOgUJIaehehYDDWkUkWMq11KrvEUcra10UAIH4jShVesZYEznB9M6n23e230klH93kOSmE8bwhtyZ2UkXRA5Mo49bJluwEdHG8NiEaq2MhNcA3VU8yTOPocBNFh/QUh66ldcsRoZ2NXtVGp/cHtUsFIk8As55iB9Sv30CQSfDw7bsRueOsp38nA03Vk1ccTMXoTTXlAjJpvC5ubQM14HYhvzlPGpkX6aEf1lNw/Yb4p0aFCjrbyRGr5DckY0fGy0CDstFocYiRpA0EmFRowOdI+MdGwDDXnOR36bx3lfP5RtJmPY09P4Gg1Q5I+EH15if+ygBJ1kFMSicojj4+LlrvphEQYlm7yXIMebnH+gDIfGhfSc2b/At5bEDVrLlFpA8mvB4p709kmPb+59lH4vYq5R9uKz1f5TPALjCxKh1MhDTIHdSX4sa0XUI838yXAsUk5zfGA7Icp6rfY1v1Tr9Cw4n/00ZpVtCSL2C1zdwv+xID2FIxX5TAu4PysWIBaxNz2yEG+EWG46jYX4Qn1GXRQOXeftrjBnwJcaqNKxcrem4nUytEfmE6EYb7y1kk3ku3tYjqmvdM05OFSP+xu0GCIUVx8AJfHBWYt6waKGSBQvaDiSwVUGCDSRSU4sBd1GvuivfFKxMgZptcIXRMWIKG3thDPGRjBsoNnxTKRsYhUvTANjcwLylDLAPgxrwV0rEjONhozpIbtWJ14oBrQUIoRM+a2b+TbYf/8pFbut/lmvRxwPmgJweZl+Jv51/DqEBtAgzrQ5LW3l3SI4alBs8DwW1uJDXn9Q5UJvV3Aiep2+6YndCZkVnV3owx/FI5FwOujM96cXGYuDp/fid8mT3P3d7By3H3wmwnAYi8jAgztgUw1FNg1ihEUAmnL5bBNaOQR9xpSCMPvaBnbr9DUQcT5etMcnE0aD7SnN883BfLSFmKTKORWkY1W5tqGgROiYIUrKMgl0Q9T7JF22I5kWFFB4KOmMyWdTiAsSjEX0423v2EJ+rDA35ih0p0hVJ+70DgMskHVBdgp3O6ixEX4pMlAPvig9LffSAjkCVQUac2BnNjYP9sFEZWM6GCXBm9JSG1ByXM+O0b+clpVU298rNTXhEmCDfDo4ZIMZcw0jQKurZtYvT+Q573Sr9y00vuLPQLfyG4vlf7KVDIG/JOPpkwqb4Q9xgVySzvvfuHeHjClfiDB0Dl4z9ueY0HLtwuPZ5QgDdwq7IVyS16JiHAHwz8fSLPeC6z8AEDU+F6uFbMU5P7Cd8gc/OU4j972zrDowkAAA==")


ROADMAP_BLOCK = clean(
    """
    ## Capability 008A.3 - Editorial Integrity Hardening

    Status: **In Progress**

    Current authoritative sequence:

    - Capability 008 - Complete
    - Capability 008A.1 - Governance Consolidation - Complete
    - Capability 008A.2 - Delivery Hardening - Complete
    - Capability 008A.3 - Editorial Integrity Hardening - In Progress
    - Capability 009 - Todo

    Capability 008A.3 makes Verified Fact earned, preserves semantic claim
    classifications and attribution, deduplicates corroboration by source identity,
    aligns contradiction and publication-blocking risk, and establishes one
    canonical StageState across affected runtime components.

    ADR-013 records Editorial Integrity Hardening. Architecture Baseline
    `2026.08.01v08` records the resulting product architecture and becomes current
    when this increment is delivered. Capability 009 remains Todo.

    Earlier status sections are historical delivery records; this section owns the
    active increment.
    """
)

SCORECARD_BLOCK = clean(
    """
    ## Capability 008A Editorial Integrity Hardening Status

    - Capability 008A.1 - Complete
    - Capability 008A.2 - Complete
    - Capability 008A.3 - In Progress
    - Capability 009 - Todo

    | Editorial integrity area | Status | Evidence |
    |---|---|---|
    | Earned Verified Fact | Complete | Claim transition tests |
    | Durable Author attribution | Complete | Classification contract tests |
    | Distinct-source corroboration | Complete | Duplicate identity tests |
    | Semantic classification preservation | Complete | Inference, forecast, and uncertainty tests |
    | Contradiction severity | Complete | Material and non-material risk tests |
    | Publication blocking | Complete | High and Severe gate tests |
    | Editorial Confidence translation | Complete | Author-message tests |
    | Canonical StageState | Complete | Cross-component identity and transition tests |
    | Editorial architecture | Complete | ADR-013 and baseline v08 |

    Capability 008A.3 hardens existing Version 1.0 editorial behavior. It does not
    begin the Article Engine, Publication Package, or any Capability 009 scope.
    """
)

CURRENT_FOCUS_BLOCK = clean(
    """
    ## Current Engineering Hardening Increment - Capability 008A.3

    Capability 008A.1 Governance Consolidation and Capability 008A.2 Delivery
    Hardening are complete. Capability 008A.3 Editorial Integrity Hardening is in
    progress. Capability 009 remains Todo and has not started.

    This increment corrects evidence certainty, source independence,
    contradiction-to-risk behavior, publication blocking, Author-facing Editorial
    Confidence translation, and canonical StageState ownership. It does not add an
    Article Engine, Publication Package, Component Collaboration, Hero Visual,
    Portable Project, real ingestion, UI, or release behavior.

    ADR-013 records the durable decision. Architecture Baseline
    `2026.08.01v08` becomes current when Capability 008A.3 is delivered; baseline
    `2026.08.01v07` remains the merged baseline during implementation.
    """
)

ISSUE_BODY = clean(
    """
    ## Objective

    Correct Evidence Validation semantics, strengthen corroboration and editorial
    risk behavior, and replace duplicated workflow-stage representations with one
    canonical StageState model.

    ## Architecture

    - ADR-013 required
    - Architecture Baseline 2026.08.01v08 required

    ## Budget

    Hard limit: approximately 10-15 files.
    """
)

PROJECT_README = clean(
    """
    # Ramrattan AI Editorial Studio

    ## Governing principle

    Trust is our most valuable feature.

    ## Current implementation

    - Capabilities 001-008 - Complete
    - Capability 008A.1 - Governance Consolidation - Complete
    - Capability 008A.2 - Delivery Hardening - Complete
    - Capability 008A.3 - Editorial Integrity Hardening - In Progress
    - Capability 009 - Article Engine and Publication Package - Todo

    ## Current architecture baseline

    2026.08.01v07

    ## Active engineering hardening increment

    Capability 008A.3 corrects Evidence Validation semantics, strengthens
    editorial risk and Editorial Confidence behavior, and establishes one
    canonical StageState under ADR-013.

    Capability 009 remains Todo and has not started. Architecture Baseline
    2026.08.01v08 becomes current only when Editorial Integrity Hardening is
    delivered.

    ## Program sequence

    Capability 008A.1 is complete.
    Capability 008A.2 is complete.
    Capability 008A.3 is in progress.
    Capability 009 begins only after the complete Capability 008A program.
    """
)

FULL_FILES = {
    "studio/editorial_intake.py": EDITORIAL_INTAKE_RUNTIME,
    "studio/editorial_discernment.py": EDITORIAL_DISCERNMENT_RUNTIME,
    "studio/editorial_guidance.py": EDITORIAL_GUIDANCE_RUNTIME,
    "studio/evidence_validation.py": EVIDENCE_VALIDATION_RUNTIME,
    "tests/test_capability008_evidence_validation.py": EVIDENCE_VALIDATION_TESTS,
    "docs/architecture/adr/ADR-013-editorial-integrity-hardening.md": ADR_013,
    (
        "docs/architecture/baselines/"
        "Architecture_Baseline_2026.08.01v08.md"
    ): ARCHITECTURE_BASELINE_V08,
}

MARKER_BLOCKS = {
    "ROADMAP.md": ("CAPABILITY_008A3_ROADMAP", ROADMAP_BLOCK),
    "docs/VERSION_ONE_SCORECARD.md": (
        "CAPABILITY_008A3_SCORECARD",
        SCORECARD_BLOCK,
    ),
    "docs/product/Current_Product_Focus.md": (
        "CAPABILITY_008A3_CURRENT_FOCUS",
        CURRENT_FOCUS_BLOCK,
    ),
}

GENERATOR_OVERRIDES = {
    "scripts/bootstrap_capability007_editorial_intake.py": clean(
        """
        # CAPABILITY_008A3_GENERATOR_OVERRIDE_START
        from bootstrap_capability008a3_editorial_integrity_hardening import (
            EDITORIAL_INTAKE_RUNTIME as CAPABILITY_008A3_EDITORIAL_INTAKE_RUNTIME,
        )
        NEW_FILES["studio/editorial_intake.py"] = (
            CAPABILITY_008A3_EDITORIAL_INTAKE_RUNTIME
        )
        # CAPABILITY_008A3_GENERATOR_OVERRIDE_END
        """
    ),
    "scripts/bootstrap_capability008_editorial_discernment.py": clean(
        """
        # CAPABILITY_008A3_GENERATOR_OVERRIDE_START
        from bootstrap_capability008a3_editorial_integrity_hardening import (
            EDITORIAL_DISCERNMENT_RUNTIME as CAPABILITY_008A3_DISCERNMENT_RUNTIME,
            EDITORIAL_GUIDANCE_RUNTIME as CAPABILITY_008A3_GUIDANCE_RUNTIME,
        )
        NEW_FILES["studio/editorial_discernment.py"] = (
            CAPABILITY_008A3_DISCERNMENT_RUNTIME
        )
        NEW_FILES["studio/editorial_guidance.py"] = (
            CAPABILITY_008A3_GUIDANCE_RUNTIME
        )
        # CAPABILITY_008A3_GENERATOR_OVERRIDE_END
        """
    ),
    "scripts/bootstrap_capability008_evidence_validation.py": clean(
        """
        # CAPABILITY_008A3_GENERATOR_OVERRIDE_START
        from bootstrap_capability008a3_editorial_integrity_hardening import (
            EVIDENCE_VALIDATION_RUNTIME as CAPABILITY_008A3_EVIDENCE_RUNTIME,
            EVIDENCE_VALIDATION_TESTS as CAPABILITY_008A3_EVIDENCE_TESTS,
        )
        FILES["studio/evidence_validation.py"] = (
            CAPABILITY_008A3_EVIDENCE_RUNTIME
        )
        FILES["tests/test_capability008_evidence_validation.py"] = (
            CAPABILITY_008A3_EVIDENCE_TESTS
        )
        # CAPABILITY_008A3_GENERATOR_OVERRIDE_END
        """
    ),
}

ADR_INDEX = "docs/architecture/adr/README.md"
ADR_INDEX_LINE = (
    "- [ADR-013 - Editorial Integrity Hardening]"
    "(ADR-013-editorial-integrity-hardening.md)"
)

EXPECTED_PATHS = {
    SCRIPT_PATH,
    *FULL_FILES,
    *MARKER_BLOCKS,
    *GENERATOR_OVERRIDES,
    ADR_INDEX,
}


def run(
    command: list[str],
    *,
    cwd: Path,
    capture: bool = False,
) -> subprocess.CompletedProcess[str]:
    """Run one exact command."""
    print("$", " ".join(command))
    result = subprocess.run(
        command,
        cwd=cwd,
        check=True,
        text=True,
        capture_output=capture,
    )
    if capture and result.stdout:
        print(result.stdout.rstrip())
    return result


def json_output(command: list[str], *, cwd: Path) -> Any:
    """Run a command and parse one JSON response."""
    result = run(command, cwd=cwd, capture=True)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise CapabilityError("GitHub returned malformed JSON.") from exc


def repository_root() -> Path:
    """Resolve and verify repository identity."""
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=True,
        text=True,
        capture_output=True,
    )
    root = Path(result.stdout.strip())
    if root.name != EXPECTED_REPOSITORY:
        raise CapabilityError(f"Unexpected repository: {root}")
    remote = run(["git", "remote", "get-url", "origin"], cwd=root, capture=True)
    if EXPECTED_REMOTE not in remote.stdout:
        raise CapabilityError("Unexpected origin remote.")
    return root


def verify_branch(root: Path) -> None:
    """Require the dedicated increment branch."""
    branch = run(["git", "branch", "--show-current"], cwd=root, capture=True)
    if branch.stdout.strip() != EXPECTED_BRANCH:
        raise CapabilityError(f"Expected branch {EXPECTED_BRANCH}.")


def verify_integrity() -> None:
    """Require the bootstrap sentinel."""
    if SENTINEL not in Path(__file__).read_text(encoding="utf-8"):
        raise CapabilityError("Bootstrap integrity sentinel is missing.")


def verify_working_tree(root: Path) -> None:
    """Permit only this increment's declared partial-apply paths."""
    result = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        cwd=root,
        check=True,
        text=True,
        capture_output=True,
    )
    observed: set[str] = set()
    for line in result.stdout.splitlines():
        if len(line) < 4:
            raise CapabilityError(f"Malformed Git status line: {line!r}")
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        observed.add(path)
    unexpected = observed - EXPECTED_PATHS
    if unexpected:
        raise CapabilityError(
            "Unexpected working-tree paths: " + ", ".join(sorted(unexpected))
        )
    print("Working tree contains only expected Capability 008A.3 paths.")


def managed_block(marker: str, content: str) -> str:
    return f"<!-- {marker}_START -->\n\n{content.rstrip()}\n\n<!-- {marker}_END -->"


def upsert_markdown(path: Path, marker: str, content: str) -> None:
    """Insert or replace one deterministic Markdown block."""
    original = path.read_text(encoding="utf-8")
    start = f"<!-- {marker}_START -->"
    end = f"<!-- {marker}_END -->"
    if (start in original) != (end in original):
        raise CapabilityError(f"Incomplete marker pair in {path}.")
    block = managed_block(marker, content)
    if start in original:
        before, remainder = original.split(start, 1)
        _, after = remainder.split(end, 1)
        updated = before.rstrip() + "\n\n" + block
        if after.strip():
            updated += "\n\n" + after.strip()
    else:
        updated = original.rstrip() + "\n\n" + block
    path.write_text(updated.rstrip() + "\n", encoding="utf-8")


def upsert_python_override(path: Path, content: str) -> None:
    """Insert or replace one owning-generator delegation block."""
    original = path.read_text(encoding="utf-8")
    start = "# CAPABILITY_008A3_GENERATOR_OVERRIDE_START"
    end = "# CAPABILITY_008A3_GENERATOR_OVERRIDE_END"
    if (start in original) != (end in original):
        raise CapabilityError(f"Incomplete generator override in {path}.")
    if start in original:
        before, remainder = original.split(start, 1)
        _, after = remainder.split(end, 1)
        updated = before.rstrip() + "\n\n" + content.rstrip()
        if after.strip():
            updated += "\n\n" + after.strip()
    else:
        anchor = '\nif __name__ == "__main__":'
        if anchor not in original:
            raise CapabilityError(f"Generator main anchor is missing in {path}.")
        updated = original.replace(
            anchor,
            "\n\n" + content.rstrip() + "\n" + anchor,
            1,
        )
    path.write_text(updated.rstrip() + "\n", encoding="utf-8")


def ensure_adr_index(path: Path) -> None:
    """Ensure ADR-013 is indexed once."""
    content = path.read_text(encoding="utf-8")
    if ADR_INDEX_LINE not in content:
        prior = "- [ADR-012 - Delivery Hardening](ADR-012-delivery-hardening.md)"
        if prior not in content:
            raise CapabilityError("ADR-012 index anchor is missing.")
        content = content.replace(prior, prior + "\n" + ADR_INDEX_LINE, 1)
        path.write_text(content, encoding="utf-8")


def apply_files(root: Path) -> None:
    """Write all generated and managed artifacts deterministically."""
    for relative, content in FULL_FILES.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"Wrote {relative}")
    for relative, (marker, content) in MARKER_BLOCKS.items():
        upsert_markdown(root / relative, marker, content)
        print(f"Updated {relative}")
    for relative, content in GENERATOR_OVERRIDES.items():
        upsert_python_override(root / relative, content)
        print(f"Synchronized {relative}")
    ensure_adr_index(root / ADR_INDEX)
    print(f"Updated {ADR_INDEX}")


def load_generator(root: Path, relative: str, name: str) -> Any:
    """Load one owning generator for parity inspection."""
    scripts_path = str(root / "scripts")
    if scripts_path not in sys.path:
        sys.path.insert(0, scripts_path)
    spec = importlib.util.spec_from_file_location(name, root / relative)
    if spec is None or spec.loader is None:
        raise CapabilityError(f"Cannot load owning generator {relative}.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_generated_files(root: Path) -> None:
    """Prove artifacts, markers, and all owning generators agree."""
    for relative, expected in FULL_FILES.items():
        if (root / relative).read_text(encoding="utf-8") != expected:
            raise CapabilityError(f"Generated artifact differs: {relative}")
    for relative, (marker, content) in MARKER_BLOCKS.items():
        expected = managed_block(marker, content)
        if expected not in (root / relative).read_text(encoding="utf-8"):
            raise CapabilityError(f"Managed status block differs: {relative}")
    for relative, override in GENERATOR_OVERRIDES.items():
        if override.strip() not in (root / relative).read_text(encoding="utf-8"):
            raise CapabilityError(f"Owning generator is stale: {relative}")
    if ADR_INDEX_LINE not in (root / ADR_INDEX).read_text(encoding="utf-8"):
        raise CapabilityError("ADR-013 is absent from the ADR index.")

    intake = load_generator(
        root,
        "scripts/bootstrap_capability007_editorial_intake.py",
        "capability007_generator_check",
    )
    discernment = load_generator(
        root,
        "scripts/bootstrap_capability008_editorial_discernment.py",
        "capability008_discernment_generator_check",
    )
    evidence = load_generator(
        root,
        "scripts/bootstrap_capability008_evidence_validation.py",
        "capability008_evidence_generator_check",
    )
    checks = (
        (intake.NEW_FILES["studio/editorial_intake.py"], EDITORIAL_INTAKE_RUNTIME),
        (
            discernment.NEW_FILES["studio/editorial_discernment.py"],
            EDITORIAL_DISCERNMENT_RUNTIME,
        ),
        (
            discernment.NEW_FILES["studio/editorial_guidance.py"],
            EDITORIAL_GUIDANCE_RUNTIME,
        ),
        (evidence.FILES["studio/evidence_validation.py"], EVIDENCE_VALIDATION_RUNTIME),
        (
            evidence.FILES["tests/test_capability008_evidence_validation.py"],
            EVIDENCE_VALIDATION_TESTS,
        ),
    )
    if any(actual != expected for actual, expected in checks):
        raise CapabilityError("An owning generator differs from 008A.3.")
    print("Runtime, tests, and all owning generators are synchronized.")


def run_validation(root: Path) -> None:
    """Run the canonical repository suite."""
    run([sys.executable, "-m", "compileall", "-q", "studio", "scripts", "tests"], cwd=root)
    run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        cwd=root,
    )
    run([sys.executable, "studio.py", "validate"], cwd=root)
    print("Capability 008A.3 repository validation passed.")


def preview() -> None:
    """Describe the bounded deterministic increment."""
    print("\nCapability 008A.3 preview:\n")
    print("Generated files:")
    for relative in FULL_FILES:
        print(f"  - {relative}")
    print("\nManaged updates:")
    for relative in (*MARKER_BLOCKS, *GENERATOR_OVERRIDES, ADR_INDEX):
        print(f"  - {relative}")
    print("\nDecisions:")
    for decision in (
        "Make Verified Fact earned",
        "Preserve attributed experience, opinion, inference, forecast, and uncertainty",
        "Deduplicate corroboration by normalized source identity",
        "Make material contradictions Severe and keep Low action-free",
        "Block publication for High and Severe risk",
        "Preserve blocking conditions in Editorial Confidence",
        "Canonicalize StageState, stage order, names, and transitions",
        "Create ADR-013 and Architecture Baseline 2026.08.01v08",
    ):
        print(f"  - {decision}")
    print("\nPreview mode changes nothing.")


def issue_list(root: Path) -> list[dict[str, Any]]:
    payload = json_output(
        [
            "gh", "issue", "list", "--repo", REPOSITORY, "--state", "all",
            "--limit", "300", "--json", "number,title,url,state",
        ],
        cwd=root,
    )
    if not isinstance(payload, list):
        raise CapabilityError("Issue response is malformed.")
    return payload


def ensure_issue(root: Path) -> dict[str, Any]:
    matches = [item for item in issue_list(root) if item.get("title") == ISSUE_TITLE]
    if len(matches) > 1:
        raise CapabilityError("Multiple Capability 008A.3 issues exist.")
    if matches:
        if matches[0].get("state") != "OPEN":
            raise CapabilityError("Capability 008A.3 issue is not open.")
        return matches[0]
    run(
        [
            "gh", "issue", "create", "--repo", REPOSITORY,
            "--title", ISSUE_TITLE, "--body", ISSUE_BODY,
        ],
        cwd=root,
    )
    for _ in range(5):
        matches = [item for item in issue_list(root) if item.get("title") == ISSUE_TITLE]
        if len(matches) == 1:
            return matches[0]
        time.sleep(2)
    raise CapabilityError("Created issue could not be resolved.")


def project_items(root: Path) -> list[dict[str, Any]]:
    payload = json_output(
        [
            "gh", "project", "item-list", str(PROJECT_NUMBER), "--owner", OWNER,
            "--limit", "300", "--format", "json",
        ],
        cwd=root,
    )
    if not isinstance(payload, dict) or not isinstance(payload.get("items"), list):
        raise CapabilityError("Project item response is malformed.")
    return payload["items"]


def ensure_project_item(root: Path, issue: dict[str, Any]) -> dict[str, Any]:
    def matches() -> list[dict[str, Any]]:
        return [
            item for item in project_items(root)
            if (item.get("content") or {}).get("url") == issue.get("url")
        ]

    found = matches()
    if len(found) > 1:
        raise CapabilityError("Multiple Project items reference Capability 008A.3.")
    if found:
        return found[0]
    run(
        [
            "gh", "project", "item-add", str(PROJECT_NUMBER), "--owner", OWNER,
            "--url", str(issue["url"]),
        ],
        cwd=root,
    )
    for _ in range(10):
        found = matches()
        if len(found) == 1:
            return found[0]
        time.sleep(2)
    raise CapabilityError("Project item did not become visible.")


def sync_project(root: Path) -> None:
    """Reuse and verify approved 008A.3 planning state."""
    validate_generated_files(root)
    run_validation(root)
    run(["gh", "auth", "status"], cwd=root)
    project = json_output(
        ["gh", "project", "view", str(PROJECT_NUMBER), "--owner", OWNER, "--format", "json"],
        cwd=root,
    )
    if not isinstance(project, dict) or project.get("id") != PROJECT_ID:
        raise CapabilityError("GitHub Project identity is unavailable or unexpected.")
    issue = ensure_issue(root)
    item = ensure_project_item(root, issue)
    run(
        [
            "gh", "project", "item-edit", "--id", str(item["id"]),
            "--project-id", PROJECT_ID, "--field-id", STATUS_FIELD_ID,
            "--single-select-option-id", IN_PROGRESS_OPTION_ID,
        ],
        cwd=root,
    )
    items = project_items(root)
    capability_009 = [
        entry for entry in items
        if entry.get("title", "").startswith("Capability 009")
    ]
    if len(capability_009) != 1 or capability_009[0].get("status") != "Todo":
        raise CapabilityError("Capability 009 is not uniquely verified Todo.")
    run(
        [
            "gh", "project", "edit", str(PROJECT_NUMBER), "--owner", OWNER,
            "--readme", PROJECT_README,
        ],
        cwd=root,
    )
    print(f"GitHub planning synchronized with issue #{issue['number']} In Progress.")


def show_status(root: Path) -> None:
    run(["git", "status", "--short"], cwd=root)
    run(["git", "diff", "--stat"], cwd=root)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Bootstrap Capability 008A.3 Editorial Integrity Hardening."
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--sync-project", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        root = repository_root()
        verify_integrity()
        verify_branch(root)
        verify_working_tree(root)
        if args.sync_project:
            sync_project(root)
        elif args.apply:
            apply_files(root)
            validate_generated_files(root)
            run_validation(root)
            show_status(root)
        else:
            preview()
        return 0
    except (
        CapabilityError,
        subprocess.CalledProcessError,
        UnicodeError,
        ValueError,
    ) as exc:
        print(f"\nERROR: {exc}", file=sys.stderr)
        return 1


# CAPABILITY_008A3_EDITORIAL_INTEGRITY_HARDENING_COMPLETE


if __name__ == "__main__":
    raise SystemExit(main())

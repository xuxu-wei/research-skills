#!/usr/bin/env python3
"""Materialize one exact, index-declared Preview evidence subset."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from validate_openai_preview_accepted_phase78 import (
    AcceptedPhase78Error,
    materialize_evidence_subset,
)


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--source-root", required=True)
    value.add_argument("--destination-root", required=True)
    value.add_argument("--asset-index-pattern", required=True)
    value.add_argument("--expected-index-count", required=True, type=int)
    return value


def main(argv: Sequence[str] | None = None) -> int:
    try:
        args = parser().parse_args(argv)
        inventory = materialize_evidence_subset(
            source_root=Path(args.source_root),
            destination_root=Path(args.destination_root),
            asset_index_pattern=args.asset_index_pattern,
            expected_index_count=args.expected_index_count,
        )
        output = {
            "schema_version": "openai-preview-evidence-subset/v1",
            "materialized": True,
            "asset_index_count": args.expected_index_count,
            "file_count": len(inventory),
            "inventory": inventory,
        }
        code = 0
    except (OSError, ValueError, AcceptedPhase78Error) as exc:
        output = {
            "schema_version": "openai-preview-evidence-subset/v1",
            "materialized": False,
            "error": f"{type(exc).__name__}: {exc}",
        }
        code = 1
    print(json.dumps(output, ensure_ascii=False, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())

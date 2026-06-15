#!/usr/bin/env python3
"""Inspect a document package before format-preserving translation."""

from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path

from ooxml_common import detect_format, is_media_or_embedding, iter_parts, iter_text_nodes, read_xml


def inspect(source: Path):
    suffix = detect_format(source)
    text_parts = list(iter_parts(source, suffix))
    segment_count = 0
    parse_warnings = []
    with zipfile.ZipFile(source) as zf:
        names = zf.namelist()
        media_parts = [name for name in names if is_media_or_embedding(name)]
        for part in text_parts:
            root = read_xml(zf, part)
            if root is None:
                parse_warnings.append(f"Could not parse {part}")
                continue
            segment_count += sum(1 for _ in iter_text_nodes(root, suffix))

    return {
        "path": str(source),
        "format": suffix.lstrip("."),
        "text_parts": text_parts,
        "media_or_embedding_parts": media_parts,
        "translatable_segment_count": segment_count,
        "warnings": parse_warnings,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Source .docx, .pptx, or .xlsx file")
    parser.add_argument("--report", type=Path, help="Optional JSON report path")
    args = parser.parse_args(argv)

    report = inspect(args.source)
    output = json.dumps(report, ensure_ascii=False, indent=2)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output + "\n", encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())

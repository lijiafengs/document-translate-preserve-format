#!/usr/bin/env python3
"""Validate that non-text OOXML package assets remained unchanged."""

from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path

from ooxml_common import detect_format, is_media_or_embedding, is_text_part, sha256


def validate(source: Path, target: Path):
    suffix = detect_format(source)
    with zipfile.ZipFile(source) as a, zipfile.ZipFile(target) as b:
        source_names = set(a.namelist())
        target_names = set(b.namelist())
        missing = sorted(source_names - target_names)
        added = sorted(target_names - source_names)
        changed_media = []
        changed_non_text_xml = []
        changed_other = []

        for name in sorted(source_names & target_names):
            left = a.read(name)
            right = b.read(name)
            if left == right:
                continue
            if is_media_or_embedding(name):
                changed_media.append(name)
            elif name.endswith(".xml") and not is_text_part(name, suffix):
                changed_non_text_xml.append(name)
            elif not is_text_part(name, suffix):
                changed_other.append(name)

        report = {
            "ok": not (missing or added or changed_media or changed_non_text_xml or changed_other),
            "entries": {
                "missing": missing,
                "added": added,
            },
            "media": {
                "changed": changed_media,
            },
            "non_text_xml": {
                "changed": changed_non_text_xml,
            },
            "other_non_text_parts": {
                "changed": changed_other,
            },
            "source_sha256": sha256(source.read_bytes()),
            "target_sha256": sha256(target.read_bytes()),
        }
        return report


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Original source .docx, .pptx, or .xlsx file")
    parser.add_argument("target", type=Path, help="Translated target file")
    parser.add_argument("--report", type=Path, help="Optional JSON report path")
    args = parser.parse_args(argv)

    report = validate(args.source, args.target)
    output = json.dumps(report, ensure_ascii=False, indent=2)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output + "\n", encoding="utf-8")
    print(output)
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())

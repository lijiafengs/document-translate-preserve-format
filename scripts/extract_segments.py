#!/usr/bin/env python3
"""Extract translatable OOXML text segments to CSV."""

from __future__ import annotations

import argparse
import csv
import sys
import zipfile
from pathlib import Path

from ooxml_common import detect_format, element_path, iter_parts, iter_text_nodes, read_xml


FIELDNAMES = [
    "segment_id",
    "format",
    "part",
    "node_index",
    "xml_path",
    "text",
    "translation",
    "notes",
]


def extract(source: Path):
    suffix = detect_format(source)
    segment_number = 0
    with zipfile.ZipFile(source) as zf:
        for part in iter_parts(source, suffix):
            root = read_xml(zf, part)
            if root is None:
                continue
            for node_index, node in enumerate(iter_text_nodes(root, suffix)):
                segment_number += 1
                yield {
                    "segment_id": f"s{segment_number:06d}",
                    "format": suffix.lstrip("."),
                    "part": part,
                    "node_index": str(node_index),
                    "xml_path": element_path(root, node),
                    "text": node.text or "",
                    "translation": "",
                    "notes": "",
                }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Source .docx, .pptx, or .xlsx file")
    parser.add_argument("segments_csv", type=Path, help="CSV file to write")
    args = parser.parse_args(argv)

    rows = list(extract(args.source))
    args.segments_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.segments_csv.open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Extracted {len(rows)} segment(s) to {args.segments_csv}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

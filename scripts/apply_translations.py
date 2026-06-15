#!/usr/bin/env python3
"""Apply translated CSV segments back into the original OOXML package."""

from __future__ import annotations

import argparse
import csv
import sys
import zipfile
from collections import defaultdict
from pathlib import Path

from ooxml_common import detect_format, iter_text_nodes, read_xml, write_zip_with_replacements, xml_bytes


def read_rows(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as fh:
        for row in csv.DictReader(fh):
            translation = (row.get("translation") or "").strip()
            if not translation:
                continue
            yield row


def apply(source: Path, translations_csv: Path, target: Path) -> int:
    suffix = detect_format(source)
    rows_by_part = defaultdict(list)
    for row in read_rows(translations_csv):
        rows_by_part[row["part"]].append(row)

    replacements = {}
    applied = 0
    with zipfile.ZipFile(source) as zf:
        for part, rows in rows_by_part.items():
            root = read_xml(zf, part)
            if root is None:
                raise SystemExit(f"Cannot parse XML part listed in CSV: {part}")
            nodes = list(iter_text_nodes(root, suffix))
            for row in rows:
                index = int(row["node_index"])
                if index >= len(nodes):
                    raise SystemExit(f"Node index out of range for {part}: {index}")
                current = nodes[index].text or ""
                expected = row.get("text", "")
                if current != expected:
                    raise SystemExit(
                        f"Source text mismatch for {row.get('segment_id', '')} in {part}: "
                        f"expected {expected!r}, found {current!r}"
                    )
                nodes[index].text = row["translation"]
                applied += 1
            replacements[part] = xml_bytes(root)

    write_zip_with_replacements(source, target, replacements)
    return applied


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Original source .docx, .pptx, or .xlsx file")
    parser.add_argument("translations_csv", type=Path, help="CSV containing translation column")
    parser.add_argument("target", type=Path, help="Translated output file")
    args = parser.parse_args(argv)

    applied = apply(args.source, args.translations_csv, args.target)
    print(f"Applied {applied} translated segment(s) to {args.target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

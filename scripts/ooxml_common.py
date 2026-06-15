#!/usr/bin/env python3
"""Shared OOXML helpers for format-preserving translation scripts."""

from __future__ import annotations

import hashlib
import posixpath
import re
import zipfile
from pathlib import Path
from typing import Dict, Iterable, List, Optional
from xml.etree import ElementTree as ET


NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


for prefix, uri in NS.items():
    ET.register_namespace(prefix, uri)


TEXT_PART_PATTERNS = {
    ".docx": [
        re.compile(r"^word/document\.xml$"),
        re.compile(r"^word/header\d+\.xml$"),
        re.compile(r"^word/footer\d+\.xml$"),
        re.compile(r"^word/footnotes\.xml$"),
        re.compile(r"^word/endnotes\.xml$"),
        re.compile(r"^word/comments\.xml$"),
    ],
    ".pptx": [
        re.compile(r"^ppt/slides/slide\d+\.xml$"),
        re.compile(r"^ppt/notesSlides/notesSlide\d+\.xml$"),
        re.compile(r"^ppt/comments/comment\d+\.xml$"),
    ],
    ".xlsx": [
        re.compile(r"^xl/sharedStrings\.xml$"),
        re.compile(r"^xl/worksheets/sheet\d+\.xml$"),
        re.compile(r"^xl/comments\d+\.xml$"),
    ],
}


MEDIA_PREFIXES = (
    "word/media/",
    "ppt/media/",
    "xl/media/",
    "word/embeddings/",
    "ppt/embeddings/",
    "xl/embeddings/",
)


def detect_format(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix not in {".docx", ".pptx", ".xlsx"}:
        raise SystemExit(f"Unsupported structured format: {path.suffix}")
    return suffix


def is_text_part(name: str, suffix: str) -> bool:
    return any(pattern.match(name) for pattern in TEXT_PART_PATTERNS.get(suffix, []))


def read_xml(zf: zipfile.ZipFile, name: str) -> Optional[ET.Element]:
    try:
        return ET.fromstring(zf.read(name))
    except ET.ParseError:
        return None


def iter_parts(path: Path, suffix: str) -> Iterable[str]:
    with zipfile.ZipFile(path) as zf:
        for name in zf.namelist():
            if is_text_part(name, suffix):
                yield name


def parent_map(root: ET.Element) -> Dict[ET.Element, ET.Element]:
    return {child: parent for parent in root.iter() for child in list(parent)}


def ancestors(node: ET.Element, parents: Dict[ET.Element, ET.Element]) -> Iterable[ET.Element]:
    current = node
    while current in parents:
        current = parents[current]
        yield current


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def namespace_uri(tag: str) -> str:
    if tag.startswith("{"):
        return tag[1:].split("}", 1)[0]
    return ""


def element_path(root: ET.Element, node: ET.Element) -> str:
    parents = parent_map(root)
    pieces: List[str] = []
    current = node
    while True:
        parent = parents.get(current)
        if parent is None:
            pieces.append(local_name(current.tag))
            break
        siblings = [child for child in list(parent) if child.tag == current.tag]
        index = siblings.index(current) + 1
        pieces.append(f"{local_name(current.tag)}[{index}]")
        current = parent
    return "/" + "/".join(reversed(pieces))


def is_inside_math(node: ET.Element, parents: Dict[ET.Element, ET.Element]) -> bool:
    math_uri = NS["m"]
    return namespace_uri(node.tag) == math_uri or any(namespace_uri(item.tag) == math_uri for item in ancestors(node, parents))


def is_inside_formula_cell(node: ET.Element, parents: Dict[ET.Element, ET.Element]) -> bool:
    for item in ancestors(node, parents):
        if local_name(item.tag) == "c" and item.find("{%s}f" % NS["main"]) is not None:
            return True
    return False


def iter_text_nodes(root: ET.Element, suffix: str):
    parents = parent_map(root)
    if suffix == ".docx":
        for node in root.iter("{%s}t" % NS["w"]):
            if node.text and node.text.strip() and not is_inside_math(node, parents):
                yield node
    elif suffix == ".pptx":
        for node in root.iter("{%s}t" % NS["a"]):
            if node.text and node.text.strip():
                yield node
    elif suffix == ".xlsx":
        for node in root.iter("{%s}t" % NS["main"]):
            if node.text and node.text.strip() and not is_inside_formula_cell(node, parents):
                yield node


def write_zip_with_replacements(source: Path, target: Path, replacements: Dict[str, bytes]) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(source, "r") as zin, zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = replacements.get(item.filename, zin.read(item.filename))
            zi = zipfile.ZipInfo(item.filename, date_time=item.date_time)
            zi.compress_type = item.compress_type
            zi.external_attr = item.external_attr
            zi.comment = item.comment
            zi.extra = item.extra
            zout.writestr(zi, data)


def xml_bytes(root: ET.Element) -> bytes:
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def is_media_or_embedding(name: str) -> bool:
    normalized = posixpath.normpath(name)
    return any(normalized.startswith(prefix) for prefix in MEDIA_PREFIXES)

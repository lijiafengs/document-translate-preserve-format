---
name: document-translate-preserve-format
description: Translate documents while preserving original layout, styles, images, formulas, tables, headers, footers, numbering, hyperlinks, charts, and embedded objects. Use when Codex needs to translate DOCX, PPTX, XLSX, PDF, HTML, Markdown, or LaTeX files and the translated output must match the source document formatting as closely as possible.
---

# Document Translate Preserve Format

## Core Rule

Translate only human-readable text nodes. Preserve the original document package, layout structure, styles, media, formulas, charts, relationships, and embedded objects.

Never rebuild a structured document from plain text when an editable package format is available.

## Format Decision

- For `.docx`, `.pptx`, and `.xlsx`, use the OOXML workflow below and read the matching reference:
  - `references/docx-ooxml.md`
  - `references/pptx-ooxml.md`
  - `references/xlsx-ooxml.md`
- For `.pdf`, read `references/pdf-limitations.md` before promising fidelity. Prefer translating the editable source file when available.
- For `.html`, `.md`, `.tex`, or other text formats, read `references/translation-rules.md` and preserve markup, code, math, links, and placeholders.

## OOXML Workflow

Use the bundled scripts for `.docx`, `.pptx`, and `.xlsx` unless a task needs custom handling.

1. Inspect the package:

   ```powershell
   python scripts/inspect_document.py source.docx --report inspect.json
   ```

2. Extract translatable segments:

   ```powershell
   python scripts/extract_segments.py source.docx segments.csv
   ```

3. Translate the `text` column into the `translation` column. Preserve placeholders, field codes, URLs, numbers that are identifiers, references, and terminology constraints.

4. Apply translations to a copy of the original package:

   ```powershell
   python scripts/apply_translations.py source.docx translated-segments.csv translated-output.docx
   ```

5. Validate unchanged non-text parts:

   ```powershell
   python scripts/validate_layout.py source.docx translated-output.docx --report validate.json
   ```

6. Render or open the result for visual QA when the environment supports it. Check text overflow, missing fonts, broken numbering, table wrapping, cropped labels, and slide placeholders.

## Translation Discipline

- Preserve all XML/package structure except the selected text node content.
- Do not translate formulas, code, field instructions, file paths, URLs, email addresses, variable names, placeholder tokens, or citation keys.
- Keep placeholders exactly byte-for-byte: `{name}`, `{{name}}`, `${name}`, `%s`, `%{name}`, `<tag>`, `[1]`, `\ref{key}`, and similar tokens.
- Keep hyperlinks and relationship IDs unchanged. Translate display text only when it is natural language.
- Keep units, part numbers, SKUs, legal clause IDs, and table/figure numbers unless the user asks otherwise.
- When translation expansion may break layout, prefer concise translation. Report risky locations instead of silently changing layout.
- If images contain text, do not edit them unless the user explicitly asks for image translation/redrawing.
- If a document uses tracked changes, comments, speaker notes, footnotes, or headers/footers, include those parts in the extraction and mention them in QA.

## Script Scope

The scripts are conservative helpers, not a full document translation engine:

- `scripts/inspect_document.py` reports format, text-bearing parts, media/embedding parts, and segment count.
- `scripts/extract_segments.py` writes a UTF-8 CSV with stable segment IDs and source locations.
- `scripts/apply_translations.py` writes non-empty `translation` cells back into the original package and refuses to proceed if the source text changed.
- `scripts/validate_layout.py` checks package entries plus media, embeddings, and non-text XML parts for unexpected changes.

If a script reports a mismatch, stop and inspect the document rather than forcing the write.

## Output Report

When finishing a translation task, report:

- source and output file paths
- source format and target language
- number of translated segments
- validation result
- any fidelity risks, especially PDF reconstruction, OCR uncertainty, text overflow, missing fonts, or image text left untranslated

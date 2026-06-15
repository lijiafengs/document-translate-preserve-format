# DOCX OOXML Notes

DOCX is a ZIP package. Preserve the package and modify only text nodes in relevant WordprocessingML parts.

## Text-Bearing Parts

Common parts:

- `word/document.xml`
- `word/header*.xml`
- `word/footer*.xml`
- `word/footnotes.xml`
- `word/endnotes.xml`
- `word/comments.xml`

The bundled extractor covers these parts.

## Preserve

Do not modify:

- `word/media/*`
- `word/embeddings/*`
- `word/styles.xml`, `word/settings.xml`, `word/numbering.xml`
- drawing elements under `w:drawing`
- formulas under `m:oMath` and `m:oMathPara`
- relationships under `_rels` unless explicitly adding/removing assets

## Editing Guidance

Translate `w:t` text only. Keep `w:rPr`, `w:pPr`, table properties, numbering, bookmarks, comments, and hyperlinks. If a hyperlink has natural-language display text, translate the display text but keep relationship IDs unchanged.

If a paragraph is split into many runs because of styling, preserve the run structure. When translation quality requires reflowing a whole sentence across runs, do it manually and then render-check the result.

## QA

Open or render the result and inspect:

- page count and page breaks
- headers, footers, footnotes, endnotes, comments
- table cell wrapping
- equations and inline symbols
- captions, cross-references, and hyperlinks

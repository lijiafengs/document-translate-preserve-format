# XLSX OOXML Notes

XLSX is a ZIP package. Preserve formulas, workbook structure, formatting, validation, charts, pivots, and media.

## Text-Bearing Parts

Common parts:

- `xl/sharedStrings.xml`
- `xl/worksheets/sheet*.xml` for inline strings
- `xl/comments*.xml`

The bundled extractor covers these parts.

## Preserve

Do not modify:

- formulas in `<f>` elements
- calculated values unless recalculation is intentionally performed
- styles, number formats, conditional formats, data validation, tables, pivots, charts, macros, and relationships
- `xl/media/*` and `xl/embeddings/*`

## Editing Guidance

Translate shared strings and inline string text. Do not translate formula cells. Keep sheet dimensions, cell references, merged cells, and styles.

Be careful with dropdown values and lookup keys. If text appears to be a key used by formulas, validation, or external systems, ask before translating or record the risk.

## QA

Open or recalculate the workbook when possible and inspect:

- formulas still evaluate
- filters, validations, pivots, and charts still work
- translated text fits cells or wrapped cells
- sheet names and named ranges remain valid if translated

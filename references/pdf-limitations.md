# PDF Limitations

PDF fidelity is fundamentally different from DOCX, PPTX, or XLSX. PDF is usually a final layout format, not an editable semantic document.

## Preferred Strategy

Ask for the editable source file whenever possible:

- DOCX for Word exports
- PPTX for slide exports
- XLSX for spreadsheet exports
- InDesign, LaTeX, HTML, or other original sources

Translate the source format, then export a new PDF.

## If Only PDF Is Available

Choose one of these strategies and state the trade-off:

- Overlay translated text on top of the original page. This preserves imagery but may leave hidden source text and can struggle with reflow.
- Reconstruct the document in an editable format, then export PDF. This improves editability but may not perfectly match layout.
- OCR scanned pages, translate OCR text, and rebuild or overlay. This depends on OCR quality and may miss image text, handwriting, symbols, or formulas.

## Do Not Promise

Do not promise exact preservation for PDF-only work unless the task is limited to simple overlay edits and visual QA confirms the result.

## QA

Render source and target pages side by side. Check:

- page count and page size
- text positions and line breaks
- image quality and cropping
- equations and symbols
- tables and borders
- selectable text and OCR errors

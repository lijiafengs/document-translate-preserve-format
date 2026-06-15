# PPTX OOXML Notes

PPTX is a ZIP package. Preserve slide geometry, themes, media, animations, notes, charts, and relationships.

## Text-Bearing Parts

Common parts:

- `ppt/slides/slide*.xml`
- `ppt/notesSlides/notesSlide*.xml`
- `ppt/comments/comment*.xml`

The bundled extractor covers these parts.

## Preserve

Do not modify:

- `ppt/media/*`
- `ppt/embeddings/*`
- slide size, transforms, placeholders, layouts, masters, and themes
- chart packages unless chart labels explicitly need translation
- animation timing and transition parts
- relationship IDs

## Editing Guidance

Translate `a:t` text only. Keep shape positions, text box dimensions, paragraph properties, run properties, bullets, and hyperlinks.

Slides are sensitive to text expansion. Use shorter translations for titles, axis labels, callouts, and buttons. If translated text risks overflow, report the affected slide and shape rather than changing geometry by default.

## QA

Render or open the deck and inspect:

- each translated slide at presentation size
- title/body placeholder overflow
- speaker notes
- charts, legends, and axis labels
- bullet indentation and line breaks
- animations or builds if the deck uses them

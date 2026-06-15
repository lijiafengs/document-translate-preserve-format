# Translation Rules

Use these rules for every format.

## Protect Before Translating

Keep these tokens unchanged:

- URLs, emails, file paths, command names, environment variables
- placeholders such as `{name}`, `{{name}}`, `${name}`, `%s`, `%d`, `%{name}`
- XML/HTML/Markdown/LaTeX tags and attributes
- citation and reference keys such as `[1]`, `\ref{fig:arch}`, `\cite{smith2024}`
- code identifiers, API names, database column names, formulas, and equations
- SKUs, clause IDs, figure/table numbers, and serial numbers

If needed, replace protected tokens with temporary markers before translation and restore them after translation.

## Segment Translation

Translate each segment with enough surrounding context to keep terminology consistent. Do not merge segments unless the target format can safely represent the merged structure. For Office documents, preserve run boundaries unless a script or manual XML edit proves a merge is safe.

Prefer concise wording when text boxes, table cells, headers, footers, or slide shapes have limited room.

## Quality Checks

Check:

- all protected tokens are present after translation
- no source-language leftovers remain in regular body text
- target-language punctuation and spacing are natural
- translated labels still fit their containers
- numbering, cross-references, and hyperlinks still work

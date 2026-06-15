# document-translate-preserve-format

Codex skill for translating documents while preserving original layout, styles, images, formulas, tables, headers, footers, numbering, hyperlinks, charts, and embedded objects.

## Install

Copy or clone this repository into your Codex skills directory:

```powershell
git clone <repo-url> "$env:USERPROFILE\.codex\skills\document-translate-preserve-format"
```

Restart Codex after installation.

## Usage

Ask Codex to use:

```text
$document-translate-preserve-format
```

For OOXML documents, the skill includes helper scripts for inspecting, extracting text segments, applying translations, and validating unchanged layout-related package parts.

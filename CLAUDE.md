# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo contains

A 1954 Russian logic textbook (Виноградов & Кузьмин, "Логика") converted from PDF to Markdown.

- `Logika_Uchebnik_dlya_sredney_shkoly-Vinogradov-1954.pdf` — source PDF
- `convert.py` — extraction script (uses `pdftotext -layout` via subprocess)
- `chapters/` — output: one `.md` file per chapter, named `NN_glava_ROMAN.md`

## Re-running the conversion

```bash
python3 convert.py
```

Requires `pdftotext` (poppler-utils). On Ubuntu: `sudo apt install poppler-utils`.

## How convert.py works

1. Runs `pdftotext -layout` on the PDF and splits output into lines.
2. Detects chapter boundaries by matching `Глава <ROMAN>` patterns (handles split across two lines).
3. Slices lines between chapter boundaries; stops at line ~7100 to exclude the table of contents appended at the end of the PDF.
4. Formats `§ N.` lines as `### headings`; joins soft-hyphenated line breaks.
5. Writes each chapter as `chapters/NN_glava_ROMAN.md`.

## Known limitations of the output

- Page numbers from the PDF text layer appear inline within paragraphs.
- Footnote markers (`¹`) stay inline; footnote text appears at the bottom of the section it was extracted from.
- Spaced letters used for emphasis (e.g., `Л о г и к а`) are preserved as-is from the PDF.

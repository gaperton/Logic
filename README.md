# Logic

**Логика: Учебник для средней школы** (1954) — public domain textbook by I. N. Vinogradov and A. P. Kuzmin, digitized and converted to web format.

## Overview

This project digitizes a classic Russian logic textbook from 1954, converting it from PDF to structured Markdown chapters, then publishing as a static website via GitHub Pages.

## Project Structure

```
Logic/
├── README.md                      # This file
├── convert.py                     # PDF → Markdown converter
├── publish.py                     # Markdown → HTML publisher
├── Logika_Uchebnik_dlya_sredney_shkoly-Vinogradov-1954.pdf
├── chapters/                      # Auto-generated Markdown from PDF
│   ├── 01_glava_I.md
│   ├── 02_glava_II.md
│   └── ...
├── chapters_human_edited/         # Manually edited chapters (source for publishing)
└── docs/                          # Generated HTML site (GitHub Pages)
```

## Workflow

### 1. Convert PDF to Markdown

```bash
python convert.py
```

This script:
- Extracts text from the PDF using `pdftotext`
- Detects chapter boundaries (Глава I-XII)
- Cleans formatting artifacts (page numbers, footnote markers, hyphenation)
- Applies Markdown structure (headings, paragraphs)
- Outputs one `.md` file per chapter to `chapters/`

**Dependencies:** `pdftotext` (from poppler-utils)

### 2. Edit Chapters

Review and manually edit the generated Markdown files in `chapters/`, then move corrected versions to `chapters_human_edited/`:

```bash
mv chapters/01_glava_I.md chapters_human_edited/
```

### 3. Publish to HTML

```bash
python publish.py
```

This script:
- Converts Markdown chapters to HTML using Python-Markdown
- Generates a responsive single-page website with navigation
- Outputs to `docs/` folder

**Dependencies:** `markdown` Python package (auto-installed if missing)

### 4. Deploy to GitHub Pages

1. Commit the `docs/` folder:
   ```bash
   git add docs/
   git commit -m "Publish updated textbook"
   git push
   ```

2. Enable GitHub Pages: **Settings → Pages → Branch: main / /docs**

## Book Information

- **Title:** Логика (Logic)
- **Subtitle:** Учебник для средней школы (Textbook for Secondary School)
- **Authors:** И. Н. Виноградов (I. N. Vinogradov), А. П. Кузьмин (A. P. Kuzmin)
- **Year:** 1954
- **Status:** Public domain

## License

Public domain (public достояние in Russian).

## Technical Notes

- The converter uses regex-based chapter detection and text cleaning pipelines
- Inline footnote markers and page numbers are automatically stripped
- Soft hyphens and line-break hyphens are joined
- The HTML output uses embedded CSS with a classic academic design
- Mobile-responsive layout with Georgia/Times serif fonts

# Logic

**Логика: Учебник для средней школы** — edited edition of the 1954 textbook by I. N. Vinogradov and A. P. Kuzmin, published as a static website via GitHub Pages.

The original textbook belongs to the Aristotelian tradition of traditional logic — concepts, judgements, syllogisms, proof — and remains more useful for anyone who wants to reason better in natural language than modern symbolic logic, which assumes premises are already precise. The 1954 text was digitized from PDF, then edited for a modern reader: OCR artifacts corrected, outdated phrasing modernized, and Soviet ideological content replaced with neutral equivalents (e.g. propaganda syllogisms swapped for examples from natural science and everyday life). The logical content of every chapter and exercise is preserved unchanged.

Editors: Vlad Balin ([@gaperton](https://github.com/gaperton)), Yuriy Shelyakh ([@drcha0s](https://github.com/drcha0s))

## Project Structure

```
Logic/
├── convert.py                 # PDF → Markdown converter
├── publish.py                 # Markdown → HTML publisher
├── chapters/                  # Auto-generated Markdown from PDF
├── chapters_ai_edited/        # AI-assisted edits
├── chapters_human_edited/     # Final manually edited chapters (source for publishing)
└── docs/                      # Generated HTML site (GitHub Pages)
```

## Workflow

### 1. Convert PDF to Markdown

```bash
python3 convert.py
```

Extracts text via `pdftotext`, detects chapter boundaries, strips page numbers and footnote markers, joins hyphenated line breaks, and outputs one `.md` file per chapter to `chapters/`.

**Requires:** `pdftotext` (poppler-utils)

### 2. Edit chapters

Review and edit generated files, then place corrected versions in `chapters_human_edited/`. That directory is the source for publishing.

### 3. Build the site

```bash
python3 publish.py
```

Converts Markdown to HTML using `markdown2`, generates navigation, and writes to `docs/`.

**Requires:** `markdown2` (auto-installed if missing)

### 4. Preview locally

```bash
python3 -m http.server 8000 --directory docs
```

Then open [http://localhost:8000](http://localhost:8000).

### 5. Deploy

Commit `docs/` and push to `main`. Enable GitHub Pages: **Settings → Pages → Branch: main / /docs**.

## Design

- Georgia/Times serif, justified text with first-line indent
- Sticky nav with prev/next chapter buttons
- CSS reading progress bar (scroll-driven, no JS)
- Print stylesheet (hides nav and footer)
- Mobile-responsive

## Book

| | |
|---|---|
| Title | Логика (Logic) |
| Subtitle | Учебник для средней школы |
| Authors | И. Н. Виноградов, А. П. Кузьмин |
| Year | 1954 |
| Status | Public domain (original text) |
| Editorial materials | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) |

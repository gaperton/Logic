#!/usr/bin/env python3
"""Build the logic textbook into /docs for GitHub Pages (main branch, /docs folder)."""

import shutil
import subprocess
import sys
from pathlib import Path

try:
    import markdown2
except ImportError:
    print("Installing markdown2 library...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "markdown2"])
    import markdown2

REPO_ROOT = Path(__file__).parent
SOURCE_DIR = REPO_ROOT / "chapters_human_edited"
SITE_DIR = REPO_ROOT / "docs"

BOOK_TITLE = "Логика"
BOOK_SUBTITLE = "Учебник для средней школы"
BOOK_AUTHORS = "И. Н. Виноградов, А. П. Кузьмин"
BOOK_YEAR = "1954"

CSS = """
:root {
  --text: #1c1a17;
  --bg: #faf8f3;
  --bg-nav: #1e1c19;
  --accent: #8b1a1a;
  --border: #d4c9b0;
  --link: #5c3317;
  --muted: #666;
  --max-width: 740px;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html { scroll-behavior: smooth; }

body {
  font-family: "Georgia", "Times New Roman", serif;
  font-size: 18px;
  line-height: 1.85;
  color: var(--text);
  background: var(--bg);
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* ─── Reading progress bar ───────────────────────────────── */
body::before {
  content: '';
  position: fixed;
  top: 0; left: 0;
  height: 2px;
  width: 100%;
  background: var(--accent);
  transform-origin: 0 50%;
  scale: 0 1;
  z-index: 999;
  animation: reading-progress linear both;
  animation-timeline: scroll();
}
@keyframes reading-progress { to { scale: 1 1; } }

/* ─── Navigation ─────────────────────────────────────────── */
nav {
  background: var(--bg-nav);
  padding: 0 1.25rem;
  height: 46px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  position: sticky;
  top: 0;
  z-index: 10;
}

nav a {
  color: #b8b0a0;
  text-decoration: none;
  font-size: 0.8rem;
  font-family: sans-serif;
  white-space: nowrap;
  padding: 0.3rem 0.6rem;
  border-radius: 3px;
  transition: background 0.15s, color 0.15s;
}

nav a:hover { color: #fff; background: rgba(255,255,255,0.1); }

nav .spacer { flex: 1; }

nav .chapter-nav {
  display: flex;
  gap: 0.4rem;
}

nav .chapter-nav a {
  border: 1px solid rgba(255,255,255,0.12);
  max-width: 26ch;
  overflow: hidden;
  text-overflow: ellipsis;
}

nav .chapter-nav a:hover {
  border-color: rgba(255,255,255,0.3);
}

/* ─── Main content ─────────────────────────────────────── */
main {
  flex: 1;
  max-width: var(--max-width);
  width: 100%;
  margin: 0 auto;
  padding: 3rem 1.5rem 6rem;
}

/* ─── Book cover (index) ─────────────────────────────────── */
.book-header {
  text-align: center;
  padding: 5rem 0 3.5rem;
  border-bottom: 2px solid var(--border);
  margin-bottom: 3rem;
}

.book-header h1 {
  font-size: 3.5rem;
  color: var(--accent);
  letter-spacing: 0.06em;
  margin-bottom: 0.75rem;
  font-weight: normal;
  line-height: 1.1;
  border-bottom: none;
  padding-bottom: 0;
}

.book-header .subtitle {
  font-size: 1rem;
  color: var(--muted);
  margin-bottom: 0.4rem;
  letter-spacing: 0.04em;
}

.book-header .authors {
  font-style: italic;
  color: #999;
  font-size: 0.88rem;
}

/* ─── Table of contents ──────────────────────────────────── */
.toc h2 {
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  color: var(--muted);
  margin-bottom: 1.25rem;
  font-family: sans-serif;
  font-weight: 400;
}

.toc ol { list-style: none; }

.toc li { border-bottom: 1px solid var(--border); }

.toc li a {
  display: block;
  padding: 0.65rem 0;
  color: var(--link);
  text-decoration: none;
  font-size: 0.95rem;
  transition: color 0.15s, padding-left 0.15s;
}

.toc li a:hover {
  color: var(--accent);
  padding-left: 0.4rem;
}

/* ─── Headings ───────────────────────────────────────────── */
h1 {
  font-size: 1.5rem;
  color: var(--accent);
  margin-bottom: 2rem;
  line-height: 1.35;
  font-weight: normal;
  padding-bottom: 0.85rem;
  border-bottom: 1px solid var(--border);
}

h2 {
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  color: var(--muted);
  font-weight: 400;
  font-family: sans-serif;
  margin: 3rem 0 1.5rem;
}

h3 {
  font-size: 1rem;
  font-style: italic;
  font-weight: normal;
  margin: 2.5rem 0 0.75rem;
  color: var(--accent);
}

/* ─── Body text ──────────────────────────────────────────── */
p {
  margin-bottom: 0;
  text-align: justify;
  text-indent: 1.5em;
  hyphens: auto;
  -webkit-hyphens: auto;
}

/* No indent after headings and certain elements */
h1 + p, h2 + p, h3 + p,
blockquote + p, .book-header p,
li > p, li > p:first-child { text-indent: 0; }

/* Center book-header text even though p is justify */
.book-header p { text-align: center; }

.edition-note {
  margin-top: 1.75rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.3rem;
}

.edition-label {
  font-family: sans-serif;
  font-size: 0.68rem;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  color: var(--muted);
}

.edition-editors {
  font-style: italic;
  font-size: 0.88rem;
  color: #999;
}

.github-link {
  display: flex;
  align-items: center;
  color: #b8b0a0;
  opacity: 0.55;
  padding: 0.3rem;
  border-radius: 3px;
  transition: opacity 0.15s, background 0.15s;
}

.github-link:hover { opacity: 1; background: rgba(255,255,255,0.1); }

/* ─── Blockquotes ─────────────────────────────────────────── */
blockquote {
  margin: 1.5rem 0;
  padding: 0.6rem 1.25rem;
  border-left: 2px solid var(--accent);
  color: #555;
  font-style: italic;
  background: rgba(139,26,26,0.03);
  border-radius: 0 2px 2px 0;
  font-size: 0.95em;
}

blockquote p { text-indent: 0; margin-bottom: 0.5rem; }
blockquote p:last-child { margin-bottom: 0; }

/* ─── Lists ──────────────────────────────────────────────── */
ol, ul { padding-left: 1.75rem; margin: 1rem 0; }
li { margin-bottom: 0.4rem; }
li p { text-indent: 0; margin-bottom: 0.3rem; }

/* ─── Images ─────────────────────────────────────────────── */
img { max-width: 100%; display: block; margin: 2rem auto; }

/* ─── Tables ─────────────────────────────────────────────── */
table {
  width: 100%;
  border-collapse: collapse;
  margin: 1.75rem 0;
  font-size: 0.92rem;
}

th, td {
  border: 1px solid var(--border);
  padding: 0.5rem 0.75rem;
  text-align: left;
}

th {
  background: rgba(212,201,176,0.35);
  font-weight: normal;
  font-style: italic;
}

/* ─── Footer ─────────────────────────────────────────────── */
footer {
  text-align: center;
  padding: 1.5rem;
  font-size: 0.78rem;
  color: #aaa;
  font-family: sans-serif;
  border-top: 1px solid var(--border);
}

/* ─── Mobile ─────────────────────────────────────────────── */
@media (max-width: 600px) {
  body { font-size: 16px; }
  .book-header h1 { font-size: 2.5rem; }
  main { padding: 2rem 1.25rem 4rem; }
  nav { height: auto; padding: 0.5rem 1rem; flex-wrap: wrap; }
  nav .chapter-nav a { max-width: 18ch; }
}

/* ─── Print ──────────────────────────────────────────────── */
@media print {
  nav, footer, body::before { display: none; }
  main { padding: 0; }
  h1 { color: #000; border: none; }
  a { color: #000; text-decoration: none; }
}
"""

GITHUB_ICON = '<a href="https://github.com/gaperton/Logic" class="github-link" title="GitHub" target="_blank" rel="noopener"><svg width="18" height="18" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg></a>'

NAV_TEMPLATE = """\
<nav>
  <a href="index.html">&#8962; Оглавление</a>
  <span class="spacer"></span>
  <div class="chapter-nav">
    {prev_link}
    {next_link}
  </div>
  """ + GITHUB_ICON + """
</nav>"""

PAGE_TEMPLATE = """\
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — {book_title}</title>
  <style>{css}</style>
</head>
<body>
{nav}
<main>
{content}
</main>
<footer>{book_authors}, {book_year}. Учебник для средней школы.</footer>
</body>
</html>"""

INDEX_TEMPLATE = """\
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{book_title} — {book_subtitle}</title>
  <style>{css}</style>
</head>
<body>
<nav>
  <a href="index.html">&#8962; Оглавление</a>
  <span class="spacer"></span>
  {github_icon}
</nav>
<main>
  <div class="book-header">
    <h1>{book_title}</h1>
    <p class="subtitle">{book_subtitle}</p>
    <p class="authors">{book_authors}, {book_year}</p>
    <div class="edition-note">
      <span class="edition-label">Редактированное издание</span>
      <span class="edition-editors">ред. В. Балин, Ю. Шелях, 2026</span>
    </div>
  </div>
  <div class="toc">
    <h2>Содержание</h2>
    <ol>
{toc_items}
    </ol>
  </div>
</main>
<footer>Публичное достояние.</footer>
</body>
</html>"""


def get_chapter_files():
    return sorted(SOURCE_DIR.glob("[0-9][0-9]_*.md"))


def extract_title(md_text: str) -> str:
    for line in md_text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return "Глава"


def build():
    if SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)
    SITE_DIR.mkdir()

    # Copy images (including those in chapter subdirectories)
    for img in SOURCE_DIR.glob("*.png"):
        shutil.copy(img, SITE_DIR / img.name)
    for img in SOURCE_DIR.glob("*.jpg"):
        shutil.copy(img, SITE_DIR / img.name)
    # Copy images from chapter subdirectories
    for chapter_dir in SOURCE_DIR.iterdir():
        if chapter_dir.is_dir():
            chapter_img_dir = SITE_DIR / chapter_dir.name
            chapter_img_dir.mkdir(exist_ok=True)
            for img in chapter_dir.glob("*"):
                if img.is_file() and (img.suffix.lower() in [".png", ".jpg", ".jpeg", ".gif", ".svg"]):
                    shutil.copy(img, chapter_img_dir / img.name)

    chapter_files = get_chapter_files()
    chapters = []
    for f in chapter_files:
        text = f.read_text(encoding="utf-8")
        chapters.append({
            "path": f,
            "title": extract_title(text),
            "slug": f.stem + ".html",
            "text": text,
        })

    for i, ch in enumerate(chapters):
        md = markdown2.Markdown(extras=["tables", "fenced-code-blocks", "strike"])
        content_html = md.convert(ch["text"])

        prev_link = (
            f'<a href="{chapters[i-1]["slug"]}">&#8592; {chapters[i-1]["title"]}</a>'
            if i > 0 else ""
        )
        next_link = (
            f'<a href="{chapters[i+1]["slug"]}">{chapters[i+1]["title"]} &#8594;</a>'
            if i < len(chapters) - 1 else ""
        )

        nav = NAV_TEMPLATE.format(prev_link=prev_link, next_link=next_link)
        page = PAGE_TEMPLATE.format(
            title=ch["title"],
            book_title=BOOK_TITLE,
            css=CSS,
            nav=nav,
            content=content_html,
            book_authors=BOOK_AUTHORS,
            book_year=BOOK_YEAR,
        )
        (SITE_DIR / ch["slug"]).write_text(page, encoding="utf-8")
        print(f"  {ch['slug']}")

    toc_items = "\n".join(
        f'      <li><a href="{ch["slug"]}">{ch["title"]}</a></li>'
        for ch in chapters
    )
    index = INDEX_TEMPLATE.format(
        book_title=BOOK_TITLE,
        book_subtitle=BOOK_SUBTITLE,
        book_authors=BOOK_AUTHORS,
        book_year=BOOK_YEAR,
        css=CSS,
        toc_items=toc_items,
        github_icon=GITHUB_ICON,
    )
    (SITE_DIR / "index.html").write_text(index, encoding="utf-8")
    # GitHub Pages needs this when not using Jekyll
    (SITE_DIR / ".nojekyll").touch()

    print(f"\nBuilt {len(chapters)} chapters → {SITE_DIR}/")
    print(f"Preview: open {SITE_DIR / 'index.html'}")
    print("\nTo publish: commit the docs/ folder and push to main.")
    print("Then enable GitHub Pages: Settings → Pages → Branch: main / /docs")


if __name__ == "__main__":
    build()

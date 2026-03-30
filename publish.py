#!/usr/bin/env python3
"""Build the logic textbook into /docs for GitHub Pages (main branch, /docs folder)."""

import shutil
import subprocess
import sys
from pathlib import Path

try:
    import markdown
except ImportError:
    print("Installing markdown library...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "markdown"])
    import markdown

REPO_ROOT = Path(__file__).parent
SOURCE_DIR = REPO_ROOT / "chapters_human_edited"
SITE_DIR = REPO_ROOT / "docs"

BOOK_TITLE = "Логика"
BOOK_SUBTITLE = "Учебник для средней школы"
BOOK_AUTHORS = "И. Н. Виноградов, А. П. Кузьмин"
BOOK_YEAR = "1954"

CSS = """
:root {
  --text: #1a1a1a;
  --bg: #faf8f3;
  --bg-nav: #2c2c2c;
  --accent: #8b1a1a;
  --border: #d4c9b0;
  --link: #5c3317;
  --max-width: 720px;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: "Georgia", "Times New Roman", serif;
  font-size: 18px;
  line-height: 1.75;
  color: var(--text);
  background: var(--bg);
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

nav {
  background: var(--bg-nav);
  padding: 0.75rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
  position: sticky;
  top: 0;
  z-index: 10;
}

nav a {
  color: #e0d8c8;
  text-decoration: none;
  font-size: 0.85rem;
  font-family: sans-serif;
  white-space: nowrap;
}

nav a:hover { color: #fff; text-decoration: underline; }

nav .spacer { flex: 1; }

nav .chapter-nav { display: flex; gap: 1rem; }

main {
  flex: 1;
  max-width: var(--max-width);
  width: 100%;
  margin: 0 auto;
  padding: 3rem 1.5rem 5rem;
}

.book-header {
  text-align: center;
  padding: 4rem 0 3rem;
  border-bottom: 2px solid var(--border);
  margin-bottom: 3rem;
}

.book-header h1 {
  font-size: 3rem;
  color: var(--accent);
  letter-spacing: 0.05em;
  margin-bottom: 0.5rem;
}

.book-header .subtitle {
  font-size: 1.1rem;
  color: #555;
  margin-bottom: 0.3rem;
}

.book-header .authors {
  font-style: italic;
  color: #777;
  font-size: 0.95rem;
}

.toc h2 {
  font-size: 1.2rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #666;
  margin-bottom: 1.5rem;
  font-family: sans-serif;
  font-weight: 400;
}

.toc ol { list-style: none; }

.toc li { border-bottom: 1px solid var(--border); }

.toc li a {
  display: block;
  padding: 0.75rem 0;
  color: var(--link);
  text-decoration: none;
  font-size: 1rem;
}

.toc li a:hover {
  color: var(--accent);
  padding-left: 0.5rem;
  transition: padding 0.15s;
}

h1 { font-size: 1.8rem; color: var(--accent); margin-bottom: 2rem; line-height: 1.3; }

h2 { font-size: 1.35rem; margin: 2.5rem 0 1rem; }

h3 {
  font-size: 1.1rem;
  font-style: italic;
  font-weight: normal;
  margin: 2rem 0 0.75rem;
  color: #333;
}

p { margin-bottom: 1.1rem; text-align: justify; }

blockquote {
  border-left: 3px solid var(--border);
  margin: 1.5rem 0;
  padding: 0.5rem 1.25rem;
  color: #444;
  font-style: italic;
}

img { max-width: 100%; display: block; margin: 1.5rem auto; }

strong { color: #111; }

table {
  width: 100%;
  border-collapse: collapse;
  margin: 1.5rem 0;
  font-size: 0.95rem;
}

th, td {
  border: 1px solid var(--border);
  padding: 0.5rem 0.75rem;
  text-align: left;
}

th { background: #ede8dc; }

footer {
  text-align: center;
  padding: 1.5rem;
  font-size: 0.8rem;
  color: #888;
  font-family: sans-serif;
  border-top: 1px solid var(--border);
}

@media (max-width: 600px) {
  body { font-size: 16px; }
  .book-header h1 { font-size: 2.2rem; }
  main { padding: 2rem 1rem 4rem; }
}
"""

NAV_TEMPLATE = """\
<nav>
  <a href="index.html">&#8962; Оглавление</a>
  <span class="spacer"></span>
  <div class="chapter-nav">
    {prev_link}
    {next_link}
  </div>
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
</nav>
<main>
  <div class="book-header">
    <h1>{book_title}</h1>
    <p class="subtitle">{book_subtitle}</p>
    <p class="authors">{book_authors}, {book_year}</p>
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
    return sorted(SOURCE_DIR.glob("[0-9][0-9]_glava_*.md"))


def extract_title(md_text: str) -> str:
    for line in md_text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return "Глава"


def build():
    if SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)
    SITE_DIR.mkdir()

    # Copy images
    for img in SOURCE_DIR.glob("*.png"):
        shutil.copy(img, SITE_DIR / img.name)
    for img in SOURCE_DIR.glob("*.jpg"):
        shutil.copy(img, SITE_DIR / img.name)

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

    md = markdown.Markdown(extensions=["tables", "fenced_code"])

    for i, ch in enumerate(chapters):
        md.reset()
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

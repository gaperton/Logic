#!/usr/bin/env python3
"""Convert PDF logic textbook to one markdown file per chapter."""

import subprocess
import re
import os

PDF = "/home/gaperton/Logic/Logika_Uchebnik_dlya_sredney_shkoly-Vinogradov-1954.pdf"
OUT_DIR = "/home/gaperton/Logic/chapters"

os.makedirs(OUT_DIR, exist_ok=True)

result = subprocess.run(["pdftotext", "-layout", PDF, "-"], capture_output=True, text=True)
lines = result.stdout.splitlines()

ROMAN = r"(?:I{1,3}|IV|VI{0,3}|IX|XI{0,3}|XII)"

# ── Chapter boundary detection ──────────────────────────────────────────────

chapter_starts = []
i = 0
while i < len(lines):
    line = lines[i].strip()
    m = re.match(rf'^Глава\s+({ROMAN})\s*$', line)
    if m:
        chapter_starts.append((i, m.group(1)))
        i += 1
        continue
    m = re.match(r'^Глава\s*$', line)
    if m and i + 1 < len(lines):
        m2 = re.match(rf'^({ROMAN})\s*$', lines[i + 1].strip())
        if m2:
            chapter_starts.append((i, m2.group(1)))
            i += 2
            continue
    i += 1

chapter_starts = chapter_starts[:12]  # skip TOC repetitions at end

roman_to_int = {
    'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6,
    'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10, 'XI': 11, 'XII': 12
}

# ── Text cleaning pipeline ───────────────────────────────────────────────────

def is_standalone_number(s):
    """Standalone 1-3 digit number — page number or footnote marker, both noise."""
    return bool(re.match(r'^\d{1,3}$', s))


def strip_inline_footnote_markers(line):
    """Remove superscript footnote digits glued directly to a letter."""
    return re.sub(r'(?<=[а-яёА-ЯЁa-zA-Z])(\d{1,2})(?=[\s».,;:!?\-]|$)', '', line)

def process_lines(raw_lines):
    """Full pipeline: clean → structure → markdown."""

    # Pass 1: strip inline footnote superscripts
    lines1 = [strip_inline_footnote_markers(l) for l in raw_lines]

    # Pass 2: join soft/hard hyphenated line breaks
    lines2 = []
    for line in lines1:
        if lines2 and re.search(r'[­\u00ad-]\s*$', lines2[-1]):
            lines2[-1] = re.sub(r'[­\u00ad-]\s*$', '', lines2[-1]) + line.lstrip()
        else:
            lines2.append(line)

    # Pass 3: drop all standalone numbers (page numbers + footnote markers)
    lines3 = [l for l in lines2 if not is_standalone_number(l.strip())]

    # Pass 4: normalize extra spaces
    lines4 = [re.sub(r'  +', ' ', l) for l in lines3]

    # Pass 5: apply markdown headings
    output = []
    for line in lines4:
        s = line.strip()
        if not s:
            output.append('')
        elif re.match(r'^§\s*[\dIVXivx]+[.\s]', s):
            output.append(f'\n### {s}\n')
        elif re.match(r'^ВОПРОСЫ ДЛЯ ПОВТОРЕНИЯ', s):
            output.append(f'\n## {s}\n')
        else:
            output.append(s)

    return re.sub(r'\n{3,}', '\n\n', '\n'.join(output))


# ── Per-chapter extraction and writing ───────────────────────────────────────

for idx, (start_line, roman_num) in enumerate(chapter_starts):
    end_line = chapter_starts[idx + 1][0] if idx + 1 < len(chapter_starts) else 7100

    chapter_lines = lines[start_line:end_line]

    # Find chapter title: first non-heading line after "Глава N"
    title = ''
    for l in chapter_lines[:6]:
        s = l.strip()
        if s and not re.match(rf'^Глава\s*({ROMAN})?\s*$', s) and not re.match(rf'^({ROMAN})\s*$', s):
            title = s
            break

    num = roman_to_int.get(roman_num, idx + 1)
    filename = f"{num:02d}_glava_{roman_num}.md"
    filepath = os.path.join(OUT_DIR, filename)

    body = process_lines(chapter_lines[2:])  # skip "Глава N" header line(s)
    md = f"# Глава {roman_num}. {title}\n\n{body}"

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(md)

    print(f"  {filename}  ({len(md):,} chars)")

print("\nDone.")

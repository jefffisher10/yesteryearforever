#!/usr/bin/env python3
"""
inject_meta.py
--------------
Run once from your site root:
    python3 inject_meta.py

Reads writing.html and making.html to build a map of:
    filename → (category, description)

Then injects two HTML comments into each post file, right after <body>:
    <!-- category: writing -->
    <!-- desc: your one-line description here -->

Skips files that already have a category comment.
"""

import re
from pathlib import Path

# ── Parse a category page for entries ───────────────────────────────────────

def parse_category_page(filepath, category):
    """
    Extract {filename: desc} from a category index page.
    Reads href from entry-title links and text from entry-desc spans.
    Strips the trailing ' · YYYY' year tag from descriptions.
    """
    content = Path(filepath).read_text(encoding="utf-8")
    entries = {}

    # Find all list items
    items = re.findall(
        r'<a href="([^"]+)"[^>]*class="entry-title"[^>]*>.*?</a>.*?'
        r'<span[^>]*class="entry-desc"[^>]*>(.*?)</span>',
        content,
        re.DOTALL
    )

    for filename, desc_raw in items:
        # Strip ' · YYYY' year suffix if present
        desc = re.sub(r'\s*·\s*\d{4}\s*$', '', desc_raw.strip()).strip()
        entries[filename] = desc

    return entries


# ── Inject comments into a post file ────────────────────────────────────────

def inject_meta(filepath, category, desc):
    content = Path(filepath).read_text(encoding="utf-8")

    # Already has category tag — skip
    if '<!-- category:' in content:
        print(f"  [skip]    {filepath}  (already tagged)")
        return

    comment_block = (
        f'\n  <!-- category: {category} -->\n'
        f'  <!-- desc: {desc} -->\n'
    )

    # Insert right after <body> (with any attributes)
    updated = re.sub(
        r'(<body[^>]*>)',
        r'\1' + comment_block,
        content,
        count=1
    )

    if updated == content:
        print(f"  [skip]    {filepath}  (no <body> tag found)")
        return

    Path(filepath).write_text(updated, encoding="utf-8")
    print(f"  [tagged]  {filepath}  [{category}] {desc}")


# ── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    print("\nParsing category pages...\n")

    writing = parse_category_page("writing.html", "writing")
    making  = parse_category_page("making.html",  "making")

    # Merge into one map — writing takes priority if somehow duplicate
    all_entries = {}
    for filename, desc in making.items():
        all_entries[filename] = ("making", desc)
    for filename, desc in writing.items():
        all_entries[filename] = ("writing", desc)

    print(f"Found {len(writing)} writing entries")
    print(f"Found {len(making)} making entries")
    print(f"\nInjecting meta comments...\n")

    missing = []

    for filename, (category, desc) in sorted(all_entries.items()):
        path = Path(filename)
        if not path.exists():
            missing.append(filename)
            print(f"  [missing] {filename}")
            continue
        inject_meta(path, category, desc)

    print(f"\n✅ Done!")

    if missing:
        print(f"\n⚠ {len(missing)} file(s) not found on disk:")
        for f in missing:
            print(f"   {f}")

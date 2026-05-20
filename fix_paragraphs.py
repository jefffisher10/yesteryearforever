#!/usr/bin/env python3
"""
fix_paragraphs.py
-----------------
Run once from your site root:
    pip install beautifulsoup4 --break-system-packages
    python3 fix_paragraphs.py

Finds <p> tags that contain block-level elements (figure, div, hr, etc.)
and splits them into proper siblings so browsers don't auto-close the <p>
and break the styling of everything after the first image.
"""

import os
import re
from bs4 import BeautifulSoup, NavigableString, Tag

# Block-level elements that can't live inside a <p>
BLOCK_TAGS = {
    'figure', 'div', 'hr', 'h2', 'h3', 'h4',
    'ul', 'ol', 'table', 'audio', 'iframe', 'pre', 'blockquote'
}

# Files to skip — already fixed manually or have special structure
SKIP_FILES = {
    'making.html', 'writing.html', 'seeing.html', 'template.html',
    'index.html', 'ABOUT.html', 'archive.html', 'lectures.html',
    'music_projects.html', 'nature-tech_romance.html', 'play_with_your_food.html',
}


def needs_fix(p_tag):
    """Return True if this <p> contains any block-level children."""
    for child in p_tag.children:
        if isinstance(child, Tag) and child.name in BLOCK_TAGS:
            return True
    return False


def clean_inline(html_str):
    """Strip leading/trailing <br> tags and whitespace from inline content."""
    s = html_str.strip()
    s = re.sub(r'^(\s*<br\s*/?>\s*)+', '', s).strip()
    s = re.sub(r'(\s*<br\s*/?>\s*)+$', '', s).strip()
    return s


def split_p_inplace(p_tag):
    """
    Split a <p> tag containing block elements into proper siblings.
    Modifies the BS4 tree in place.
    """
    segments = []
    current_inline = []

    for child in list(p_tag.children):
        is_block = isinstance(child, Tag) and child.name in BLOCK_TAGS
        if is_block:
            if current_inline:
                segments.append(('inline', list(current_inline)))
                current_inline = []
            segments.append(('block', child))
        else:
            current_inline.append(child)

    if current_inline:
        segments.append(('inline', list(current_inline)))

    # Build replacement elements
    new_elements = []
    for kind, content in segments:
        if kind == 'block':
            new_elements.append(content)
        else:
            inline_html = clean_inline(''.join(str(c) for c in content))
            if inline_html:
                new_p = BeautifulSoup(f'<p>{inline_html}</p>', 'html.parser').p
                new_elements.append(new_p)

    if not new_elements:
        p_tag.decompose()
        return

    # Insert new elements after the original p, then remove it
    ref = p_tag
    for el in new_elements:
        ref.insert_after(el)
        ref = el

    p_tag.decompose()


def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        original = f.read()

    soup = BeautifulSoup(original, 'html.parser')

    # Find all <p> tags with block children — collect first, then process
    # (modifying tree during iteration causes issues)
    to_fix = [p for p in soup.find_all('p') if needs_fix(p)]

    if not to_fix:
        print(f'  [skip]    {filepath}  (no block-in-p found)')
        return

    for p in to_fix:
        split_p_inplace(p)

    updated = str(soup)

    if updated == original:
        print(f'  [skip]    {filepath}  (no change after processing)')
        return

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(updated)

    print(f'  [updated] {filepath}  ({len(to_fix)} <p> tag(s) split)')


if __name__ == '__main__':
    html_files = [
        f for f in os.listdir('.')
        if f.endswith('.html') and f not in SKIP_FILES
    ]

    if not html_files:
        print('No HTML files found. Run from your site root.')
    else:
        print(f'Fixing paragraph structure in {len(html_files)} files...\n')
        for filename in sorted(html_files):
            process_file(filename)
        print('\nDone!')

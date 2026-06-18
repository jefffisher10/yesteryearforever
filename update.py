import os
import re
from pathlib import Path
from datetime import datetime
from PIL import Image

# -----------------------
# CONFIG
# -----------------------

SITE_ROOT = Path(".")
HTML_DIR = SITE_ROOT

SITE_URL = "https://yesteryearforever.xyz"

IMAGE_DIR = SITE_ROOT / "images"
IMAGE_SUBDIR = "images"
THUMB_SUFFIX = "_thumb"
THUMB_SIZE = (500, 500)

ALLOWED_IMAGE_EXTS = {".jpg",".jpeg",".png",".gif",".webp"}

MEDIA_EXTS = (
    ".html",".css",".js",
    ".jpg",".jpeg",".png",".gif",".svg",".webp",
    ".mp3",".m4a",".aac",".ogg",".wav",".flac"
)

FILE_PERMS = 0o644
DIR_PERMS = 0o755

AUDIO_SUBDIR = "audio"

# Pages excluded from category generation, random, archive, sitemap
EXCLUDED_PAGES = {
    "template.html","index.html","mylinks.html","desiderata.html",
    "first_star.html","green_planet.html","space_index.html",
    "preamble.html","lectures.html","archive.html",
    "making.html","writing.html","sensing.html","seeing.html",
    "ABOUT.html",
}

EXCLUDED_RANDOM = EXCLUDED_PAGES | {
    "links.html",
}

EXCLUDED_IMAGE = {
    "first_star.html","green_planet.html","space_index.html"
}

EXCLUDED_SITEMAP = EXCLUDED_PAGES | {
    "README.md","deploy.sh","notes.txt","links.html",
}

# Valid category names
VALID_CATEGORIES = {"writing", "making", "sensing"}


# -----------------------
# TITLE EXTRACTION
# -----------------------

def get_title(path):
    try:
        content = Path(path).read_text(encoding="utf-8")
        match = re.search(r"<title>(.*?)</title>", content, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1).strip()
    except:
        pass
    return Path(path).stem


# -----------------------
# DATE EXTRACTION
# -----------------------

def get_post_date(path):
    try:
        content = Path(path).read_text(encoding="utf-8")
        match = re.search(r"\d{4}-\d{2}-\d{2}", content)
        if match:
            return match.group(0)
    except:
        pass
    return None


# -----------------------
# CATEGORY EXTRACTION
# -----------------------

def get_category(path):
    """Read <!-- category: writing --> style comment from file."""
    try:
        content = Path(path).read_text(encoding="utf-8")
        match = re.search(r"<!--\s*category:\s*(\w+)\s*-->", content, re.IGNORECASE)
        if match:
            cat = match.group(1).strip().lower()
            if cat in VALID_CATEGORIES:
                return cat
    except:
        pass
    return None


# -----------------------
# DESCRIPTION EXTRACTION
# -----------------------

def get_desc(path):
    """Read <!-- desc: some description --> style comment from file."""
    try:
        content = Path(path).read_text(encoding="utf-8")
        match = re.search(r"<!--\s*desc:\s*(.+?)\s*-->", content, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    except:
        pass
    return ""


# -----------------------
# CATEGORY PAGE GENERATOR
# -----------------------

CATEGORY_TITLES = {
    "writing": "— writing —",
    "making":  "— making —",
    "sensing": "— sensing —",
}

NAV_HTML = """  <nav id="topnav">
    <div id="topnav-inner">
      <a href="ABOUT.html">| about |</a>
      <span class="nav-sep">·</span>
      <a href="making.html">| making |</a>
      <span class="nav-sep">·</span>
      <a href="writing.html">| writing |</a>
      <span class="nav-sep">·</span>
      <a href="sensing.html">| sensing |</a>
      <span class="nav-sep">·</span>
      <button id="toggle-dark-mode">| dark mode |</button>
      <span class="nav-sep">·</span>
      <button onclick="goRandom()">| random |</button>
    </div>
  </nav>"""


def generate_category_pages():
    """Scan all post files for category/desc comments and rebuild category pages."""

    # Collect all categorized posts
    categories = {cat: [] for cat in VALID_CATEGORIES}

    for f in HTML_DIR.glob("*.html"):
        if f.name in EXCLUDED_PAGES:
            continue

        cat = get_category(f)
        if not cat:
            continue

        title = get_title(f)
        date  = get_post_date(f)
        desc  = get_desc(f)
        year  = date[:4] if date else ""

        categories[cat].append({
            "file":  f.name,
            "title": title,
            "date":  date or "0000-00-00",
            "desc":  desc,
            "year":  year,
        })

    # Sort each category newest first; undated sink to bottom
    for cat in categories:
        categories[cat].sort(
            key=lambda x: x["date"] if x["date"] != "0000-00-00" else "9999-99-99",
            reverse=True
        )

    # Write each category page
    SKIP_CATEGORY_PAGES = {"sensing"}

    for cat, posts in categories.items():
        if cat in SKIP_CATEGORY_PAGES:
            continue
        outfile = Path(f"{cat}.html")

        header = CATEGORY_TITLES[cat]

        if posts:
            items = []
            for p in posts:
                desc_text = p["desc"]
                if p["year"]:
                    desc_text = f"{desc_text} · {p['year']}" if desc_text else p["year"]
                items.append(
                    f'      <li>\n'
                    f'        <a href="{p["file"]}" class="entry-title">{p["title"]}</a>\n'
                    f'        <span class="entry-dots"></span>\n'
                    f'        <span class="entry-desc">{desc_text}</span>\n'
                    f'      </li>'
                )
            list_html = "\n".join(items)
            list_block = f'    <ul class="category-list">\n{list_html}\n    </ul>'
        else:
            list_block = (
                '    <p style="text-align:center;color:#999;font-size:0.9rem;margin-top:3rem;">'
                f'nothing here yet — check back soon.</p>'
            )

        page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{cat} | yesteryear forever</title>
  <link rel="stylesheet" href="style.css" />
  <script src="script.js" defer></script>
</head>
<body>

{NAV_HTML}

  <div class="container">
    <h1><a href="index.html">| yesteryear forever |</a></h1>

    <p class="category-header">{header}</p>

{list_block}

  </div>

  <div class="lightbox" id="lightbox">
    <img id="lightbox-img" src="" alt="">
  </div>

</body>
</html>
"""
        outfile.write_text(page, encoding="utf-8")
        print(f"📂 {cat}.html rebuilt ({len(posts)} posts)")


# -----------------------
# NAV UPDATER
# -----------------------

def update_nav():
    """Replace old nav blocks with the current nav in every post page."""

    # Pattern: match the entire <nav id="topnav">...</nav> block
    nav_pattern = re.compile(
        r'<nav id="topnav">.*?</nav>',
        re.DOTALL
    )

    skip = EXCLUDED_PAGES | {"making.html", "writing.html", "sensing.html", "index.html", "ABOUT.html"}

    updated_count = 0

    for f in HTML_DIR.glob("*.html"):
        if f.name in skip:
            continue

        content = f.read_text(encoding="utf-8")

        # Also fix seeing.html → sensing.html references in older navs
        content_fixed = content.replace(
            'href="seeing.html"', 'href="sensing.html"'
        ).replace(
            '>| seeing |<', '>| sensing |<'
        )

        new_content = nav_pattern.sub(NAV_HTML.strip(), content_fixed)

        if new_content != content:
            f.write_text(new_content, encoding="utf-8")
            updated_count += 1

    print(f"🧭 nav updated in {updated_count} pages")


# -----------------------
# THUMBNAIL GENERATOR
# -----------------------

def generate_thumbnails():

    if not IMAGE_DIR.exists():
        print("⚠ images directory not found")
        return

    for image_path in IMAGE_DIR.iterdir():

        if image_path.suffix.lower() not in ALLOWED_IMAGE_EXTS:
            continue

        if THUMB_SUFFIX in image_path.stem:
            continue

        thumb_name = image_path.stem + THUMB_SUFFIX + image_path.suffix
        thumb_path = IMAGE_DIR / thumb_name

        if thumb_path.exists():
            continue

        try:
            with Image.open(image_path) as img:
                img.thumbnail(THUMB_SIZE)
                img.save(thumb_path)
                print(f"🖼 thumbnail created: {thumb_name}")

        except Exception as e:
            print(f"❌ thumbnail failed: {image_path.name} — {e}")


# -----------------------
# IMAGE TAG UPDATER
# -----------------------

img_tag_pattern = re.compile(
    r'<img\s+([^>]*?)src=["\']images/([^"\']+)["\']([^>]*)>',
    re.IGNORECASE
)

def update_img_tag(match):

    before   = match.group(1)
    filename = match.group(2)
    after    = match.group(3)

    ext  = Path(filename).suffix.lower()
    stem = Path(filename).stem

    if THUMB_SUFFIX in stem or ext not in ALLOWED_IMAGE_EXTS:
        return match.group(0)

    thumb = f"{stem}{THUMB_SUFFIX}{ext}"

    if "data-full=" in match.group(0):
        return re.sub(
            r'src=["\']images/' + re.escape(filename) + r'["\']',
            f'src="images/{thumb}"',
            match.group(0)
        )
    else:
        return f'<img {before}src="images/{thumb}" data-full="images/{filename}"{after}>'


def update_image_tags():

    for html_file in HTML_DIR.glob("*.html"):

        if html_file.name in EXCLUDED_IMAGE:
            continue

        content = html_file.read_text(encoding="utf-8")
        updated = img_tag_pattern.sub(update_img_tag, content)

        if updated != content:
            html_file.write_text(updated, encoding="utf-8")
            print(f"🖼 image tags updated: {html_file.name}")


# -----------------------
# RANDOM POST LIST
# -----------------------

def update_random_posts(js_file="script.js"):

    pages = sorted([
        f.stem for f in HTML_DIR.glob("*.html")
        if f.name not in EXCLUDED_RANDOM
    ])

    pages_array = ", ".join([f'"{p}"' for p in pages])

    pattern = re.compile(
        r"(const\s+pages\s*=\s*\[)[^\]]*(\];)",
        re.DOTALL
    )

    try:
        content = Path(js_file).read_text(encoding="utf-8")
        updated = pattern.sub(rf"\1 {pages_array} \2", content)
        Path(js_file).write_text(updated, encoding="utf-8")
        print("🎲 random post list updated")
    except:
        print("⚠ script.js not found")


# -----------------------
# RSS FEED
# -----------------------

def generate_rss():

    items = []

    for file in HTML_DIR.glob("*.html"):

        if file.name in EXCLUDED_PAGES:
            continue

        title = get_title(file)
        date  = get_post_date(file)

        if not date:
            continue

        link = f"{SITE_URL}/{file.name}"
        items.append((date, title, link))

    items.sort(reverse=True)

    rss_items = []
    for date, title, link in items[:20]:
        rss_items.append(f"""
<item>
<title>{title}</title>
<link>{link}</link>
<pubDate>{date}</pubDate>
</item>
""")

    rss = f"""<?xml version="1.0" encoding="UTF-8"?>

<rss version="2.0">

<channel>

<title>Yesteryear Forever</title>
<link>{SITE_URL}</link>
<description>Personal writings, projects, and reflections</description>

{''.join(rss_items)}

</channel>

</rss>
"""
    Path("rss.xml").write_text(rss, encoding="utf-8")
    print("📰 rss.xml generated")


# -----------------------
# SITEMAP
# -----------------------

def generate_sitemap():

    urls = []

    for file in HTML_DIR.glob("*.html"):

        if file.name in EXCLUDED_SITEMAP:
            continue

        urls.append(f"""
<url>
<loc>{SITE_URL}/{file.name}</loc>
</url>
""")

    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>

<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">

{''.join(urls)}

</urlset>
"""
    Path("sitemap.xml").write_text(sitemap)
    print("🗺 sitemap.xml generated")


# -----------------------
# PERMISSIONS
# -----------------------

def fix_permissions():

    for dirpath, dirnames, filenames in os.walk(SITE_ROOT):

        os.chmod(dirpath, DIR_PERMS)

        for file in filenames:
            path = Path(dirpath) / file
            if path.suffix.lower() in MEDIA_EXTS:
                try:
                    os.chmod(path, FILE_PERMS)
                except:
                    pass


# -----------------------
# MAIN
# -----------------------

def main():

    print("\nUpdating site...\n")

    generate_thumbnails()

    update_nav()

    update_image_tags()

    update_random_posts()

    generate_category_pages()

    generate_rss()

    generate_sitemap()

    fix_permissions()

    print("\n✅ Site update complete\n")


if __name__ == "__main__":
    main()

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
THUMB_SIZE = (300, 300)

ALLOWED_IMAGE_EXTS = {".jpg",".jpeg",".png",".gif",".webp"}

MEDIA_EXTS = (
    ".html",".css",".js",
    ".jpg",".jpeg",".png",".gif",".svg",".webp",
    ".mp3",".m4a",".aac",".ogg",".wav",".flac"
)

FILE_PERMS = 0o644
DIR_PERMS = 0o755

AUDIO_SUBDIR = "audio"

EXCLUDED_ARCHIVE = {
    "template.html","index.html","mylinks.html","desiderata.html",
    "first_star.html","green_planet.html","space_index.html",
    "preamble.html","lectures.html","archive.html"
}

EXCLUDED_RANDOM = {
    "index.html","mylinks.html","template.html",
    "first_star.html","green_planet.html","space_index.html",
    "preamble.html","lectures.html","archive.html"
}

EXCLUDED_IMAGE = {
    "first_star.html","green_planet.html","space_index.html"
}


EXCLUDED_SITEMAP = {
    "template.html",
    "first_star.html",
    "green_planet.html",
    "space_index.html",
    "preamble.html",
    "lectures.html",
    "mylinks.html",
    "README.md",
    "deploy.sh",
    "desiderata.html",
    "archive.html",
    "notes.txt"
}


# -----------------------
# TITLE EXTRACTION
# -----------------------

def get_title(path):

    try:
        content = Path(path).read_text(encoding="utf-8")

        match = re.search(
            r"<title>(.*?)</title>",
            content,
            re.IGNORECASE | re.DOTALL
        )

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

        match = re.search(r"\d{4}-\d{2}-\d{2}",content)

        if match:
            return match.group(0)

    except:
        pass

    return None


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
# ARCHIVE GENERATOR
# -----------------------

def generate_archive():

    html_files = [
        f for f in os.listdir(HTML_DIR)
        if f.endswith(".html") and f not in EXCLUDED_ARCHIVE
    ]

    regular_files = [f for f in html_files if f != "links.html"]

    links = [
        f'<li><a href="{f}">{get_title(f)}</a></li>'
        for f in sorted(regular_files)
    ]

    if "links.html" in html_files:
        links.append('<li><a href="links.html" style="color:#FFFFFF">| links |</a></li>')

    archive_html = "<ul class=\"archive-list\">\n"
    archive_html += "\n".join(links)
    archive_html += "\n</ul>"

    Path("archive.html").write_text(archive_html,encoding="utf-8")

    print("📚 archive.html generated")


# -----------------------
# IMAGE TAG UPDATER
# -----------------------

img_tag_pattern = re.compile(
    r'<img\s+([^>]*?)src=["\']images/([^"\']+)["\']([^>]*)>',
    re.IGNORECASE
)

def update_img_tag(match):

    before = match.group(1)
    filename = match.group(2)
    after = match.group(3)

    ext = Path(filename).suffix.lower()
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

        updated = img_tag_pattern.sub(update_img_tag,content)

        if updated != content:

            html_file.write_text(updated,encoding="utf-8")

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

        updated = pattern.sub(rf"\1 {pages_array} \2",content)

        Path(js_file).write_text(updated,encoding="utf-8")

        print("🎲 random post list updated")

    except:
        print("⚠ script.js not found")


# -----------------------
# RSS FEED
# -----------------------

def generate_rss():

    items = []

    for file in HTML_DIR.glob("*.html"):

        if file.name in EXCLUDED_ARCHIVE:
            continue

        title = get_title(file)
        date = get_post_date(file)

        if not date:
            continue

        link = f"{SITE_URL}/{file.name}"

        items.append((date,title,link))

    items.sort(reverse=True)

    rss_items = []

    for date,title,link in items[:20]:

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
<description>Personal writings and reflections</description>

{''.join(rss_items)}

</channel>

</rss>
"""

    Path("rss.xml").write_text(rss,encoding="utf-8")

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

    for dirpath,dirnames,filenames in os.walk(SITE_ROOT):

        os.chmod(dirpath,DIR_PERMS)

        for file in filenames:

            path = Path(dirpath)/file

            if path.suffix.lower() in MEDIA_EXTS:

                try:
                    os.chmod(path,FILE_PERMS)
                except:
                    pass


# -----------------------
# MAIN
# -----------------------

def main():

    print("\nUpdating site...\n")

    generate_thumbnails()

    generate_archive()

    update_image_tags()

    update_random_posts()

    generate_rss()

    generate_sitemap()

    fix_permissions()

    print("\n✅ Site update complete\n")


if __name__ == "__main__":
    main()

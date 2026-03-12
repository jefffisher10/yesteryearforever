# yesteryearforever.xyz

A minimalist personal website.

This site is a small collection of writing, projects, images, and experiments.
It is intentionally simple: plain HTML pages, a single CSS file, and a few small Python scripts that automate repetitive tasks.

The goal is for the site to remain easy to understand, maintain, and edit by hand.

---

# Philosophy

This site avoids complex frameworks or static site generators.

Instead it uses:

* plain HTML pages
* one stylesheet
* one JavaScript file
* a small Python utility script

The result is a website that can still function even if the automation scripts are never run again.

Everything is transparent and easy to repair manually.

---

# Directory Structure

Example structure:

```
/var/www/html

index.html
about.html
template.html
archive.html

style.css
script.js

update.py

images/
audio/
```

### Important Files

**index.html**
Main landing page.

**template.html**
Template used when creating new posts.

**archive.html**
Automatically generated list of all posts.

**style.css**
Main styling for the site.

**script.js**
Handles UI features such as:

* random post button
* dark mode
* archive toggle on mobile
* image lightbox
* audio playlists

**update.py**
Utility script that automates site maintenance.

---

# Creating a New Post

1. Copy `template.html`

2. Rename it

Example:

```
my_new_post.html
```

3. Edit the title

```
<title>My New Post</title>
```

4. Write the content.

5. Add images if desired.

Images should go inside:

```
images/
```

---

# Images

Images placed in the `images/` directory will automatically get thumbnails generated when the update script is run.

Example:

```
photo.jpg
```

The script will generate:

```
photo_thumb.jpg
```

The HTML `<img>` tag will automatically be updated to use the thumbnail and open the full image in a lightbox.

---

# Running the Update Script

After adding new posts or images run:

```
python3 update.py
```

This script performs several automated tasks:

• generates image thumbnails
• updates `<img>` tags to use thumbnails
• regenerates the archive list
• updates the random post list in `script.js`
• generates `rss.xml`
• generates `sitemap.xml`
• fixes file permissions

---

# Deployment Workflow

Typical workflow:

Edit files locally.

Push changes to GitHub.

On the Raspberry Pi server:

```
cd /var/www/html
git pull
python3 update.py
```

---

# Technologies Used

The site intentionally uses very few technologies:

* HTML
* CSS
* JavaScript
* Python
* Apache

No frameworks or CMS are used.

---

# License

This project is primarily a personal website.

Content belongs to the site owner unless otherwise noted.

Code may be reused freely.
=======
# yesteryearforever.xyz

A minimalist personal website.

This site is a small collection of writing, projects, images, and experiments.
It is intentionally simple: plain HTML pages, a single CSS file, and a few small Python scripts that automate repetitive tasks.

The goal is for the site to remain easy to understand, maintain, and edit by hand.

---

# Philosophy

This site avoids complex frameworks or static site generators.

Instead it uses:

* plain HTML pages
* one stylesheet
* one JavaScript file
* a small Python utility script

The result is a website that can still function even if the automation scripts are never run again.

Everything is transparent and easy to repair manually.

---

# Directory Structure

Example structure:

```
/var/www/html

index.html
about.html
template.html
archive.html

style.css
script.js

update.py

images/
audio/
```

### Important Files

**index.html**
Main landing page.

**template.html**
Template used when creating new posts.

**archive.html**
Automatically generated list of all posts.

**style.css**
Main styling for the site.

**script.js**
Handles UI features such as:

* random post button
* dark mode
* archive toggle on mobile
* image lightbox
* audio playlists

**update.py**
Utility script that automates site maintenance.

---

# Creating a New Post

1. Copy `template.html`

2. Rename it

Example:

```
my_new_post.html
```

3. Edit the title

```
<title>My New Post</title>
```

4. Write the content.

5. Add images if desired.

Images should go inside:

```
images/
```

---

# Images

Images placed in the `images/` directory will automatically get thumbnails generated when the update script is run.

Example:

```
photo.jpg
```

The script will generate:

```
photo_thumb.jpg
```

The HTML `<img>` tag will automatically be updated to use the thumbnail and open the full image in a lightbox.

---

# Running the Update Script

After adding new posts or images run:

```
python3 update.py
```

This script performs several automated tasks:

• generates image thumbnails
• updates `<img>` tags to use thumbnails
• regenerates the archive list
• updates the random post list in `script.js`
• generates `rss.xml`
• generates `sitemap.xml`
• fixes file permissions

---

# Deployment Workflow

Typical workflow:

Edit files locally.

Push changes to GitHub.

On the Raspberry Pi server:

```
cd /var/www/html
git pull
python3 update.py
```

---

# Technologies Used

The site intentionally uses very few technologies:

* HTML
* CSS
* JavaScript
* Python
* Apache

No frameworks or CMS are used.

---

# License

This project is primarily a personal website.

Content belongs to the site owner unless otherwise noted.

Code may be reused freely.

# Heima Photo Site Rules v1.0

This document defines the stable rules for `heimaphoto.com`.

It is shared by all Codex skills and publishing workflows.

The purpose is simple:

- keep the site static
- keep the structure predictable
- keep future publishing easy
- avoid duplicated or conflicting rules between article publishing and photo publishing

Heima Photo is a personal archive for writing and photography.
It is not a CMS, not a social photo platform, and not a commercial gallery site.

---

## 1. Core Principles

1. The site must remain fully static.
2. Prefer simple HTML/CSS over JavaScript.
3. Do not introduce frameworks, build systems, databases, or runtime dependencies unless explicitly requested.
4. Keep visual style quiet, restrained, and archive-like.
5. Do not redesign existing pages unless the user explicitly asks.
6. Do not modify manual homepage blocks unless explicitly requested.

---

## 2. Main Site Structure

Expected top-level structure:

```text
/
├── index.html
├── archive.html
├── about.html
├── article/
│   └── *.html
├── category/
│   └── *.html
├── md/
│   └── *.md
├── portfolio/
│   └── index.html
├── photo/
│   └── *.html
├── images/
│   ├── article/
│   └── photo/
└── tools/
```

Notes:

- `article/` contains generated article pages.
- `photo/` contains new photo/portfolio detail pages.
- `portfolio/index.html` is the new portfolio entry page.
- Existing old portfolio/archive files must be preserved.
- The old portfolio entry must remain accessible from the new portfolio page.

---

## 3. Navigation Rules

Main navigation should remain simple.

Default visible navigation:

```text
首页
摄影作品
七种武器
归档
关于
```

Do not add new global navigation items unless explicitly requested.

The new `portfolio/index.html` should include a modest link to the old portfolio/archive as historical preservation.

Suggested wording:

```text
Old Portfolio
旧版作品入口
```

Placement may be near the page intro or page footer, but it should not dominate the new portfolio page.

---

## 4. Article Categories

Article categories use a one-level category system.

Current real categories on the live site:

```text
生活随想
看的艺术
摄影技术
建站记录
摄影笔记
七种武器
```

These are current categories, not a permanent closed list.

Future new article categories are allowed.

Rules for new article categories:

1. New categories must remain one-level only.
2. Do not create nested category structures.
3. When a new article category appears, regenerate the corresponding `category/*.html` page.
4. Update category links/summary areas where the existing article publisher already maintains them, including `about.html` if applicable.
5. Keep category display names in Chinese unless the user explicitly requests otherwise.
6. Use a stable English `category_slug` when provided.
7. If `category_slug` is not provided, generate a safe and stable slug according to the existing publisher behavior.

Important:

- Do not use old or obsolete category names from previous drafts as current truth.
- The live site and user-provided front matter are the source of truth.

---

## 5. Archive Rules

`archive.html` is the unified chronological archive.

It should include both:

- articles
- new portfolio/photo works

The archive remains simple and time-based.

Each archive entry should show:

```text
date
title
category/type
```

For normal articles:

```text
date | article title | article category
```

For new photo works:

```text
date | photo title | 摄影作品
```

Photo works should appear in archive as `摄影作品`.

Do not split archive into separate article archive and photo archive unless explicitly requested.

Do not create `category/portfolio.html`.
The portfolio system has its own entry page at:

```text
portfolio/index.html
```

---

## 6. Portfolio Rules

The new portfolio system is for selected recent photo works.

`portfolio/index.html` should be a grid entry page.

Recommended layout:

- square image grid
- desktop: 3 columns preferred
- mobile: 1 or 2 columns
- chronological order, newest first
- quiet captions
- no pagination for now

Do not mix articles into the portfolio grid.

Do not move or rewrite old portfolio pages.

Include a modest link to the old portfolio as historical preservation.

---

## 7. Photo Work Types

The new portfolio supports two internal work types:

```text
Photo
Series
```

Meaning:

- `Photo`: one main image
- `Series`: multiple images belonging to one work

These types may be shown on the photo detail page.

In `archive.html`, both types should still display as:

```text
摄影作品
```

Do not create separate archive categories for `Photo` and `Series`.

---

## 8. Photo Detail Page Rules

Photo detail pages live under:

```text
photo/<slug>.html
```

A photo detail page should feel like a quiet photography book page, not a blog post and not a gallery platform.

Required or recommended fields:

```yaml
title:
date:
type: photo | series
image:
images:        # for series
camera:
lens:
location:
description:
```

Rules:

1. The image is the visual focus.
2. For `type: photo`, show the main image first, then title, summary, metadata, detailed description, and return links.
3. For `type: series`, show title and summary first, then photo 1, photo 2, and subsequent images, then metadata, detailed description, and return links.
4. Text should be restrained.
5. Metadata may include date, camera, lens, and location.
6. Missing optional metadata should simply not render.
7. Do not render empty labels.
8. `description` is a plain text summary and should not contain HTML.
9. Body content after the front matter is an optional detailed description; preserve simple Markdown or simple HTML formatting on the photo detail page.
10. Use the site's existing lightweight `lightbox.js` effect for photo detail images, including click-to-enlarge and previous/next navigation for multi-image works. Do not add separate page-level slideshows, carousel components, masonry layouts, or heavy JavaScript unless explicitly requested.
11. For series pages, prefer vertical large images over complex gallery widgets.

---

## 9. Image Rules

If the user provides already processed web images:

- accept JPG images directly
- recommended long edge: about 1600 px
- do not reprocess unless requested

If Codex is asked to process source images:

- export web image as JPG
- long edge: about 1600 px
- quality: around 80–85
- preserve reasonable color appearance
- do not upload original full-resolution files unless requested

For the first version of the new portfolio system:

- do not require separate thumbnails
- portfolio grid may use the same 1600 px web image with CSS square cropping

Future optimization may add generated thumbnails, but do not introduce that complexity now.

---

## 10. Manual Blocks

Do not modify homepage manual blocks unless explicitly requested.

Known manual blocks:

```text
MANUAL-RECOMMENDATIONS
MANUAL-FEATURED-PHOTOS
```

The article publisher must preserve them.

The photo publisher must also avoid changing them unless the user explicitly asks to update featured homepage photos.

---

## 11. URL and Slug Rules

Article pages:

```text
article/<slug>.html
```

Photo pages:

```text
photo/<slug>.html
```

Rules:

1. Use stable English slugs.
2. Use lowercase letters, numbers, and hyphens.
3. Avoid spaces, Chinese characters, punctuation, and date prefixes unless the existing site already requires them.
4. Do not rename existing published pages unless explicitly requested.

---

## 12. Publishing Responsibility Split

Article publishing skill handles:

- markdown article source under `md/`
- article page generation
- homepage article list updates
- archive article entries
- category pages
- about page category links when needed

Photo publishing skill handles:

- new photo detail pages
- portfolio grid updates
- archive portfolio entries
- optional image placement under `images/photo/`

Shared rules live here.

Do not duplicate these shared site rules inside each skill except as short references.

---

## 13. Skill Source and Installation Rules

The repository `skills/` directory is the source of truth for Heima Photo skills.

Installed Codex skills under:

```text
~/.codex/skills/
```

are runtime copies only.

Rules:

1. When changing a Heima Photo skill, update the repository copy first.
2. After editing repository skills, run:

```text
python3 tools/install_skills.py
```

3. Do not edit only the installed copy and leave the repository copy stale.
4. If an installed skill was changed directly during emergency work, copy the change back into `skills/` before finishing.
5. When a task changes publishing behavior, navigation labels, category names, portfolio rules, Gear/七种武器 rules, or skill instructions, update the repository skill files and `skills/site-rules.md` first, then sync them to the installed skills directory before finishing.
6. The install script must copy `skills/site-rules.md` into each installed Heima Photo skill directory as `site-rules.md`.
7. After syncing, verify installed skill files and installed `site-rules.md` copies match the repository sources with `diff -rq`.

---

## 14. Gear / 七种武器 Rules

`gear.html` is the single entry page for Gear/七种武器 articles.

Current display name:

```text
七种武器
```

Compatibility aliases that map to the same `gear` slug may remain in the publisher:

```text
器材
工具
七种武器
```

Rules:

1. Gear/七种武器 articles should use `category: 七种武器`.
2. Gear/七种武器 article archive labels should link to `gear.html`.
3. Do not generate `category/gear.html`.
4. The `gear.html` photo wall should include real Gear/七种武器 articles that have a `thumbnail`.
5. Sort Gear/七种武器 photo wall items newest first.

---

## 15. Compatibility Rules

1. Preserve existing working structure.
2. Prefer minimal changes.
3. Do not rewrite the whole site.
4. Do not modify old portfolio files.
5. Do not change category naming unless the user explicitly requests it.
6. Do not introduce pagination for portfolio at current scale.
7. Do not create duplicate systems for the same purpose.

---

## 16. Current Design Direction

The new portfolio and photo pages should feel:

```text
minimal
quiet
high-end but not commercial
archive-like
photo-first
text-light
```

Avoid:

```text
busy cards
heavy borders
large shadows
sliders
masonry layout
over-designed hover effects
commercial studio style
```

The site should feel like a long-term personal archive, not a temporary template.

---
name: heimaphoto-photo-publisher
description: Publish new photo/portfolio works for heimaphoto.com. Use when the user asks to publish a new Heima Photo portfolio work, photo page, or series page.
metadata:
  short-description: Publish Heima Photo portfolio works
---

# Heima Photo Photo Publisher

Use this skill to publish new photo works on `heimaphoto.com`.

This skill must follow:

```text
site-rules.md
```

If this skill conflicts with `site-rules.md`, follow `site-rules.md`.

---

## Purpose

Publish a new portfolio work while preserving the existing static site.

A portfolio work may be:

```text
Photo
Series
```

Both appear in `archive.html` as:

```text
摄影作品
```

Do not create `category/portfolio.html`.

Do not modify old portfolio files.

---

## Required Inputs

For a single photo work:

```yaml
source_image:
slug:
title:
date:
type: photo
camera:
lens:
location:
description: 一句纯文本摘要
```

For a series work:

```yaml
source_images:
slug:
title:
date:
type: series
camera:
lens:
location:
description: 一句纯文本摘要
```

Optional fields may be blank.

Only render optional metadata when it exists.

`description` is a plain text summary. Do not put HTML in this field.

Any body content after the front matter is an optional detailed description. Render it on the photo detail page and preserve simple Markdown or simple HTML formatting.

---

## Image Handling

If the user provides an already processed web image:

1. Use it directly.
2. Assume recommended long edge is about 1600 px.
3. Do not reprocess unless requested.

If the user asks Codex to process the image:

1. Export JPG.
2. Resize long edge to about 1600 px.
3. Use quality around 80–85.
4. Save under the photo image folder used by the repository.

For the first version, do not generate separate thumbnails unless the user explicitly requests it.

The portfolio grid may use the same web image with CSS square cropping.

---

## Generated / Updated Files

When publishing a new portfolio work, update or create:

```text
photo/<slug>.html
portfolio/index.html
archive.html
```

When `camera`, `lens`, or `film` metadata matches an existing Gear slug, also update:

```text
md/<gear-source>.md
article/<gear-source>.html
gear.html
```

If needed, place images under:

```text
images/photo/
```

or the existing photo image path used by the site.

Do not update:

```text
category/*.html
```

for portfolio works.

Do not update homepage manual blocks unless the user explicitly asks.

Known homepage manual blocks:

```text
MANUAL-RECOMMENDATIONS
MANUAL-FEATURED-PHOTOS
```

## Workflow

1. Create or confirm a source file under `photo-md/`.
2. Ignore `_*.md` templates.
3. Run:

```bash
python3 tools/publish_photo.py photo-md/example.md
```

The photo publisher shares archive and portfolio rendering with the article publisher so the two systems do not overwrite each other's index entries.

It also shares Gear `Published Work` maintenance with the article publisher. A photo work can link back to Gear pages through `camera`, `lens`, or `film` metadata using the same exact slug rules described below.

The command must finish with the validation message:

```text
Validated photo work in photo/, portfolio/index.html and archive.html
```

If validation fails, do not finish the task. Fix the missing generated output and rerun the command until the validation passes.

---

## Photo Detail Page

Create a quiet photo-first detail page.

Required page behavior:

1. For `type: photo`, show the main image first, then title, summary, metadata, detailed description, and return links.
2. For `type: series`, show title and summary first, then photo 1, photo 2, and subsequent images, then metadata, detailed description, and return links.
3. Show metadata only when available.
4. If the source markdown has body content after the front matter, render it as the detailed description.
5. Include a return link to `portfolio/index.html`.
6. Keep layout consistent with the site style.
7. Keep the existing lightweight `lightbox.js` effect on photo detail images, including click-to-enlarge and previous/next navigation for multi-image works. Avoid separate page-level slideshows, carousel components, masonry scripts, and other heavy JavaScript.

Suggested metadata:

```text
Date
Camera
Lens
Location
```

## Gear Published Work Links

Photo work metadata can link back to Gear pages through these fields only:

```yaml
camera:
lens:
film:
```

Match values case-insensitively as exact Gear slugs. Slugs should be written as lowercase kebab-case in new source files, for example `iphone-air`, `rx1rm2`, `planar-50`, or `fomapan-100`; existing mixed-case values still match after normalization. Do not use spaces, display names, Chinese names, or concatenated display names such as `iPhoneAir` for new metadata.

Do not match against titles, image names, product display names, body text, `related`, `thumbnail`, `description`, or loose substrings. Gear slugs are derived from Gear article source filenames by stripping the leading numeric prefix and an optional `gear-` prefix, for example `md/78-gear-rx1rm2.md` maps to `rx1rm2`, and `md/65-gear-iphone-air.md` maps to `iphone-air`.

When publishing a photo work, the publisher should update only the Gear pages referenced by that source metadata, plus any Gear page that already links to that photo work so stale links can be removed. When publishing a Gear article or doing an initialization pass through the article publisher, rebuild that Gear article's `### Published Work` entries from all existing articles and photo works.

On generated photo work pages, displayed `camera`, `lens`, and `film` metadata values should link back to the matched Gear article page. Keep the displayed value from the source metadata, but wrap it with the Gear detail URL when a match exists. Leave unmatched values as plain text.

`Published Work` rows are markdown links in newest-first order:

```markdown
[2026-07-01 Photo Work Title](../photo/example.html)
```

Keep existing manual content in the `Published Work` section. Do not create new Gear pages or empty links when a metadata value is blank or unmatched.

---

## Portfolio Page

`portfolio/index.html` is the new portfolio entry page.

Rules:

1. Show selected portfolio works in a square image grid.
2. Sort newest first.
3. Desktop layout should prefer 3 columns.
4. Mobile should adapt to 1 or 2 columns.
5. Use quiet captions.
6. Do not add pagination.
7. Include a modest link to the old portfolio as historical preservation.

Suggested old portfolio link text:

```text
旧版作品入口 / Old Portfolio
```

Do not modify the old portfolio files.

---

## Archive Update

Add the new portfolio work to `archive.html`.

Archive entry should use:

```text
date | title | 摄影作品
```

Do not display `Photo` or `Series` in archive.

Those types are only for the portfolio detail page.

---

## Validation Checklist

Before finishing:

1. Confirm `python3 tools/publish_photo.py photo-md/example.md` ended with the validation message.
2. Confirm `photo/<slug>.html` exists and opens.
3. Confirm `portfolio/index.html` includes the new work.
4. Confirm `archive.html` includes the new work with category/type `摄影作品`.
5. If `camera`, `lens`, or `film` metadata matches Gear, confirm the affected Gear source and `article/<gear-source>.html` include the photo work under `Published Work`, and the photo detail metadata links back to the Gear article page.
6. Confirm no `category/portfolio.html` was created.
7. Confirm old portfolio files were not modified.
8. Confirm homepage manual blocks were not modified unless explicitly requested.
9. Confirm missing optional metadata does not produce empty labels.
10. Confirm links are relative and work on GitHub Pages.

---

## User Command Examples

Example single photo:

```text
请使用「Heima Photo Photo Publisher」发布作品：

source_image: images/source/milk-tea.jpg
slug: milk-tea
title: Milk Tea
date: 2026-06-15
type: photo
camera: Leica M262
lens: Voigtländer 40mm F1.4
location: Shanghai
description: 奶茶并不重要，重要的是那个下午的光。
```

Optional body content after the front matter may contain a longer note:

```md
---
description: 一句纯文本摘要。
---

这里写更详细的说明，支持简单 Markdown。

<p>少量 HTML 也可以保留。</p>
```

Example series:

```text
请使用「Heima Photo Photo Publisher」发布组图：

source_images:
- images/source/shanghai-night-01.jpg
- images/source/shanghai-night-02.jpg
- images/source/shanghai-night-03.jpg
slug: shanghai-night
title: Shanghai Night
date: 2026-06-15
type: series
camera: Leica M262
lens: Voigtländer 40mm F1.4
location: Shanghai
description: 雨后的城市有一种很短暂的安静。
```

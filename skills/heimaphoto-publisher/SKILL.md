---
name: heimaphoto-publisher
description: Publish articles for heimaphoto.com from /md/*.md files. Use when the user says “请发布 /md/xxx.md”, asks to publish a Heima Photo article, or needs index/archive/category/article pages regenerated for the static Heima Photo site.
metadata:
  short-description: Publish Heima Photo markdown articles
---

# Heima Photo Publisher

This skill must follow `site-rules.md`. If this skill conflicts with `site-rules.md`, follow `site-rules.md`. New portfolio work is handled by the separate `heimaphoto-photo-publisher` skill.

Use this skill to publish a new static article on `heimaphoto.com`.

## Workflow

1. Work from the Heima Photo repository root.
2. Confirm the requested source file is under `md/`, is not named with a leading `_`, and uses YAML front matter.
3. If the user needs a starting point, use `md/_template.md`. The publisher ignores `_*.md` files.
4. Run:

```bash
python3 tools/publish_article.py md/example.md
```

When a target `md/example.md` is provided, the publisher indexes all `md/*.md` files for homepage/archive/category/Gear pages, but only rewrites the target `article/example.html`. The article URL always comes from the Markdown filename (not its `title`), so a filename such as `72-rx1rm2-test.md` keeps the URL `article/72-rx1rm2-test.html` even when its visible title omits `72-`. This preserves any manual edits made to older generated article HTML. A full rebuild without a target may rewrite all article pages.

5. Verify the generated files:
   - `article/<slug>.html`
   - `index.html`
   - `archive.html`
   - `category/*.html`
   - `gear.html` and affected Gear article pages when article or photo work `camera`, `lens`, or `film` metadata is present
   - `about.html` category links if categories changed
6. Do not automatically edit the homepage manual blocks:
   - `MANUAL-RECOMMENDATIONS`
   - `MANUAL-FEATURED-PHOTOS`
7. Do not modify the old portfolio files. The new `portfolio/index.html` is only an entry point to the existing portfolio archive.

## Article Format

Required front matter fields:

```yaml
title:
date:
category:
summary:
```

Recommended:

```yaml
lead:
```

Optional:

```yaml
category_slug:
location:
camera:
lens:
film:
thumbnail:
gallery:
related:
```

Known category slugs:

```yaml
生活随想: prose
摄影/看的艺术: TheArtOfSeeing
摄影/技术: technology
摄影: photography
七种武器: gear
建站: website
生活: life
养猫日记: Cat
```

Legacy aliases may still be accepted by the publisher for compatibility, including `散文`, `器材`, and `工具`, but new source files should use the current display names from `site-rules.md`.

Only render optional sections when data exists. `summary` is for homepage cards only; article pages use `lead`. Homepage featured photos are preserved by the manual block when publishing; do not assume or add homepage lightbox behavior.

## Markdown Body Support

Article body Markdown supports simple paragraphs, headings, images, blockquotes, links, and unordered lists.

Unordered list rules are intentionally small:

```markdown
- First-level item
- First-level item
  - Second-level item
  - Second-level item
```

Only `- ` at the start of a line creates a first-level bullet. Two leading spaces followed by `- ` creates a second-level bullet under the previous first-level item. Lists are limited to two levels; do not rely on `*`, `+`, ordered lists, or deeper indentation.

## Gear Published Work Links

Article and photo work metadata can link back to Gear pages through these fields only:

```yaml
camera:
lens:
film:
```

Match values case-insensitively as exact Gear slugs. Slugs should be written as lowercase kebab-case in new source files, for example `iphone-air`, `rx1rm2`, `planar-50`, or `fomapan-100`; existing mixed-case values still match after normalization. Do not use spaces, display names, Chinese names, or concatenated display names such as `iPhoneAir` for new metadata.

Do not match against titles, image names, product display names, body text, `related`, `thumbnail`, or loose substrings. Gear slugs are derived from Gear source filenames by stripping the leading numeric prefix and an optional `gear-` prefix, for example `md/78-gear-rx1rm2.md` maps to `rx1rm2`, and `md/65-gear-iphone-air.md` maps to `iphone-air`.

When publishing a normal article or a photo work, the publisher should update only the Gear pages referenced by that source metadata, plus any Gear page that already links to that source so stale links can be removed. When publishing a Gear article or doing an initialization pass, rebuild that Gear article's `### Published Work` entries from all existing articles and photo works.

On generated article and photo work pages, displayed `camera`, `lens`, and `film` metadata values should link back to the matched Gear article page. Keep the displayed value from the source metadata, but wrap it with the Gear detail URL when a match exists. Leave unmatched values as plain text.

`Published Work` rows are markdown links in newest-first order:

```markdown
[2026-08-12 Article Title](../article/example.html)
[2026-07-01 Photo Work Title](../photo/example.html)
```

Keep existing manual content in the `Published Work` section. Do not create new Gear pages or empty links when a metadata value is blank or unmatched.

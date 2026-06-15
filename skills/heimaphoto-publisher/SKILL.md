---
name: heimaphoto-publisher
description: Publish articles for heimaphoto.com from /md/*.md files. Use when the user says “请发布 /md/xxx.md”, asks to publish a Heima Photo article, or needs index/archive/category/article pages regenerated for the static Heima Photo site.
metadata:
  short-description: Publish Heima Photo markdown articles
---

# Heima Photo Publisher

This skill must follow `skills/site-rules.md`. If this skill conflicts with `site-rules.md`, follow `site-rules.md`. New portfolio work is handled by the separate `heimaphoto-photo-publisher` skill.

Use this skill to publish a new static article on `heimaphoto.com`.

## Workflow

1. Work from the Heima Photo repository root.
2. Confirm the requested source file is under `md/`, is not named with a leading `_`, and uses YAML front matter.
3. If the user needs a starting point, use `md/_template.md`. The publisher ignores `_*.md` files.
4. Run:

```bash
python3 tools/publish_article.py md/example.md
```

5. Verify the generated files:
   - `article/<slug>.html`
   - `index.html`
   - `archive.html`
   - `category/*.html`
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
thumbnail:
gallery:
related:
```

Known category slugs:

```yaml
散文: prose
摄影/看的艺术: TheArtOfSeeing
摄影/技术: technology
摄影: photography
器材: gear
建站: website
生活: life
```

Only render optional sections when data exists. `summary` is for homepage cards only; article pages use `lead`. Homepage featured photos use a small native lightbox and are preserved by the manual block when publishing.

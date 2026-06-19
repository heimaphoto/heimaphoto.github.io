#!/usr/bin/env python3
import hashlib
import html
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MD_DIR = ROOT / "md"
PHOTO_MD_DIR = ROOT / "photo-md"
ARTICLE_DIR = ROOT / "article"
CATEGORY_DIR = ROOT / "category"
PHOTO_DIR = ROOT / "photo"

SITE_TITLE = "Heima Photo"
DESCRIPTION = "Heima Photo：摄影、文字、器材与一些安静的好奇心。"
CATEGORY_SLUGS = {
    "散文": "prose",
    "摄影": "photography",
    "摄影笔记": "Photography",
    "看的艺术": "TheArtOfSeeing",
    "摄影技术": "technology",
    "器材": "gear",
    "工具": "gear",
    "建站": "website",
    "建站记录": "site",
    "生活": "life",
}
CATEGORY_EN = {
    "散文": "Prose",
    "摄影": "Photography",
    "摄影笔记": "Photography",
    "看的艺术": "The Art Of Seeing",
    "摄影技术": "Technology",
    "器材": "Gear",
    "工具": "Gear",
    "建站": "Website",
    "建站记录": "Site",
    "生活": "Life",
}
DEFAULT_CATEGORIES = ["散文", "看的艺术", "摄影技术"]


def esc(value):
    return html.escape(str(value or ""), quote=True)


def render_inline(text):
    parts = []
    pos = 0
    for match in re.finditer(r"\[([^\]]+)\]\(([^)\s]+)\)", text):
        parts.append(esc(text[pos : match.start()]))
        label, href = match.groups()
        parts.append(f'<a href="{esc(href)}">{esc(label)}</a>')
        pos = match.end()
    parts.append(esc(text[pos:]))
    return "".join(parts)


def is_external_href(href):
    if href.startswith("//"):
        return True
    match = re.match(r"^https?://([^/#?:]+)", href, re.I)
    if not match:
        return False
    return match.group(1).lower() not in {"heimaphoto.com", "www.heimaphoto.com"}


def prepare_article_body_links(body):
    def replace(match):
        attrs = match.group(1)
        href_match = re.search(r'\shref=(["\'])(.*?)\1', attrs, re.I)
        if not href_match or not is_external_href(href_match.group(2)):
            return match.group(0)
        if re.search(r"\starget=", attrs, re.I):
            updated = re.sub(r'\starget=(["\']).*?\1', ' target="_blank"', attrs, count=1, flags=re.I)
        else:
            updated = attrs + ' target="_blank"'
        if re.search(r"\srel=", updated, re.I):
            updated = re.sub(r'\srel=(["\']).*?\1', ' rel="noopener noreferrer"', updated, count=1, flags=re.I)
        else:
            updated += ' rel="noopener noreferrer"'
        return f"<a{updated}>"

    return re.sub(r"<a\b([^>]*)>", replace, body, flags=re.I)


def slugify(value):
    known = CATEGORY_SLUGS.get(value)
    if known:
        return known
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if slug:
        return slug
    return "category-" + hashlib.sha1(value.encode("utf-8")).hexdigest()[:8]


def read_front_matter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path} 缺少 YAML front matter")
    end = text.find("\n---", 4)
    if end == -1:
        raise ValueError(f"{path} front matter 没有结束标记")
    raw = text[4:end].splitlines()
    body = text[end + 4 :].lstrip()
    data = {}
    key = None
    current_item = None

    def scalar(value):
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] == '"':
            return value[1:-1].replace('\\"', '"').replace("\\\\", "\\")
        return value

    for line in raw:
        if not line.strip():
            continue
        if not line.startswith(" "):
            key, value = line.split(":", 1)
            key = key.strip()
            value = scalar(value)
            if value:
                data[key] = value
            else:
                data[key] = []
            current_item = None
            continue
        if key is None:
            continue
        stripped = line.strip()
        if stripped.startswith("- "):
            item = stripped[2:]
            if ":" in item:
                k, v = item.split(":", 1)
                current_item = {k.strip(): scalar(v)}
                data[key].append(current_item)
            else:
                current_item = None
                data[key].append(scalar(item))
        elif current_item is not None and ":" in stripped:
            k, v = stripped.split(":", 1)
            current_item[k.strip()] = scalar(v)
    return data, body


def markdown_to_html(markdown, title):
    if markdown.lstrip().startswith("<"):
        return markdown.strip()
    blocks = []
    paragraph = []
    quote = []
    lines = markdown.splitlines()

    def flush_paragraph():
        nonlocal paragraph
        if paragraph:
            blocks.append("<p>" + "<br>\n".join(render_inline(x) for x in paragraph) + "</p>")
            paragraph = []

    def flush_quote():
        nonlocal quote
        if quote:
            blocks.append("<blockquote><p>" + "<br>\n".join(render_inline(x) for x in quote) + "</p></blockquote>")
            quote = []

    def flush():
        flush_paragraph()
        flush_quote()

    for line in lines:
        stripped = line.strip()
        if not stripped:
            flush()
            continue
        if stripped.startswith("<"):
            flush()
            blocks.append(stripped)
            continue
        inline_image = re.match(r"^\{\{\s*image:\s*(.+?)\s*\}\}$", stripped)
        if inline_image:
            flush()
            raw = inline_image.group(1).strip()
            if "|" in raw:
                src, caption = [part.strip() for part in raw.split("|", 1)]
            else:
                src, caption = raw, ""
            if caption:
                blocks.append(
                    '<figure><img src="{src}" alt="{caption}"><figcaption>{caption}</figcaption></figure>'.format(
                        src=esc(src), caption=esc(caption)
                    )
                )
            else:
                blocks.append(f'<figure><img src="{esc(src)}" alt=""></figure>')
            continue
        image = re.match(r"!\[(.*?)\]\((.*?)\)", stripped)
        if image:
            flush()
            alt, src = image.groups()
            blocks.append(
                '<figure><img src="{src}" alt="{alt}"><figcaption>{alt}</figcaption></figure>'.format(
                    src=esc(src), alt=esc(alt)
                )
            )
            continue
        blockquote = re.match(r"^>\s?(.*)$", stripped)
        if blockquote:
            flush_paragraph()
            quote.append(blockquote.group(1))
            continue
        heading = re.match(r"^(#{2,4})\s+(.+)$", stripped)
        if heading:
            flush()
            level = min(len(heading.group(1)), 3)
            text = heading.group(2).strip()
            if not blocks and text == title:
                continue
            blocks.append(f"<h{level}>{render_inline(text)}</h{level}>")
            continue
        flush_quote()
        paragraph.append(stripped)
    flush()
    return "\n".join(blocks)


def parse_article(path):
    data, body = read_front_matter(path)
    for field in ("title", "date", "category", "summary"):
        if not data.get(field):
            raise ValueError(f"{path} 缺少必填字段 {field}")
    date = datetime.strptime(data["date"], "%Y-%m-%d")
    slug = path.stem
    return {
        "source": path,
        "slug": slug,
        "url": f"article/{slug}.html",
        "article_href": f"{slug}.html",
        "title": data["title"],
        "date": date,
        "category": data["category"],
        "category_slug": data.get("category_slug", slugify(data["category"])),
        "summary": data["summary"],
        "lead": data.get("lead", ""),
        "location": data.get("location", ""),
        "camera": data.get("camera", ""),
        "thumbnail": data.get("thumbnail", ""),
        "gear_note": data.get("gear_note", ""),
        "gallery": data.get("gallery", []),
        "related": data.get("related", []),
        "body": prepare_article_body_links(markdown_to_html(body, data["title"])),
    }


def photo_image_path(path):
    if not path:
        return ""
    if path.startswith("../") or path.startswith("http://") or path.startswith("https://"):
        return path
    if path.startswith("images/") or path.startswith("img/"):
        return "../" + path
    return path


def parse_photo_work(path):
    data, body = read_front_matter(path)
    for field in ("title", "date", "type"):
        if not data.get(field):
            raise ValueError(f"{path} 缺少必填字段 {field}")
    slug = data.get("slug") or path.stem
    date = datetime.strptime(data["date"], "%Y-%m-%d")
    work_type = data["type"].lower()
    if work_type not in ("photo", "series"):
        raise ValueError(f"{path} type 必须是 photo 或 series")
    images = data.get("images") or data.get("source_images") or []
    image = data.get("image") or data.get("source_image") or ""
    if image and image not in images:
        images = [image] + images
    images = [photo_image_path(item) for item in images if item]
    if not images:
        raise ValueError(f"{path} 至少需要 image/source_image 或 images/source_images")
    detail = markdown_to_html(body, data["title"]) if body.strip() else ""
    return {
        "source": path,
        "slug": slug,
        "url": f"photo/{slug}.html",
        "photo_href": f"{slug}.html",
        "title": data["title"],
        "date": date,
        "date_display": data.get("date_display", ""),
        "type": work_type,
        "image": images[0],
        "images": images,
        "camera": data.get("camera", ""),
        "lens": data.get("lens", ""),
        "location": data.get("location", ""),
        "description": data.get("description", ""),
        "detail": detail,
    }


def root_image_path(path):
    return path[3:] if path.startswith("../") else path


def header(active="", depth=0):
    p = "../" * depth
    items = [
        ("index.html", "首页", "index"),
        ("archive.html", "归档", "archive"),
        ("portfolio/index.html", "Portfolio", "portfolio"),
        ("gear.html", "工具", "gear"),
        ("about.html", "关于", "about"),
    ]
    links = []
    for href, label, key in items:
        current = ' aria-current="page"' if active == key else ""
        links.append(f'      <a href="{p}{href}"{current}>{label}</a>')
    return f"""<header class="site-header">
  <div class="wrap header-inner">
    <a class="site-title" href="{p}index.html">HEIMA PHOTO</a>
    <nav class="site-nav" aria-label="主导航">
{chr(10).join(links)}
    </nav>
  </div>
</header>"""


def footer(depth=0):
    return f"""<footer class="site-footer">
  <div class="wrap">
    <p>© {datetime.now().year} Heima Photo. Built quietly with static HTML.</p>
  </div>
</footer>"""


def page(title, body, active="", depth=0, description=DESCRIPTION):
    css = "../" * depth + "stylesheets/style.css"
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <link rel="stylesheet" href="{css}">
</head>
<body>
{header(active, depth)}
{body}
{footer(depth)}
</body>
</html>
"""


def preserve_block(path, start, end, fallback):
    if not path.exists():
        return fallback
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(start) + r"(.*?)" + re.escape(end), re.S)
    match = pattern.search(text)
    if not match:
        return fallback
    return start + match.group(1) + end


def render_post_card(article):
    meta = f'{article["date"].strftime("%Y.%m.%d")} · {article["category"]}'
    thumb = article.get("thumbnail")
    if thumb:
        return f"""        <article class="post-card with-image">
          <a href="{article['url']}"><img src="{esc(root_image_path(thumb))}" alt=""></a>
          <div>
            <p class="meta">{esc(meta)}</p>
            <h3><a href="{article['url']}">{esc(article['title'])}</a></h3>
            <p>{esc(article['summary'])}</p>
          </div>
        </article>"""
    return f"""        <article class="post-card">
          <p class="meta">{esc(meta)}</p>
          <h3><a href="{article['url']}">{esc(article['title'])}</a></h3>
          <p>{esc(article['summary'])}</p>
        </article>"""


def render_index(articles):
    latest = "\n\n".join(render_post_card(a) for a in articles[:5])
    hero = preserve_block(
        ROOT / "index.html",
        "<!-- MANUAL-HERO:START -->",
        "<!-- MANUAL-HERO:END -->",
        """<!-- MANUAL-HERO:START -->
      <img src="img/photo/Milk-Tea.jpg" alt="Heima Photo featured photograph">
      <figcaption>Latest light, quiet frame.</figcaption>
      <!-- MANUAL-HERO:END -->""",
    )
    recommendations = preserve_block(
        ROOT / "index.html",
        "<!-- MANUAL-RECOMMENDATIONS:START -->",
        "<!-- MANUAL-RECOMMENDATIONS:END -->",
        """<!-- MANUAL-RECOMMENDATIONS:START -->
      <li><a href="article/48-prose.html">上海的夜晚</a><span>散文 / 摄影</span></li>
      <li><a href="article/post/44-prose.htm">棚拍日记</a><span>旧文档案</span></li>
      <li><a href="article/post/7-prose.htm">赶集</a><span>旧文档案</span></li>
      <!-- MANUAL-RECOMMENDATIONS:END -->""",
    )
    photos = preserve_block(
        ROOT / "index.html",
        "<!-- MANUAL-FEATURED-PHOTOS:START -->",
        "<!-- MANUAL-FEATURED-PHOTOS:END -->",
        """<!-- MANUAL-FEATURED-PHOTOS:START -->
      <a href="portfolio/index.html"><img src="img/photo/Milk-Tea.jpg" alt="Milk Tea"></a>
      <a href="portfolio/index.html"><img src="img/photo/By-the-park-lake.jpg" alt="By the park lake"></a>
      <a href="portfolio/index.html"><img src="img/photo/On-a-rainy-road.jpg" alt="On a rainy road"></a>
      <a href="portfolio/index.html"><img src="img/photo/shanghai-night.jpg" alt="Shanghai night"></a>
      <!-- MANUAL-FEATURED-PHOTOS:END -->""",
    )
    body = f"""<main>
  <section class="hero wrap">
    <div class="hero-text">
      <p class="eyebrow">Personal Archive</p>
      <h1>Photographs, Notes and Quiet Experiments.</h1>
      <p class="intro">这里保存一些照片、文字、器材折腾，以及我对日常生活的观察。摄影是入口，文字是线索，最后留下来的大概是一个人的观看方式。</p>
    </div>
    <figure class="hero-image">
{hero}
    </figure>
  </section>

  <section class="wrap main-layout">
    <section class="content">
      <div class="section-heading">
        <h2>最新文章</h2>
        <a href="archive.html">查看归档 →</a>
      </div>
      <div class="post-list">
{latest}
      </div>
    </section>
    <aside class="sidebar">
      <section class="side-card">
        <h2>关于这里</h2>
        <p>一个缓慢更新的个人档案馆。</p>
        <p>保存照片、文字与时间留下的痕迹。</p>
        <a class="text-link" href="about.html">更多关于这里 →</a>
      </section>
      <section class="side-card">
        <h2>推荐文章</h2>
        <ul class="recommend-list">
{recommendations}
        </ul>
      </section>
    </aside>
  </section>

  <section class="portfolio-strip wrap">
    <div class="section-heading">
      <h2>精选照片</h2>
      <a href="portfolio/index.html">进入 Portfolio →</a>
    </div>
    <div class="photo-grid">
{photos}
    </div>
  </section>

  <section class="wrap closing-note">
    <p>A personal archive of photographs, notes and curiosities.</p>
  </section>
</main>
"""
    return page(f"{SITE_TITLE} — Photographs, Notes and Quiet Experiments", body, "index")


def grouped(articles):
    years = defaultdict(list)
    for article in articles:
        years[article["date"].year].append(article)
    return dict(sorted(years.items(), reverse=True))


def archive_entries(articles, photo_works):
    entries = []
    for article in articles:
        entries.append(
            {
                "date": article["date"],
                "title": article["title"],
                "url": article["url"],
                "label": article["category"],
                "label_url": f"category/{article['category_slug']}.html",
                "kind": "article",
            }
        )
    for work in photo_works:
        entries.append(
            {
                "date": work["date"],
                "display_date": work.get("date_display", ""),
                "title": work["title"],
                "url": work["url"],
                "label": "Portfolio",
                "label_url": "",
                "kind": "portfolio",
            }
        )
    entries.sort(key=lambda item: item["date"], reverse=True)
    return entries


def render_category_sidebar(categories):
    rows = []
    for cat in categories:
        rows.append(
            f'      <li><a href="category/{slugify(cat)}.html">{esc(cat)}</a><span>{esc(CATEGORY_EN.get(cat, slugify(cat)))}</span></li>'
        )
    return "\n".join(rows)


def render_archive(articles, categories, photo_works=None):
    photo_works = photo_works or []
    sections = []
    for year, rows in grouped(archive_entries(articles, photo_works)).items():
        items = []
        for a in rows:
            label = (
                f'<a class="item-category" href="{a["label_url"]}">{esc(a["label"])}</a>'
                if a.get("label_url")
                else f'<span class="item-category">{esc(a["label"])}</span>'
            )
            items.append(
                f"""        <li>
          <time>{esc(a.get('display_date') or a['date'].strftime('%m.%d'))}</time>
          <a href="{a['url']}">{esc(a['title'])}</a>
          {label}
        </li>"""
            )
        sections.append(f"      <h2>{year}</h2>\n      <ul>\n{chr(10).join(items)}\n      </ul>")
    body = f"""<main>
  <section class="wrap page-title">
    <p class="eyebrow">Archive</p>
    <h1>归档</h1>
    <p>文章与作品都放在这里。首页只放最近几篇，归档负责长期保存。</p>
  </section>
  <section class="wrap main-layout">
    <div class="compact-list">
{chr(10).join(sections)}
    </div>
    <aside class="sidebar">
      <section class="side-card">
        <h2>分类</h2>
        <ul class="category-list">
{render_category_sidebar(categories)}
        </ul>
      </section>
    </aside>
  </section>
</main>"""
    return page(f"归档 — {SITE_TITLE}", body, "archive")


def render_category_page(category, articles):
    sections = []
    for year, rows in grouped(articles).items():
        items = [
            f'        <li><time>{a["date"].strftime("%m.%d")}</time><a href="../{a["url"]}">{esc(a["title"])}</a></li>'
            for a in rows
        ]
        sections.append(f"      <h2>{year}</h2>\n      <ul>\n{chr(10).join(items)}\n      </ul>")
    empty = "      <p class=\"empty-note\">这个分类下暂时还没有文章。</p>" if not sections else ""
    body = f"""<main>
  <section class="narrow page-title">
    <p class="eyebrow">Category</p>
    <h1>{esc(category)}</h1>
  </section>
  <section class="narrow single-column-page">
    <div class="compact-list category-archive">
{chr(10).join(sections)}
{empty}
    </div>
  </section>
</main>"""
    return page(f"{category} — {SITE_TITLE}", body, depth=1, description=f"Heima Photo {category} 分类文章。")


def render_the_art_archive():
    legacy = ROOT / "article" / "archive" / "TheArtOfSeeing1.htm"
    content = ""
    if legacy.exists():
        text = legacy.read_text(encoding="utf-8", errors="ignore")
        match = re.search(r'<div id="container">\s*(.*?)\s*</div>\s*</body>', text, re.S | re.I)
        content = match.group(1) if match else text
        content = re.sub(r'<h3>.*?</h3>', "", content, flags=re.S | re.I)
        content = re.sub(r'<font[^>]*>(.*?)</font>', r"\1", content, flags=re.S | re.I)
        content = re.sub(r'\s+target="_blank"', "", content)
        content = re.sub(r'href="\.\./post/([^"]+?)\.htm"', r'href="../article/\1.html"', content)
    if not content.strip():
        content = '<p class="empty-note">看的艺术索引暂时无法读取。</p>'
    body = f"""<main>
  <section class="narrow page-title">
    <p class="eyebrow">Category</p>
    <h1>看的艺术</h1>
  </section>
  <section class="narrow single-column-page">
    <div class="article-body legacy-archive">
{content}
    </div>
  </section>
</main>"""
    return page("看的艺术 — Heima Photo", body, depth=1, description="Heima Photo 看的艺术分类文章。")


def render_article(article, prev_article, next_article):
    meta_parts = [article["date"].strftime("%Y.%m.%d"), article["category"]]
    if article.get("location"):
        meta_parts.append(article["location"])
    if article.get("camera"):
        meta_parts.append(article["camera"])
    lead = f'      <p class="article-lead">{esc(article["lead"])}</p>\n' if article.get("lead") else ""
    gallery = ""
    if article.get("gallery"):
        imgs = "\n".join(f'        <img src="{esc(src)}" alt="">' for src in article["gallery"])
        gallery = f"""      <section class="article-gallery">
        <h2>图片</h2>
{imgs}
      </section>
"""
    related = ""
    if article.get("related"):
        rows = []
        for item in article["related"]:
            rows.append(f'        <li><a href="{esc(item.get("url", "#"))}">{esc(item.get("title", ""))}</a></li>')
        related = f"""      <section class="related-records">
        <h2>Related</h2>
        <ul>
{chr(10).join(rows)}
        </ul>
      </section>
"""
    body = f"""<main>
  <article class="narrow single-column-page">
    <header class="article-header">
      <p class="eyebrow">{esc(article['category'])}</p>
      <h1>{esc(article['title'])}</h1>
      <p class="meta">{esc(' · '.join(meta_parts))}</p>
{lead}    </header>
    <div class="article-body">
{article['body']}
{gallery}{related}      <nav class="article-nav article-page-nav">
        <a class="nav-archive" href="../archive.html">Archive</a>
        <a class="nav-forum" href="https://www.douban.com/group/514220/" target="_blank" rel="noopener noreferrer">Forum</a>
      </nav>
    </div>
  </article>
</main>"""
    return page(f"{article['title']} — {SITE_TITLE}", body, depth=1, description=article["summary"])


def render_about(categories):
    body = f"""<main>
  <section class="wrap page-title">
    <p class="eyebrow">ABOUT</p>
    <h1>关于</h1>
    <p>一个存在了很多年的个人网站。记录摄影、文字，以及时间留下的痕迹。</p>
  </section>
  <section class="narrow about-page">
    <div class="about-story about-story-start">
      <p>这个网站最早建立于很多年前。</p>
      <p>这些年里，我见过太多网站诞生，<br>也见过太多网站消失。</p>
      <p>有些网站关闭了，有些账号停止更新了，<br>而这个网站却意外地保留了下来。</p>
    </div>

    <div class="about-map" aria-label="网站结构">
      <div>
        <h2>Portfolio</h2>
        <p>记录照片</p>
      </div>
      <div>
        <h2>Archive</h2>
        <p>保存文章</p>
      </div>
      <div>
        <h2>About</h2>
        <p>记录网站本身</p>
      </div>
    </div>

    <div class="about-story about-story-end">
      <p>最初它只是一个放照片的地方。</p>
      <p>后来，我开始记录一些文字。</p>
      <p>关于摄影，<br>关于器材，<br>关于建站，<br>关于那些偶然想到的事情。</p>
      <p>内容并不系统，<br>也没有明确规划。</p>
      <p>更像是一份持续积累的个人档案。</p>
      <p>这里没有算法推荐。<br>也没有流量目标。</p>
      <p>我更愿意把它理解为一个长期保存的空间。</p>
      <p>而时间把它们慢慢连接起来。</p>
      <p>如果多年以后我再次打开这个网站，<br>希望仍然能够通过这些照片和文字，<br>想起当时为什么按下快门，<br>又为什么写下这些内容。</p>
      <p>也许这就是 Heimaphoto 一直保留下来的原因。</p>
    </div>

    <div class="about-timeline">
      <h2>Timeline</h2>
      <dl>
        <div>
          <dt>2013</dt>
          <dd>网站建立</dd>
        </div>
        <div>
          <dt>2017</dt>
          <dd>开始留下照片与文字</dd>
        </div>
        <div>
          <dt>2025</dt>
          <dd>重新整理旧档案</dd>
        </div>
        <div>
          <dt>2026</dt>
          <dd>新作品系统上线</dd>
        </div>
      </dl>
    </div>
  </section>
</main>"""
    return page(f"关于 — {SITE_TITLE}", body, "about", description="Heima Photo：个人摄影与文字档案馆。")


def render_gear_item(article):
    note = article.get("gear_note") or article["summary"]
    return f"""      <a class="gear-item" href="{article['url']}">
        <img src="{esc(root_image_path(article['thumbnail']))}" alt="{esc(article['title'])}">
        <span class="gear-caption">
          <strong>{esc(article['title'])}</strong>
          <em>{esc(note)}</em>
        </span>
      </a>"""


def render_gear(articles):
    gear_articles = [
        article
        for article in articles
        if article["category_slug"] == "gear" and article.get("thumbnail")
    ]
    if gear_articles:
        items = "\n".join(render_gear_item(article) for article in gear_articles)
    else:
        items = """      <!-- Gear item template:
      <a class="gear-item" href="article/example.html">
        <img src="images/gear/example.jpg" alt="Example title">
        <span class="gear-caption">
          <strong>Example title</strong>
          <em>Optional short note.</em>
        </span>
      </a>
      -->
      <a class="gear-item" href="#">
        <img src="img/photo/coffee-time.jpg" alt="Leica M262">
        <span class="gear-caption">
          <strong>Leica M262</strong>
          <em>待替换</em>
        </span>
      </a>
      <a class="gear-item" href="#">
        <img src="img/photo/recorder.jpg" alt="Voigtlander 40mm F1.4">
        <span class="gear-caption">
          <strong>Voigtlander 40mm F1.4</strong>
          <em>待替换</em>
        </span>
      </a>
      <a class="gear-item" href="#">
        <img src="img/photo/Office-building.jpg" alt="MacBook Air">
        <span class="gear-caption">
          <strong>MacBook Air</strong>
          <em>待替换</em>
        </span>
      </a>
      <a class="gear-item" href="#">
        <img src="img/photo/sisyphe-bookstore-cafe.jpg" alt="iPad Pro">
        <span class="gear-caption">
          <strong>iPad Pro</strong>
          <em>待替换</em>
        </span>
      </a>
      <a class="gear-item" href="#">
        <img src="img/photo/recorder.jpg" alt="Mechanical Keyboard">
        <span class="gear-caption">
          <strong>Mechanical Keyboard</strong>
          <em>待替换</em>
        </span>
      </a>
      <a class="gear-item" href="#">
        <img src="img/photo/Office-building.jpg" alt="Software Tools">
        <span class="gear-caption">
          <strong>Software Tools</strong>
          <em>待替换</em>
        </span>
      </a>"""
    body = f"""<main class="gear-page">
  <section class="wrap gear-intro">
    <p class="eyebrow">Gear</p>
    <h1>工具</h1>
    <p>Things I Use and Keep.</p>
  </section>
  <section class="gear-stage wrap" aria-label="工具照片墙">
    <div class="gear-wall">
{items}
    </div>
  </section>
</main>"""
    return page("工具 — Heima Photo", body, "gear", description="Heima Photo 工具页：相机、镜头、电脑、键盘与软件工具的个人长期使用记录。")


def render_portfolio_entry(photo_works=None):
    photo_works = photo_works or []
    if not photo_works:
        body = """<main>
  <section class="wrap page-title">
    <p class="eyebrow">Portfolio</p>
    <h1>摄影作品集</h1>
    <p>这里保留旧作品集结构，作为摄影作品档案馆。</p>
  </section>
  <section class="narrow single-column-page">
    <div class="article-body">
      <p><a href="../portfolio.htm">进入旧版 Portfolio</a></p>
    </div>
  </section>
</main>"""
        return page(f"Portfolio — {SITE_TITLE}", body, "portfolio", depth=1)
    cards = []
    for work in photo_works:
        cards.append(
            f"""      <a class="portfolio-work" href="../{work['url']}">
        <img src="{esc(work['image'])}" alt="{esc(work['title'])}">
        <span>{esc(work['title'])}</span>
      </a>"""
        )
    works_html = f"""    <div class="portfolio-grid">
{chr(10).join(cards)}
    </div>"""
    body = f"""<main>
  <section class="wrap page-title">
    <p class="eyebrow">Portfolio</p>
    <h1>摄影作品集</h1>
    <p>新的 Portfolio 用来保存近期整理出的摄影作品。旧作品集仍作为历史档案保留。</p>
  </section>
  <section class="wrap portfolio-page">
{works_html}
    <p class="old-portfolio-link"><a href="../portfolio.htm">旧版作品入口 / Old Portfolio</a></p>
  </section>
</main>"""
    return page(f"Portfolio — {SITE_TITLE}", body, "portfolio", depth=1)


def render_photo_detail(work):
    meta = [("Date", work.get("date_display") or work["date"].strftime("%Y.%m.%d"))]
    if work.get("camera"):
        meta.append(("Camera", work["camera"]))
    if work.get("lens"):
        meta.append(("Lens", work["lens"]))
    if work.get("location"):
        meta.append(("Location", work["location"]))
    rows = "\n".join(f"        <div><dt>{esc(label)}</dt><dd>{esc(value)}</dd></div>" for label, value in meta)
    meta_html = f"""      <dl class="photo-meta">
{rows}
      </dl>
"""
    subtitle = f'      <p class="photo-subtitle">{esc(work["description"])}</p>\n' if work.get("description") else ""
    figures = []
    for index, src in enumerate(work["images"], 1):
        figure_class = "photo-hero" if index == 1 else "photo-frame"
        suffix = f" {index}" if work["type"] == "series" else ""
        figures.append(f'    <figure class="{figure_class}"><img src="{esc(src)}" alt="{esc(work["title"])}{suffix}"></figure>')
    images = "\n".join(figures)
    detail = f"""      <div class="photo-description">
{work['detail']}
      </div>
""" if work.get("detail") else ""
    nav = """      <nav class="article-nav photo-nav">
        <a href="../portfolio/index.html">← Portfolio</a>
        <a href="../archive.html">Archive →</a>
      </nav>
"""
    kicker = f"{esc(work['type'].title())} · {work['date'].year}"
    if work["type"] == "series":
        body = f"""<main>
  <article class="wrap photo-page">
    <section class="photo-info photo-info-top">
      <p class="photo-kicker">{kicker}</p>
      <h1>{esc(work['title'])}</h1>
{subtitle}    </section>
{images}
    <section class="photo-info">
{meta_html}{detail}{nav}    </section>
  </article>
</main>"""
    else:
        body = f"""<main>
  <article class="wrap photo-page">
{images}
    <section class="photo-info">
      <p class="photo-kicker">{kicker}</p>
      <h1>{esc(work['title'])}</h1>
{subtitle}{meta_html}{detail}{nav}    </section>
  </article>
</main>"""
    return page(f"{work['title']} — {SITE_TITLE}", body, depth=1, description=work.get("description") or DESCRIPTION)


def publish(target=None):
    if target and not target.is_absolute():
        target = (ROOT / target).resolve()
    ARTICLE_DIR.mkdir(exist_ok=True)
    PHOTO_DIR.mkdir(exist_ok=True)
    CATEGORY_DIR.mkdir(exist_ok=True)
    articles = [parse_article(path) for path in sorted(MD_DIR.glob("*.md")) if not path.name.startswith("_")]
    photo_works = [parse_photo_work(path) for path in sorted(PHOTO_MD_DIR.glob("*.md")) if not path.name.startswith("_")]
    known_sources = [a["source"].resolve() for a in articles] + [p["source"].resolve() for p in photo_works]
    if target and target not in known_sources:
        raise SystemExit(f"没有在 md/ 或 photo-md/ 中找到 {target}")
    articles.sort(key=lambda a: (a["date"], a["slug"]), reverse=True)
    photo_works.sort(key=lambda item: (item["date"], item["slug"]), reverse=True)
    chronological = list(reversed(articles))
    positions = {a["slug"]: i for i, a in enumerate(chronological)}
    categories = list(DEFAULT_CATEGORIES)
    for a in articles:
        if a["category"] not in categories:
            categories.append(a["category"])

    (ROOT / "index.html").write_text(render_index(articles), encoding="utf-8")
    (ROOT / "archive.html").write_text(render_archive(articles, categories, photo_works), encoding="utf-8")
    (ROOT / "about.html").write_text(render_about(categories), encoding="utf-8")
    (ROOT / "gear.html").write_text(render_gear(articles), encoding="utf-8")
    (ROOT / "portfolio" / "index.html").write_text(render_portfolio_entry(photo_works), encoding="utf-8")

    for article in articles:
        pos = positions[article["slug"]]
        prev_article = chronological[pos - 1] if pos > 0 else None
        next_article = chronological[pos + 1] if pos < len(chronological) - 1 else None
        (ARTICLE_DIR / f"{article['slug']}.html").write_text(
            render_article(article, prev_article, next_article), encoding="utf-8"
        )
    by_category = defaultdict(list)
    for article in articles:
        by_category[article["category"]].append(article)
    for category in categories:
        if category == "看的艺术":
            html_text = render_the_art_archive()
        else:
            html_text = render_category_page(category, by_category.get(category, []))
        (CATEGORY_DIR / f"{slugify(category)}.html").write_text(html_text, encoding="utf-8")
    for work in photo_works:
        (PHOTO_DIR / f"{work['slug']}.html").write_text(render_photo_detail(work), encoding="utf-8")
    print(f"Published {len(articles)} article(s), {len(photo_works)} photo work(s).")


def main():
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    publish(target)


if __name__ == "__main__":
    main()

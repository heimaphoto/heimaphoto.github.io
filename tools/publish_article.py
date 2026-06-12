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
ARTICLE_DIR = ROOT / "article"
CATEGORY_DIR = ROOT / "category"

SITE_TITLE = "Heima Photo"
DESCRIPTION = "Heima Photo：摄影、文字、器材与一些安静的好奇心。"
CATEGORY_SLUGS = {
    "散文": "prose",
    "摄影": "photography",
    "看的艺术": "TheArtOfSeeing",
    "摄影技术": "technology",
    "器材": "gear",
    "建站": "website",
    "生活": "life",
}
CATEGORY_EN = {
    "散文": "Prose",
    "摄影": "Photography",
    "看的艺术": "The Art Of Seeing",
    "摄影技术": "Technology",
    "器材": "Gear",
    "建站": "Website",
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
        "gallery": data.get("gallery", []),
        "related": data.get("related", []),
        "body": markdown_to_html(body, data["title"]),
    }


def root_image_path(path):
    return path[3:] if path.startswith("../") else path


def header(active="", depth=0):
    p = "../" * depth
    items = [
        ("index.html", "首页", "index"),
        ("archive.html", "归档", "archive"),
        ("portfolio/index.html", "Portfolio", "portfolio"),
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
      <a class="lightbox-trigger" href="img/photo/Milk-Tea.jpg" data-caption="Milk Tea"><img src="img/photo/Milk-Tea.jpg" alt="Milk Tea"></a>
      <a class="lightbox-trigger" href="img/photo/By-the-park-lake.jpg" data-caption="By the park lake"><img src="img/photo/By-the-park-lake.jpg" alt="By the park lake"></a>
      <a class="lightbox-trigger" href="img/photo/On-a-rainy-road.jpg" data-caption="On a rainy road"><img src="img/photo/On-a-rainy-road.jpg" alt="On a rainy road"></a>
      <a class="lightbox-trigger" href="img/photo/shanghai-night.jpg" data-caption="Shanghai night"><img src="img/photo/shanghai-night.jpg" alt="Shanghai night"></a>
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
        <p>Heima Photo 是王斌的个人档案馆：照片、文字、设备、建站记录，以及一些不太重要但我偏要记下来的东西。</p>
        <a class="text-link" href="about.html">更多关于我 →</a>
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
<div class="lightbox" id="lightbox" aria-hidden="true">
  <button class="lightbox-close" type="button" aria-label="关闭">×</button>
  <img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw==" alt="">
  <div class="lightbox-caption"></div>
</div>
<script>
(function () {{
  var blankImage = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw==";
  var box = document.getElementById("lightbox");
  if (!box) return;

  var image = box.getElementsByTagName("img")[0];
  var caption = box.getElementsByClassName("lightbox-caption")[0];
  var closeButton = box.getElementsByClassName("lightbox-close")[0];
  var links = document.querySelectorAll(".lightbox-trigger");

  function openLightbox(link) {{
    image.src = link.getAttribute("href");
    image.alt = link.getElementsByTagName("img")[0].alt || "";
    caption.textContent = link.getAttribute("data-caption") || image.alt || "";
    box.className = "lightbox is-open";
    box.setAttribute("aria-hidden", "false");
  }}

  function closeLightbox() {{
    box.className = "lightbox";
    box.setAttribute("aria-hidden", "true");
    image.src = blankImage;
  }}

  for (var i = 0; i < links.length; i += 1) {{
    links[i].addEventListener("click", function (event) {{
      event.preventDefault();
      openLightbox(this);
    }});
  }}

  closeButton.addEventListener("click", closeLightbox);
  box.addEventListener("click", function (event) {{
    if (event.target === box) closeLightbox();
  }});
  document.addEventListener("keydown", function (event) {{
    if (event.key === "Escape" || event.keyCode === 27) closeLightbox();
  }});
}}());
</script>"""
    return page(f"{SITE_TITLE} — Photographs, Notes and Quiet Experiments", body, "index")


def grouped(articles):
    years = defaultdict(list)
    for article in articles:
        years[article["date"].year].append(article)
    return dict(sorted(years.items(), reverse=True))


def render_category_sidebar(categories):
    rows = []
    for cat in categories:
        rows.append(
            f'      <li><a href="category/{slugify(cat)}.html">{esc(cat)}</a><span>{esc(CATEGORY_EN.get(cat, slugify(cat)))}</span></li>'
        )
    return "\n".join(rows)


def render_archive(articles, categories):
    sections = []
    for year, rows in grouped(articles).items():
        items = []
        for a in rows:
            items.append(
                f"""        <li>
          <time>{a['date'].strftime('%m.%d')}</time>
          <a href="{a['url']}">{esc(a['title'])}</a>
          <a class="item-category" href="category/{a['category_slug']}.html">{esc(a['category'])}</a>
        </li>"""
            )
        sections.append(f"      <h2>{year}</h2>\n      <ul>\n{chr(10).join(items)}\n      </ul>")
    body = f"""<main>
  <section class="wrap page-title">
    <p class="eyebrow">Archive</p>
    <h1>文章归档</h1>
    <p>所有文字内容都放在这里。首页只放最近几篇，归档负责长期保存。</p>
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
    return page(f"文章归档 — {SITE_TITLE}", body, "archive")


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
        <h2>相关记录</h2>
        <ul>
{chr(10).join(rows)}
        </ul>
      </section>
"""
    prev_link = f'<a href="{prev_article["article_href"]}">上一篇：{esc(prev_article["title"])}</a>' if prev_article else "<span></span>"
    next_link = f'<a href="{next_article["article_href"]}">下一篇：{esc(next_article["title"])}</a>' if next_article else "<span></span>"
    body = f"""<main>
  <article class="narrow single-column-page">
    <header class="article-header">
      <p class="eyebrow">{esc(article['category'])}</p>
      <h1>{esc(article['title'])}</h1>
      <p class="meta">{esc(' · '.join(meta_parts))}</p>
{lead}    </header>
    <div class="article-body">
{article['body']}
{gallery}{related}      <nav class="article-nav">
        {prev_link}
        <a href="../archive.html">返回归档</a>
        {next_link}
      </nav>
    </div>
  </article>
</main>"""
    return page(f"{article['title']} — {SITE_TITLE}", body, depth=1, description=article["summary"])


def render_about(categories):
    rows = "\n".join(f'        <li><a href="category/{slugify(c)}.html">{esc(c)}</a></li>' for c in categories)
    body = f"""<main>
  <section class="wrap page-title">
    <p class="eyebrow">About</p>
    <h1>关于 Heima Photo</h1>
    <p>这里不是商业摄影官网，也不是内容农场。它更像一个长期保留的个人档案馆。</p>
  </section>
  <section class="wrap about-grid">
    <div class="about-main">
      <h2>王斌</h2>
      <p>我拍照片，也写一点文字。喜欢简单、可靠、能长期保存的东西。所以这个网站仍然使用纯静态 HTML。</p>
      <p>这里会有摄影作品、器材记录、建站笔记、生活片段。摄影是入口，但我更希望它最终呈现的是一个人的观看方式。</p>
      <h2>关于这个网站</h2>
      <p>Portfolio 页面保留原来的作品集形式，像一个旧档案柜。首页作为主要入口；文章页和分类页采用单栏，以减少发布时需要同步修改的内容。</p>
    </div>
    <aside class="about-side">
      <h2>网站结构</h2>
      <ul>
        <li>首页：最新文章 + 精选照片 + 推荐文章</li>
        <li>文章页：单栏，文字与照片混排</li>
        <li>归档页：全部文章索引 + 分类入口</li>
        <li>分类页：单栏，日期与标题列表</li>
        <li>Portfolio：原作品集保留</li>
      </ul>
      <h2>类别</h2>
      <ul>
{rows}
      </ul>
    </aside>
  </section>
</main>"""
    return page(f"关于 — {SITE_TITLE}", body, "about")


def render_portfolio_entry():
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


def main():
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if target and not target.is_absolute():
        target = (ROOT / target).resolve()
    ARTICLE_DIR.mkdir(exist_ok=True)
    CATEGORY_DIR.mkdir(exist_ok=True)
    articles = [parse_article(path) for path in sorted(MD_DIR.glob("*.md")) if not path.name.startswith("_")]
    if target and target not in [a["source"].resolve() for a in articles]:
        raise SystemExit(f"没有在 md/ 中找到 {target}")
    articles.sort(key=lambda a: (a["date"], a["slug"]), reverse=True)
    chronological = list(reversed(articles))
    positions = {a["slug"]: i for i, a in enumerate(chronological)}
    categories = list(DEFAULT_CATEGORIES)
    for a in articles:
        if a["category"] not in categories:
            categories.append(a["category"])

    (ROOT / "index.html").write_text(render_index(articles), encoding="utf-8")
    (ROOT / "archive.html").write_text(render_archive(articles, categories), encoding="utf-8")
    (ROOT / "about.html").write_text(render_about(categories), encoding="utf-8")
    (ROOT / "portfolio" / "index.html").write_text(render_portfolio_entry(), encoding="utf-8")

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
    print(f"Published {len(articles)} article(s).")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import html
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POST_DIR = ROOT / "article" / "post"
MD_DIR = ROOT / "md"


class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in {"p", "div", "h1", "h2", "h3", "li", "br", "ol", "ul"}:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in {"p", "div", "h1", "h2", "h3", "li", "ol", "ul"}:
            self.parts.append("\n")

    def handle_data(self, data):
        self.parts.append(data)

    def text(self):
        value = html.unescape("".join(self.parts))
        value = re.sub(r"\s+", " ", value)
        return value.strip()


def clean_text(value):
    value = html.unescape(value or "")
    value = re.sub(r"<[^>]+>", "", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def visible_text(fragment):
    parser = VisibleText()
    parser.feed(fragment)
    return parser.text()


def yaml_scalar(value):
    value = (value or "").replace("\r", " ").replace("\n", " ")
    value = re.sub(r"\s+", " ", value).strip()
    if not value:
        return ""
    if re.search(r"[:#\\[\\]{}&*!|>'\"%@`]", value):
        return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return value


def normalize_asset_path(value):
    value = value.strip()
    value = value.replace("../../", "../")
    value = value.replace("../post/", "")
    value = re.sub(r"\.htm(\b|[#?])", r".html\1", value)
    return value


def normalize_body_html(fragment):
    fragment = re.sub(r"<h2[^>]*>.*?</h2>", "", fragment, count=1, flags=re.S | re.I)
    fragment = re.sub(r'\s+target="_blank"', "", fragment)
    fragment = re.sub(r'src="\.\./\.\./([^"]+)"', r'src="../\1"', fragment)
    fragment = re.sub(r'href="\.\./post/([^"]+?)\.htm"', r'href="\1.html"', fragment)
    fragment = re.sub(r'href="\./([^"]+?)\.htm"', r'href="\1.html"', fragment)
    fragment = re.sub(r'href="\.\./archive/prose1\.htm"', 'href="../category/prose.html"', fragment)
    fragment = re.sub(r'href="\.\./archive/data1\.htm"', 'href="../category/technology.html"', fragment)
    fragment = re.sub(r'href="\.\./archive/TheArtOfSeeing1\.htm"', 'href="../category/TheArtOfSeeing.html"', fragment)
    lines = [line.rstrip() for line in fragment.strip().splitlines()]
    return "\n".join(line for line in lines if line.strip())


def extract_body_html(text):
    matches = re.findall(r'<div class="bd[12]">\s*(.*?)\s*</div>', text, flags=re.S | re.I)
    if matches:
        return "\n\n".join(normalize_body_html(match) for match in matches if visible_text(match))
    body_match = re.search(r"<body[^>]*>(.*?)</body>", text, flags=re.S | re.I)
    return normalize_body_html(body_match.group(1) if body_match else text)


def extract_title(text, fallback):
    h2 = re.search(r"<h2[^>]*>(.*?)</h2>", text, flags=re.S | re.I)
    if h2:
        title = clean_text(h2.group(1))
        if title:
            return title
    title = re.search(r"<title[^>]*>(.*?)</title>", text, flags=re.S | re.I)
    return clean_text(title.group(1)) if title else fallback


def extract_meta(text):
    match = re.search(r"Written on\s*([0-9]{8})\s*\|\s*Tag:\s*(?:<a[^>]*>)?([^<\n]+)", text, flags=re.I)
    if not match:
        return "", ""
    raw_date = match.group(1)
    date = f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:8]}"
    return date, clean_text(match.group(2))


def category_for(path, tag):
    name = path.name
    if "TheArtOfSeeing" in name or "TheArtOfSeeing" in tag or "看的艺术" in tag:
        return "摄影/看的艺术", "TheArtOfSeeing"
    if "-data" in name or tag == "资料":
        return "摄影/技术", "technology"
    if "-prose" in name or tag == "散文":
        return "散文", "prose"
    return "摄影", "photography"


def summarize(body_html, title):
    text = visible_text(body_html)
    text = re.sub(r"^" + re.escape(title) + r"\s*", "", text)
    text = re.sub(r"Photo by [^|。；;]+(?:\|\s*Photo URL)?", "", text, flags=re.I)
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return f"{title}。"
    return text[:96] + ("……" if len(text) > 96 else "")


def gallery_paths(text):
    paths = []
    for src in re.findall(r'<img[^>]+src="([^"]+)"', text, flags=re.I):
        src = normalize_asset_path(src)
        if src not in paths:
            paths.append(src)
    return paths


def convert(path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    title = extract_title(text, path.stem)
    date, tag = extract_meta(text)
    category, category_slug = category_for(path, tag)
    if not date:
        raise ValueError(f"{path} 缺少日期")
    body_html = extract_body_html(text)
    summary = summarize(body_html, title)
    images = gallery_paths(text)
    lines = [
        "---",
        f"title: {yaml_scalar(title)}",
        f"date: {date}",
        f"category: {yaml_scalar(category)}",
        f"category_slug: {category_slug}",
        f"summary: {yaml_scalar(summary)}",
    ]
    if images:
        lines.append(f"thumbnail: {images[0]}")
        lines.append("gallery:")
        lines.extend(f"  - {image}" for image in images)
    lines.extend(["---", "", body_html, ""])
    return "\n".join(lines)


def main():
    MD_DIR.mkdir(exist_ok=True)
    sample = MD_DIR / "shanghai-night.md"
    if sample.exists():
        sample.unlink()
    count = 0
    for path in sorted(POST_DIR.glob("*.htm")):
        (MD_DIR / f"{path.stem}.md").write_text(convert(path), encoding="utf-8")
        count += 1
    old_sample_page = ROOT / "article" / "shanghai-night.html"
    if old_sample_page.exists():
        old_sample_page.unlink()
    print(f"Migrated {count} legacy post(s) into md/.")


if __name__ == "__main__":
    main()

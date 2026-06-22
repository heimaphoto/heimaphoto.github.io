#!/usr/bin/env python3
import sys
from pathlib import Path

import publish_article


def validate_publish(target):
    work = publish_article.parse_photo_work(target)
    checks = [
        (
            publish_article.ROOT / "photo" / f"{work['slug']}.html",
            [work["title"]],
            "photo detail page",
        ),
        (
            publish_article.ROOT / "portfolio" / "index.html",
            [work["title"], work["url"]],
            "portfolio index",
        ),
        (
            publish_article.ROOT / "archive.html",
            [work["title"], work["url"], "摄影作品"],
            "archive",
        ),
    ]
    missing = []
    for path, expected, label in checks:
        if not path.exists():
            missing.append(f"{label}: missing {path.relative_to(publish_article.ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        absent = [value for value in expected if value not in text]
        if absent:
            missing.append(f"{label}: missing {', '.join(absent)}")
    if missing:
        detail = "\n".join(f"- {item}" for item in missing)
        raise SystemExit(f"照片发布校验失败：\n{detail}")
    print(f"Validated photo work in photo/, portfolio/index.html and archive.html: {work['title']}")


def main():
    if len(sys.argv) < 2:
        raise SystemExit("请指定 photo-md/<slug>.md")
    target = Path(sys.argv[1])
    if target.name.startswith("_") or target.suffix != ".md":
        raise SystemExit("photo 发布源文件必须是非 _ 开头的 .md 文件")
    if "photo-md" not in target.parts:
        raise SystemExit("photo 发布源文件必须放在 photo-md/ 目录")
    publish_article.publish(target)
    validate_publish((publish_article.ROOT / target).resolve() if not target.is_absolute() else target.resolve())


if __name__ == "__main__":
    main()

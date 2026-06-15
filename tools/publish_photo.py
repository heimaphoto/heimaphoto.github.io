#!/usr/bin/env python3
import sys
from pathlib import Path

import publish_article


def main():
    if len(sys.argv) < 2:
        raise SystemExit("请指定 photo-md/<slug>.md")
    target = Path(sys.argv[1])
    if target.name.startswith("_") or target.suffix != ".md":
        raise SystemExit("photo 发布源文件必须是非 _ 开头的 .md 文件")
    if "photo-md" not in target.parts:
        raise SystemExit("photo 发布源文件必须放在 photo-md/ 目录")
    publish_article.publish(target)


if __name__ == "__main__":
    main()

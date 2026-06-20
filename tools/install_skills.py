#!/usr/bin/env python3
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills"
TARGET = Path.home() / ".codex" / "skills"
SITE_RULES = SOURCE / "site-rules.md"

SKILLS = [
    "heimaphoto-publisher",
    "heimaphoto-photo-publisher",
]


def main():
    if not SOURCE.exists():
        raise SystemExit("skills/ directory does not exist")
    if not SITE_RULES.exists():
        raise SystemExit(f"Missing {SITE_RULES}")
    TARGET.mkdir(parents=True, exist_ok=True)
    for name in SKILLS:
        src = SOURCE / name
        dst = TARGET / name
        if not (src / "SKILL.md").exists():
            raise SystemExit(f"Missing {src / 'SKILL.md'}")
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        shutil.copy2(SITE_RULES, dst / "site-rules.md")
        print(f"Installed {name} -> {dst}")


if __name__ == "__main__":
    main()

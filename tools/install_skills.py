#!/usr/bin/env python3
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills"
TARGET = Path.home() / ".codex" / "skills"

SKILLS = [
    "heimaphoto-publisher",
    "heimaphoto-photo-publisher",
]


def main():
    if not SOURCE.exists():
        raise SystemExit("skills/ directory does not exist")
    TARGET.mkdir(parents=True, exist_ok=True)
    for name in SKILLS:
        src = SOURCE / name
        dst = TARGET / name
        if not (src / "SKILL.md").exists():
            raise SystemExit(f"Missing {src / 'SKILL.md'}")
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        print(f"Installed {name} -> {dst}")


if __name__ == "__main__":
    main()

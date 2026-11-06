#!/usr/bin/env python3
"""Check that relative links in Markdown files resolve on disk.

External URLs are not fetched (they belong to lesson review, not to
a filesystem check). Anchors are stripped; percent-encoding is
decoded. Exits nonzero listing every broken relative link.
"""
import os
import re
import sys
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def main():
    broken = []
    for dirpath, _dirs, files in os.walk(ROOT):
        if ".git" in dirpath:
            continue
        for name in files:
            if not name.endswith(".md"):
                continue
            path = os.path.join(dirpath, name)
            with open(path, encoding="utf-8") as f:
                text = f.read()
            for target in LINK.findall(text):
                target = target.strip()
                if not target or target.startswith(
                        ("http://", "https://", "mailto:", "#")):
                    continue
                target = urllib.parse.unquote(target.split("#")[0])
                if not target:
                    continue
                resolved = os.path.normpath(
                    os.path.join(os.path.dirname(path), target))
                if not resolved.startswith(ROOT):
                    # Links like ../../issues are GitHub-web-relative:
                    # they resolve against the repository page on
                    # github.com, not against the filesystem.
                    continue
                if not os.path.exists(resolved):
                    broken.append(
                        f"{os.path.relpath(path, ROOT)} -> {target}")
    for b in broken:
        print("BROKEN", b)
    print(f"{len(broken)} broken relative link(s)")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
build.py - dựng trang HTML một file từ story.json.

Usage:
  python build.py story.json -o out.html            # kiểm tra tĩnh rồi build (dừng nếu có lỗi)
  python build.py story.json -o out.html --force    # build dù còn lỗi (chỉ để xem nháp)

Brief (người nhận, mức, cài đặt người đọc) KHÔNG bao giờ được đưa vào HTML.
"""
import argparse
import html
import json
import re
import sys
from pathlib import Path

from console import configure_utf8

HERE = Path(__file__).resolve().parent
SHELL = HERE.parent / "assets" / "shell.html"
THEMES = {"onboard": "#D8501A", "neutral": "#3A4654"}
RENDER_KEYS_DROP = {"brief", "lint"}


def _strip_private(node):
    """Bỏ các khóa nội bộ (brief, lint, sources, basis) khỏi dữ liệu gửi vào trang."""
    if isinstance(node, dict):
        return {k: _strip_private(v) for k, v in node.items() if k not in RENDER_KEYS_DROP and k not in ("sources", "basis")}
    if isinstance(node, list):
        return [_strip_private(v) for v in node]
    return node


def _fonts(langs, style=None):
    fam = ["Be+Vietnam+Pro:wght@400;500;700", "Lexend:wght@500;700"]
    if style == "sketch":
        fam.append("Patrick+Hand")
    if style == "editorial":
        fam.append("Playfair+Display:wght@600;700")
    if "ja" in langs:
        fam.append("Noto+Sans+JP:wght@400;700")
    q = "&".join("family=" + f for f in fam)
    return ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            f'<link href="https://fonts.googleapis.com/css2?{q}&display=swap" rel="stylesheet">')


def _brand(theme):
    if isinstance(theme, dict) and re.fullmatch(r"#[0-9a-fA-F]{6}", str(theme.get("brand", ""))):
        return theme["brand"]
    if isinstance(theme, str) and re.fullmatch(r"#[0-9a-fA-F]{6}", theme):
        return theme
    return THEMES.get(theme or "onboard", THEMES["onboard"])


def build_html(story):
    langs = story.get("langs") or ["vi"]
    default = story.get("defaultLang") or langs[0]
    title = (story.get("meta") or {}).get("title", "")
    if isinstance(title, dict):
        title = title.get(default) or next(iter(title.values()), "")
    title = re.sub(r"<[^>]+>", "", str(title))
    public = _strip_private(story)
    data = json.dumps(public, ensure_ascii=False).replace("</", "<\\/").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    shell = SHELL.read_text(encoding="utf-8")
    out = (shell.replace("__LANG__", html.escape(default))
                .replace("__TITLE__", html.escape(title))
                .replace("__BRAND__", _brand(story.get("theme")))
                .replace("<!--__FONTS__-->", _fonts(langs, story.get("style")))
                .replace("/*__STORY__*/null", data))
    return out


def main():
    configure_utf8()
    ap = argparse.ArgumentParser(description="Build trang onboard từ story.json")
    ap.add_argument("story")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--force", action="store_true", help="build dù kiểm tra tĩnh còn lỗi")
    a = ap.parse_args()
    story = json.loads(Path(a.story).read_text(encoding="utf-8-sig"))
    sys.path.insert(0, str(HERE))
    from check import static_check
    rep = static_check(story)
    for line in rep.errors + rep.warnings:
        print(line)
    if rep.errors and not a.force:
        print(f"\n=> Dừng: {len(rep.errors)} lỗi. Sửa story hoặc dùng --force để xem nháp.")
        sys.exit(1)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(build_html(story), encoding="utf-8")
    size = Path(a.out).stat().st_size
    print(f"\n=> Đã build {a.out} ({size // 1024} KB, {len(story.get('steps', []))} bước, {len(story.get('langs') or ['vi'])} ngôn ngữ)")


if __name__ == "__main__":
    main()

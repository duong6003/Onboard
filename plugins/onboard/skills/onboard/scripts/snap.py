#!/usr/bin/env python3
"""
snap.py - chụp hình của từng bước (trạng thái cuối) thành PNG, kèm manifest.json chứa chữ của bước.
Dùng để dựng slide (Slides type / pptx) hoặc chèn vào tài liệu từ cùng một story.

Usage:
  python snap.py story.json -o snaps/                # mọi ngôn ngữ
  python snap.py story.json -o snaps/ --lang vi --width 1280 --scale 2
"""
import argparse
import json
import re
import sys
from pathlib import Path

from console import configure_utf8

HERE = Path(__file__).resolve().parent


def plain(v, lang, default):
    if isinstance(v, dict):
        v = v.get(lang) or v.get(default) or next(iter(v.values()), "")
    return re.sub(r"<[^>]+>", "", str(v or ""))


def main():
    configure_utf8()
    ap = argparse.ArgumentParser(description="Chụp hình từng bước của story")
    ap.add_argument("story")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--lang", action="append", help="chỉ chụp ngôn ngữ này (lặp lại được)")
    ap.add_argument("--width", type=int, default=1280)
    ap.add_argument("--scale", type=float, default=2.0, help="độ nét (device scale factor)")
    a = ap.parse_args()
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Cần playwright để chụp hình.", file=sys.stderr)
        sys.exit(1)
    sys.path.insert(0, str(HERE))
    from build import build_html
    story = json.loads(Path(a.story).read_text(encoding="utf-8-sig"))
    story = dict(story, format="stepper", autoplay=False)
    langs = a.lang or story.get("langs") or ["vi"]
    default = story.get("defaultLang") or (story.get("langs") or ["vi"])[0]
    out = Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    page_path = out / "_snap.html"
    page_path.write_text(build_html(story), encoding="utf-8")
    manifest = {"title": {}, "steps": []}
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": a.width, "height": 900}, device_scale_factor=a.scale, reduced_motion="reduce")
        pg.goto(page_path.as_uri())
        pg.wait_for_timeout(300)
        for lang in langs:
            pg.evaluate(f"window.__onboard.setLang({json.dumps(lang)})")
            manifest["title"][lang] = plain((story.get("meta") or {}).get("title"), lang, default)
            for i, s in enumerate(story.get("steps", [])):
                pg.evaluate(f"window.__onboard.go({i})")
                pg.wait_for_timeout(150)
                img = out / f"{lang}-{i + 1:02d}.png"
                el = pg.query_selector("#visual")
                if el and s.get("visual"):
                    el.screenshot(path=str(img))
                else:
                    img = None
                if lang == langs[0]:
                    manifest["steps"].append({"n": i + 1, "images": {}, "title": {}, "body": {}, "notes": {}})
                m = manifest["steps"][i]
                m["title"][lang] = plain(s.get("title"), lang, default).replace("{count}", str((s.get("count") or {}).get("to", "")))
                m["body"][lang] = plain(s.get("body"), lang, default)
                notes = s.get("notes") or ([s["note"]] if s.get("note") else [])
                m["notes"][lang] = [f"{n.get('type')}: {plain(n.get('text'), lang, default)}" for n in notes]
                if img:
                    m["images"][lang] = img.name
        b.close()
    page_path.unlink(missing_ok=True)
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"=> {len(manifest['steps'])} bước × {len(langs)} ngôn ngữ, ảnh và manifest.json trong {out}")


if __name__ == "__main__":
    main()

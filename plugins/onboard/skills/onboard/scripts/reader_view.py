#!/usr/bin/env python3
"""
reader_view.py - in ra đúng những gì người đọc thấy trên trang (không có brief, nguồn, basis).
Dùng cho bước soát độc lập: người soát chỉ đọc bản này, không đọc story.json.

Usage:
  python3 reader_view.py story.json [--lang vi] > reader.md
"""
import argparse
import json
import re
from pathlib import Path

from console import configure_utf8

SKIP = {"pattern", "anim", "status", "from", "to", "col", "lane", "id", "max", "blocks", "together", "reveal", "showMiss",
        "headSpan", "rowCount", "colCount", "order", "highlight", "kind", "type", "at", "dim", "decimals", "links",
        "focus", "state", "shape", "basis", "sources", "during", "expr", "valueExpr", "maxExpr", "if", "min", "step",
        "answer", "scale", "path", "current", "start", "row", "recommend", "_uid", "layout"}


def T(v, lang, default):
    if isinstance(v, dict) and v and all(len(k) <= 3 for k in v):
        v = v.get(lang) or v.get(default) or next(iter(v.values()))
    return re.sub(r"<[^>]+>", "", str(v)) if isinstance(v, (str, int, float)) else ""


def texts(node, lang, default, out):
    if isinstance(node, dict):
        if node and all(isinstance(k, str) and len(k) <= 3 and k.isalpha() and k.islower() for k in node) and all(isinstance(x, str) for x in node.values()):
            out.append(T(node, lang, default))
            return
        for k, v in node.items():
            if k == "cells" and isinstance(v, dict):
                continue
            if k in SKIP:
                continue
            texts(v, lang, default, out)
    elif isinstance(node, list):
        for v in node:
            texts(v, lang, default, out)
    elif isinstance(node, (str, int, float)) and str(node).strip():
        out.append(re.sub(r"<[^>]+>", "", str(node)))


def main():
    configure_utf8()
    ap = argparse.ArgumentParser()
    ap.add_argument("story")
    ap.add_argument("--lang")
    a = ap.parse_args()
    s = json.loads(Path(a.story).read_text(encoding="utf-8-sig"))
    langs = s.get("langs") or ["vi"]
    default = s.get("defaultLang") or langs[0]
    lang = a.lang or default
    meta = s.get("meta") or {}
    print(f"# {T(meta.get('title', ''), lang, default)}")
    if meta.get("subtitle"):
        print(T(meta["subtitle"], lang, default))
    if meta.get("footer"):
        print(T(meta["footer"], lang, default))
    steps = s.get("steps") or []
    for i, st in enumerate(steps):
        title = T(st.get("title", ""), lang, default)
        if st.get("count"):
            title = title.replace("{count}", str(st["count"].get("to", "")))
        print(f"\n## Bước {i + 1}/{len(steps)}: {title}")
        if st.get("body"):
            print(T(st["body"], lang, default))
        for c in st.get("chips") or []:
            print(f"- [{c.get('kind', 'info')}] {T(c.get('text', ''), lang, default)}")
        for c in st.get("checks") or []:
            print(f"- {T(c.get('text', ''), lang, default)} → {T(c.get('verdict', ''), lang, default)}")
        for n in st.get("notes") or ([st["note"]] if st.get("note") else []):
            print(f"> Nhãn {n.get('type')}: {T(n.get('text', ''), lang, default)}")
        vis = st.get("visual")
        vl = vis if isinstance(vis, list) else ([vis] if vis else [])
        for v in vl:
            out = []
            texts(v, lang, default, out)
            uniq = list(dict.fromkeys(x for x in out if x))
            print(f"[Hình {v.get('pattern')}] " + " · ".join(uniq[:40]))


if __name__ == "__main__":
    main()

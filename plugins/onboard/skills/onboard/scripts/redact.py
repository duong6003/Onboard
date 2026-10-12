#!/usr/bin/env python3
"""
redact.py - che dữ liệu nhạy cảm trong nguồn (log, ghi chú) hoặc story.json trước khi gửi ra ngoài.

Usage:
  python redact.py input.txt -o output.txt
  python redact.py story.json -o story.json --keep "TEST-VBAD\\d+-\\d+"
  python redact.py input.txt --mask "KH-\\d{6}" --dry-run

Mặc định che: email, IP, JWT, khóa/mật khẩu dạng key=value, chuỗi hex dài, đường dẫn máy, host nội bộ.
--keep  REGEX : giữ nguyên các chuỗi khớp (ví dụ mã thiết bị khách đã biết)
--mask  REGEX : che thêm theo mẫu riêng của dự án
"""
import argparse
import json
import re
import sys
from pathlib import Path

from console import configure_utf8

RULES = [
    ("EMAIL", re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")),
    ("TOKEN", re.compile(r"eyJ[\w-]{10,}\.[\w-]{10,}\.[\w-]{5,}")),
    ("SECRET", re.compile(r"(?i)(\b(?:authorization\s*:\s*)?(?:bearer|token|api[_-]?key|secret|password|passwd)\b\s*(?:[:=]|\s)\s*)\S+")),
    ("IP", re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b")),
    ("TOKEN", re.compile(r"\b[0-9a-fA-F]{32,}\b")),
    ("PATH", re.compile(r"(?:[A-Za-z]:\\[^\r\n\"']+)|(?:/(?:home|Users|var|etc|opt|srv)/[^\r\n\"']+)")),
    ("HOST", re.compile(r"\b(?:localhost|[\w-]+\.(?:local|internal|lan|corp))\b")),
]


def redact_text(s, keep, extra, counts):
    kept = {}

    def hold(m):
        key = f"\x00{len(kept)}\x00"
        kept[key] = m.group(0)
        return key

    for k in keep:
        s = k.sub(hold, s)
    for name, rx in RULES:
        def sub(m, name=name):
            counts[name] = counts.get(name, 0) + 1
            if name == "SECRET":
                return m.group(1) + "[SECRET]"
            return f"[{name}]"
        s = rx.sub(sub, s)
    for rx in extra:
        def sub2(m):
            counts["CUSTOM"] = counts.get("CUSTOM", 0) + 1
            return "[REDACTED]"
        s = rx.sub(sub2, s)
    for key, val in kept.items():
        s = s.replace(key, val)
    return s


def redact_json(node, keep, extra, counts):
    if isinstance(node, dict):
        return {k: redact_json(v, keep, extra, counts) for k, v in node.items()}
    if isinstance(node, list):
        return [redact_json(v, keep, extra, counts) for v in node]
    if isinstance(node, str):
        return redact_text(node, keep, extra, counts)
    return node


def main():
    configure_utf8()
    ap = argparse.ArgumentParser(description="Che dữ liệu nhạy cảm")
    ap.add_argument("input")
    ap.add_argument("-o", "--out")
    ap.add_argument("--keep", action="append", default=[])
    ap.add_argument("--mask", action="append", default=[])
    ap.add_argument("--dry-run", action="store_true", help="chỉ đếm, không ghi file")
    a = ap.parse_args()
    keep = [re.compile(k) for k in a.keep]
    extra = [re.compile(m) for m in a.mask]
    raw = Path(a.input).read_text(encoding="utf-8-sig")
    counts = {}
    if a.input.endswith(".json"):
        out = json.dumps(redact_json(json.loads(raw), keep, extra, counts), ensure_ascii=False, indent=2)
    else:
        out = redact_text(raw, keep, extra, counts)
    total = sum(counts.values())
    print("Đã che: " + (", ".join(f"{k}={v}" for k, v in sorted(counts.items())) if counts else "không có gì"), file=sys.stderr)
    if a.dry_run:
        return
    if a.out:
        Path(a.out).write_text(out, encoding="utf-8")
        print(f"=> {a.out} ({total} chỗ đã che)", file=sys.stderr)
    else:
        sys.stdout.write(out)


if __name__ == "__main__":
    main()

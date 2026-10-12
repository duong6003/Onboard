#!/usr/bin/env python3
"""
hook_check.py - hook PostToolUse (Claude Code plugin): sau khi ghi/sửa một story*.json, chạy kiểm tra tĩnh.
Có lỗi thì in ra stderr và thoát mã 2 để Claude thấy và sửa; không phải story thì bỏ qua.
"""
import json
import re
import sys
from pathlib import Path

from console import configure_utf8

HERE = Path(__file__).resolve().parent


def main():
    configure_utf8()
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    ti = data.get("tool_input") or {}
    fp = ti.get("file_path") or ti.get("path") or ""
    if not fp or not re.search(r"story[^/\\]*\.json$", fp):
        return 0
    p = Path(fp)
    if not p.exists():
        return 0
    try:
        story = json.loads(p.read_text(encoding="utf-8-sig"))
    except Exception as e:
        print(f"[onboard] {p.name} không phải JSON hợp lệ: {e}", file=sys.stderr)
        return 2
    if not isinstance(story, dict) or "steps" not in story:
        return 0
    sys.path.insert(0, str(HERE))
    from check import static_check
    try:
        rep = static_check(story)
    except Exception as e:
        print(f"[onboard] {p.name} không kiểm tra được: {e}", file=sys.stderr)
        return 2
    if rep.errors:
        print(f"[onboard] {p.name}: {len(rep.errors)} lỗi cần sửa trước khi build:", file=sys.stderr)
        for line in rep.errors[:15]:
            print("  " + line, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
regress.py - chạy lại check.py cho mọi story mẫu (và thư mục thêm) sau mỗi lần sửa skill.

Usage:
  python3 regress.py                         # examples/*.story.json
  python3 regress.py --extra ../my-stories   # thêm story của dự án
  python3 regress.py --no-render             # chỉ kiểm tĩnh
Exit code 1 nếu có story bị lỗi.
"""
import argparse
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from console import configure_utf8

HERE = Path(__file__).resolve().parent


def main():
    configure_utf8()
    ap = argparse.ArgumentParser()
    ap.add_argument("--extra", action="append", default=[])
    ap.add_argument("--no-render", action="store_true")
    a = ap.parse_args()
    files = sorted((HERE.parent / "examples").glob("*.json"))
    for d in a.extra:
        files += sorted(Path(d).glob("**/*story*.json"))
    render = not a.no_render and importlib.util.find_spec("playwright") is not None
    failed = 0
    with tempfile.TemporaryDirectory() as tmp:
        for f in files:
            cmd = [sys.executable, str(HERE / "check.py"), str(f), "--json"]
            if render:
                cmd += ["--render", str(Path(tmp) / f.stem)]
            out = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
            try:
                r = json.loads(out.stdout)
                ne, nw = len(r["errors"]), len(r["warnings"])
            except Exception:
                ne, nw = 1, 0
            failed += ne > 0
            print(f"{'LỖI' if ne else 'OK '}  {f.name:<44} {ne} lỗi, {nw} cảnh báo")
    print(f"\n=> {len(files)} story, {failed} lỗi" + ("" if render else " (không kiểm hiển thị)"))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()

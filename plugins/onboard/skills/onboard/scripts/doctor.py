#!/usr/bin/env python3
"""
doctor.py - kiểm tra môi trường chạy skill onboard (bất kỳ agent nào).

Usage:
  python3 doctor.py          # in bảng trạng thái và cách cài phần thiếu
  python3 doctor.py --json   # kết quả dạng JSON
Exit code luôn 0; phần thiếu chỉ làm skill chạy ở chế độ giảm (ví dụ bỏ qua kiểm hiển thị).
"""
import importlib
import json
import platform
import sys

from console import configure_utf8


def check():
    res = []
    ok_py = sys.version_info >= (3, 8)
    res.append(("python", ok_py, platform.python_version(), "Cần Python 3.8 trở lên"))
    for mod, why, fix in [
        ("PIL", "ghép ảnh chụp thành sheet để xem nhanh", "pip install pillow"),
        ("playwright", "chụp từng bước, kiểm tràn chữ, kiểm lỗi JavaScript", "pip install playwright && python3 -m playwright install chromium"),
    ]:
        try:
            m = importlib.import_module(mod)
            res.append((mod, True, getattr(m, "__version__", "có"), why))
        except Exception:
            res.append((mod, False, "thiếu", f"{why}. Cài: {fix}"))
    chromium = False
    detail = "bỏ qua (thiếu playwright)"
    if any(r[0] == "playwright" and r[1] for r in res):
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                b = p.chromium.launch()
                b.close()
            chromium, detail = True, "chạy được"
        except Exception as e:
            detail = f"không chạy được: {str(e).splitlines()[0][:80]}. Cài: python3 -m playwright install chromium"
    res.append(("chromium", chromium, detail, "trình duyệt cho kiểm hiển thị"))
    return res


def main():
    configure_utf8()
    res = check()
    if "--json" in sys.argv:
        print(json.dumps([{"name": n, "ok": o, "detail": d, "note": w} for n, o, d, w in res], ensure_ascii=False, indent=2))
        return
    for n, o, d, w in res:
        print(f"{'OK ' if o else 'THIẾU'}  {n:<11} {d:<14} {w}")
    full = all(o for _, o, _, _ in res)
    print("\n=> " + ("Đủ để chạy toàn bộ quy trình." if full else
                     "Chạy được ở chế độ giảm: build.py và check.py (tĩnh) vẫn dùng được; kiểm hiển thị bị bỏ qua và phải ghi vào phần báo lại."))


if __name__ == "__main__":
    main()

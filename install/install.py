#!/usr/bin/env python3
"""
install.py - cài skill onboard và onboard-review cho nhiều agent từ cùng một repo.

Usage:
  python3 install/install.py --list                     # xem các agent có sẵn đường dẫn
  python3 install/install.py --agent codex --agent cursor
  python3 install/install.py --agent claude --project ~/work/du-an-x   # cài vào dự án thay vì thư mục người dùng
  python3 install/install.py --dest ~/my-agent/skills                 # agent khác: chỉ định thư mục skills
  python3 install/install.py --agents-md ~/work/du-an-x/AGENTS.md     # agent không hỗ trợ skill: thêm chỉ dẫn vào AGENTS.md

Claude Code nên cài bằng plugin marketplace (xem README) để có thêm subagent và hook.
Đường dẫn mặc định của từng agent có thể đổi theo phiên bản; kiểm lại với tài liệu của agent nếu không thấy skill.
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

import re

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "plugins" / "onboard" / "skills"
HOME = Path.home()
# agent: (thư mục skills cấp người dùng, thư mục skills cấp dự án)
PRESETS = {
    "claude":   (HOME / ".claude/skills",          ".claude/skills"),
    "codex":    (HOME / ".codex/skills",           ".codex/skills"),
    "cursor":   (HOME / ".cursor/skills",          ".cursor/skills"),
    "cline":    (HOME / ".cline/skills",           ".cline/skills"),
    "continue": (HOME / ".continue/skills",        ".continue/skills"),
    "roo":      (HOME / ".roo/skills",             ".roo/skills"),
    "kilocode": (HOME / ".kilocode/skills",        ".kilocode/skills"),
    "qwen":     (HOME / ".qwen/skills",            ".qwen/skills"),
    "junie":    (HOME / ".junie/skills",           ".junie/skills"),
    "droid":    (HOME / ".factory/skills",         ".factory/skills"),
    "amp":      (HOME / ".config/agents/skills",   ".agents/skills"),
}
AGENTS_START = "<!-- ONBOARD:START -->"
AGENTS_END = "<!-- ONBOARD:END -->"
AGENTS_MD = f"""{AGENTS_START}
## Onboard

Khi được nhờ làm trang giải trình / onboard dễ hiểu (hoặc gặp lệnh `/onboard`), đọc và làm đúng theo
{{path}}/onboard/SKILL.md. Khi được nhờ soát lại một trang đã có, làm theo {{path}}/onboard-review/SKILL.md.
{AGENTS_END}
"""


def configure_utf8():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except AttributeError:
            pass


def copy_to(dest: Path, force: bool, dry: bool):
    for skill in ("onboard", "onboard-review"):
        src, dst = SKILLS / skill, dest / skill
        if dst.exists() and not force:
            print(f"  bỏ qua {dst} (đã có; dùng --force để cài đè)")
            continue
        print(f"  {'(thử) ' if dry else ''}{src.name} → {dst}")
        if not dry:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(src, dst, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__"))


def main():
    configure_utf8()
    ap = argparse.ArgumentParser(description="Cài skill onboard cho nhiều agent")
    ap.add_argument("--agent", action="append", default=[], help="tên agent trong --list (lặp lại được)")
    ap.add_argument("--all", action="store_true", help="cài cho mọi agent trong danh sách")
    ap.add_argument("--project", help="cài vào thư mục dự án thay vì thư mục người dùng")
    ap.add_argument("--dest", action="append", default=[], help="thư mục skills tùy chọn")
    ap.add_argument("--agents-md", help="thêm chỉ dẫn vào file AGENTS.md (agent không hỗ trợ skill)")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    if a.list:
        for k, (u, p) in PRESETS.items():
            print(f"{k:<9} người dùng: {u}    dự án: <dự án>/{p}")
        return
    targets = []
    for name in (list(PRESETS) if a.all else a.agent):
        if name not in PRESETS:
            sys.exit(f"Không biết agent '{name}'. Xem --list, hoặc dùng --dest.")
        user_dir, proj_dir = PRESETS[name]
        targets.append((name, Path(a.project).expanduser() / proj_dir if a.project else user_dir))
    targets += [("dest", Path(d).expanduser()) for d in a.dest]
    if not targets and not a.agents_md:
        ap.print_help()
        return
    for name, dest in targets:
        print(f"[{name}]")
        copy_to(dest, a.force, a.dry_run)
    if a.agents_md:
        path = Path(a.agents_md).expanduser()
        base = targets[0][1] if targets and a.project else (targets[0][1] if targets and a.dest else SKILLS)
        block = AGENTS_MD.format(path=base)
        print(f"[AGENTS.md] {'(thử) ' if a.dry_run else ''}thêm chỉ dẫn vào {path}")
        if not a.dry_run:
            path.parent.mkdir(parents=True, exist_ok=True)
            old = path.read_text(encoding="utf-8") if path.exists() else ""
            pattern = re.compile(re.escape(AGENTS_START) + r".*?" + re.escape(AGENTS_END), re.S)
            updated = pattern.sub(lambda _: block.rstrip(), old)
            if updated == old:
                updated = old.rstrip() + "\n" + block
            path.write_text(updated, encoding="utf-8")
    if not a.dry_run:
        print("\nKiểm tra môi trường:")
        subprocess.run([sys.executable, str(SKILLS / "onboard" / "scripts" / "doctor.py")], check=True)


if __name__ == "__main__":
    main()

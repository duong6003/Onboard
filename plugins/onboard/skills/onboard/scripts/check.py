#!/usr/bin/env python3
"""
check.py - kiểm tra story.json trước khi giao.

Usage:
  python check.py story.json                 # kiểm tra tĩnh
  python check.py story.json --render OUTDIR # kiểm tra tĩnh + build + chụp từng bước mọi ngôn ngữ

Exit code 0 = không có lỗi (có thể còn cảnh báo), 1 = có lỗi.
"""
import json
import re
import sys
import argparse
from pathlib import Path

from console import configure_utf8

HERE = Path(__file__).resolve().parent

LEVELS = {"low", "medium", "high", "ultra"}
SKELETONS = {"su-viec", "giai-thich", "thay-doi", "quyet-dinh", "trang-thai", "huong-dan", "custom"}
NOTE_TYPES = {"illustration", "assumption", "proposal", "unconfirmed", "target", "source"}
LABELLED_BASIS = {"illustration", "assumption", "proposal", "unconfirmed", "target"}
BASIS_VALUES = {"fact", *LABELLED_BASIS}
PATTERNS = {"grid", "timeline", "bars", "flow", "compare", "stats", "list", "checks", "custom",
            "sequence", "states", "heatmap", "slider", "calc", "quiz", "matrix"}
FORMATS = {"stepper", "scroll", "onepage"}
STYLES = {"clean", "dark", "sketch", "editorial"}
LAYOUTS = {"split", "hero", "center"}

# Cụm từ "rò rỉ yêu cầu": chỉ dẫn cho người viết lọt vào nội dung cho người đọc.
LEAK = {
    "vi": ["đọc nhanh", "đọc trong 1 phút", "đọc trong một phút", "hiểu trong 1 phút", "hiểu trong một phút", "tóm tắt trong 1 phút", "1 phút là hiểu", "dễ hiểu", "dành cho người mới",
           "giải thích đơn giản", "theo yêu cầu", "như đã yêu cầu", "đọc phần", "các phần sau", "phần dưới đây",
           "hình dưới đây", "sơ đồ dưới đây", "tài liệu này", "ngắn gọn", "siêu dễ", "cực kỳ dễ"],
    "en": ["read in 1 minute", "read in one minute", "1-minute read", "understand in 1 minute", "quick read", "easy to understand", "for beginners", "for newcomers",
           "simple explanation", "as requested", "per your request", "read this section", "the following sections",
           "the diagram below", "the image below", "this document", "super easy", "in short"],
    "ja": ["1分でわかる", "1分で読める", "一分でわかる", "わかりやすく", "分かりやすく", "初心者向け", "簡単に説明", "ご依頼", "ご要望により",
           "以下の図", "本資料では"],
}
GENERIC_TITLES = {
    "vi": {"tóm tắt", "tóm lại", "giới thiệu", "tổng quan", "kết luận", "nội dung chính", "mở đầu"},
    "en": {"summary", "overview", "introduction", "conclusion", "recap", "intro"},
    "ja": {"まとめ", "概要", "はじめに", "結論"},
}
SENSITIVE = [
    ("email", re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")),
    ("ip", re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b")),
    ("jwt", re.compile(r"eyJ[\w-]{10,}\.[\w-]{10,}\.[\w-]{5,}")),
    ("secret", re.compile(r"(?i)(?:\bauthorization\b\s*:\s*)?(?:\bbearer\b|\bapi[_-]?key\b|\btoken\b|\bsecret\b|\bpassword\b|\bpasswd\b)\s*(?:[:=]|\s)\s*\S+")),
    ("hex-token", re.compile(r"\b[0-9a-fA-F]{32,}\b")),
    ("path", re.compile(r"(?:[A-Za-z]:\\[^\s]+)|(?:/(?:home|Users|var|etc|opt|srv)/[^\s]+)")),
    ("internal-host", re.compile(r"\b(?:localhost|[\w-]+\.(?:local|internal|lan|corp))\b")),
]
# Khóa không chứa chữ hiển thị (cấu trúc, trạng thái, số).
STRUCT_KEYS = {"pattern", "anim", "status", "from", "to", "col", "lane", "id", "max", "blocks", "together",
               "reveal", "showMiss", "headSpan", "rowCount", "colCount", "cells", "order", "highlight", "kind",
               "type", "at", "dim", "decimals", "links", "focus", "state", "shape", "basis",
               "sources", "during", "_uid", "expr", "valueExpr", "maxExpr", "if", "min", "step",
               "answer", "scale", "path", "current", "start", "row", "decimals", "format", "unit_", "layout", "recommend"}
LIMITS = {"title": {"default": 70, "ja": 36}, "body": {"default": 260, "ja": 130}, "chip": {"default": 120, "ja": 60}}


EXPR_FUNCS = {"min", "max", "round", "floor", "ceil", "abs"}
EXPR_TOKEN = re.compile(r"\s*(?:(\d*\.?\d+)|([A-Za-z_][A-Za-z0-9_]*)|(<=|>=|==|!=|&&|\|\||[-+*/%()<>!,]))")


def expr_problems(src, names):
    """Kiểm tra cú pháp biểu thức calc theo đúng grammar của engine JavaScript."""
    s = str(src).strip()
    if not s:
        return "biểu thức không được rỗng"
    tokens, pos = [], 0
    while pos < len(s):
        m = EXPR_TOKEN.match(s, pos)
        if not m:
            return f"ký tự không hợp lệ ở vị trí {pos}: '{s[pos:pos + 8]}'"
        token = m.group(0).strip()
        tokens.append(token)
        pos = m.end()

    at = 0

    def peek(*wanted):
        return at < len(tokens) and tokens[at] in wanted

    def take(token=None):
        nonlocal at
        if at >= len(tokens) or (token is not None and tokens[at] != token):
            return None
        value = tokens[at]
        at += 1
        return value

    def primary():
        if take("("):
            error = logical_or()
            if error:
                return error
            if not take(")"):
                return "ngoặc không cân"
            return None
        token = take()
        if token is None:
            return "thiếu toán hạng"
        if re.fullmatch(r"\d*\.?\d+", token):
            return None
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", token):
            return f"cần toán hạng trước '{token}'"
        if take("("):
            if token not in EXPR_FUNCS:
                return f"hàm '{token}' không được phép"
            if peek(")"):
                return f"hàm '{token}' cần ít nhất một đối số"
            error = logical_or()
            if error:
                return error
            while take(","):
                error = logical_or()
                if error:
                    return error
            if not take(")"):
                return "ngoặc không cân"
            return None
        if token not in names:
            return f"tên '{token}' không phải input hoặc hàm cho phép"
        return None

    def unary():
        if peek("-", "!"):
            take()
        return primary() if not peek("-", "!") else unary()

    def binary(next_level, operators):
        error = next_level()
        if error:
            return error
        while peek(*operators):
            take()
            error = next_level()
            if error:
                return error
        return None

    def multiplication():
        return binary(unary, ("*", "/", "%"))

    def addition():
        return binary(multiplication, ("+", "-"))

    def comparison():
        error = addition()
        if error:
            return error
        if peek("<=", ">=", "==", "!=", "<", ">"):
            take()
            return addition()
        return None

    def logical_and():
        return binary(comparison, ("&&",))

    def logical_or():
        return binary(logical_and, ("||",))

    error = logical_or()
    if error:
        return error
    if at != len(tokens):
        return f"thừa token '{tokens[at]}'"
    return None


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s)


def sentences(s, lang):
    s = strip_tags(s).strip()
    if not s:
        return 0
    if lang == "ja":
        parts = [p for p in re.split(r"(?<=[。！？])", s) if p.strip()]
    else:
        parts = [p for p in re.split(r"(?<=[.!?])\s+", s) if p.strip()]
    return len(parts)


def localized_values(v, langs):
    if isinstance(v, dict):
        return {k: str(value) for k, value in v.items() if isinstance(value, (str, int, float))}
    if isinstance(v, (str, int, float)):
        return {lang: str(v) for lang in langs}
    return {}


class Report:
    def __init__(self):
        self.errors, self.warnings, self.infos = [], [], []

    def err(self, where, msg):
        self.errors.append(f"[LỖI] {where}: {msg}")

    def warn(self, where, msg):
        self.warnings.append(f"[CẢNH BÁO] {where}: {msg}")

    def info(self, where, msg):
        self.infos.append(f"[GHI CHÚ] {where}: {msg}")

    def ok(self):
        return not self.errors


def walk_strings(node, path, out):
    """Collect (path, value) for every renderable text field inside a visual spec."""
    if isinstance(node, dict):
        if node and all(isinstance(k, str) and len(k) <= 3 and k.isalpha() and k.islower() for k in node.keys()) \
                and all(isinstance(x, str) for x in node.values()):
            out.append((path, node))
            return
        for k, v in node.items():
            if k == "cells" and isinstance(v, list):
                walk_strings(v, f"{path}.{k}", out)
                continue
            if k in STRUCT_KEYS:
                continue
            walk_strings(v, f"{path}.{k}", out)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk_strings(v, f"{path}[{i}]", out)
    elif isinstance(node, str):
        out.append((path, node))


def static_check(story):
    r = Report()
    if not isinstance(story, dict):
        r.err("story", "root phải là object JSON")
        return r
    raw_langs = story.get("langs")
    if raw_langs is None:
        langs = ["vi"]
    elif not isinstance(raw_langs, list) or not raw_langs or any(not isinstance(lang, str) or not lang.strip() for lang in raw_langs):
        r.err("langs", "phải là danh sách mã ngôn ngữ không rỗng")
        langs = ["vi"]
    else:
        langs = raw_langs
        if len(set(langs)) != len(langs):
            r.err("langs", "không được lặp mã ngôn ngữ")
    default_lang = story.get("defaultLang")
    if default_lang is not None and default_lang not in langs:
        r.err("defaultLang", "phải là một mã trong 'langs'")
    if not isinstance(story.get("id"), str) or not story.get("id").strip():
        r.warn("id", "nên có id ổn định để lưu ngôn ngữ đã chọn; trang không có id sẽ không lưu tùy chọn này")
    lint = story.get("lint")
    allow_values = lint.get("allow", []) if isinstance(lint, dict) else []
    allow = [a.lower() for a in allow_values if isinstance(a, str)]
    multi = len(langs) > 1

    brief = story.get("brief")
    if not isinstance(brief, dict):
        r.err("brief", "thiếu brief (người nhận, phạm vi chia sẻ, mức, khung xương). Brief không bao giờ hiển thị nhưng bắt buộc có.")
        brief = {}
    level = brief.get("level", "medium")
    sharing = brief.get("sharing")
    if level not in LEVELS:
        r.err("brief.level", f"'{level}' không hợp lệ ({', '.join(sorted(LEVELS))})")
    if sharing not in ("internal", "external"):
        r.err("brief.sharing", "phải là 'internal' hoặc 'external' (quyết định cái gì được hiện)")
    for k in ("recipient", "purpose", "skeleton"):
        if not brief.get(k):
            r.err(f"brief.{k}", "bắt buộc")
    if brief.get("skeleton") and brief["skeleton"] not in SKELETONS:
        r.warn("brief.skeleton", f"'{brief['skeleton']}' không nằm trong danh sách khung xương đã biết")

    if story.get("format", "stepper") not in FORMATS:
        r.err("format", f"phải là một trong {sorted(FORMATS)}")
    if story.get("style", "clean") not in STYLES:
        r.err("style", f"phải là một trong {sorted(STYLES)}")
    meta = story.get("meta") or {}
    if not isinstance(meta, dict):
        r.err("meta", "phải là object")
        meta = {}
    if not meta.get("title"):
        r.err("meta.title", "bắt buộc")

    steps = story.get("steps") or []
    if not isinstance(steps, list):
        r.err("steps", "phải là danh sách")
        steps = []
    if len(steps) < 2:
        r.err("steps", "cần ít nhất 2 bước")
    if len(steps) > 12:
        r.warn("steps", f"{len(steps)} bước, quá dài; cân nhắc gộp hoặc tách thành 2 trang")

    texts = []  # (where, kind, value)
    for f in ("title", "subtitle", "footer"):
        if meta.get(f):
            texts.append((f"meta.{f}", "meta", meta[f]))

    for i, s in enumerate(steps):
        w = f"bước {i + 1}"
        if not isinstance(s, dict):
            r.err(w, "phải là object")
            continue
        if not s.get("title"):
            r.err(w, "thiếu tiêu đề")
        texts.append((f"{w}.title", "title", s.get("title", "")))
        if s.get("body"):
            texts.append((f"{w}.body", "body", s["body"]))
        chips = s.get("chips") or []
        if not isinstance(chips, list):
            r.err(w, "chips phải là danh sách")
            chips = []
        if len(chips) > 2:
            r.warn(w, f"{len(chips)} chip; tối đa nên là 2")
        for j, c in enumerate(chips):
            if not isinstance(c, dict):
                r.err(f"{w}.chips[{j}]", "phải là object")
                continue
            texts.append((f"{w}.chips[{j}]", "chip", c.get("text", "")))
        checks = s.get("checks") or []
        if not isinstance(checks, list):
            r.err(w, "checks phải là danh sách")
            checks = []
        for j, c in enumerate(checks):
            if not isinstance(c, dict):
                r.err(f"{w}.checks[{j}]", "phải là object")
                continue
            texts.append((f"{w}.checks[{j}]", "chip", c.get("text", "")))
            texts.append((f"{w}.checks[{j}].verdict", "chip", c.get("verdict", "")))
        raw_notes = s.get("notes")
        if raw_notes is not None and not isinstance(raw_notes, list):
            r.err(f"{w}.notes", "phải là danh sách")
            raw_notes = []
        notes = raw_notes or ([s["note"]] if s.get("note") else [])
        for j, n in enumerate(notes):
            if not isinstance(n, dict):
                r.err(f"{w}.note[{j}]", "phải là object")
                continue
            if n.get("type") not in NOTE_TYPES:
                r.err(f"{w}.note", f"type phải là một trong {sorted(NOTE_TYPES)}")
            texts.append((f"{w}.note", "chip", n.get("text", "")))
        if s.get("alt"):
            texts.append((f"{w}.alt", "alt", s["alt"]))
        elif s.get("visual"):
            r.warn(w, "thiếu alt (mô tả hình cho trình đọc màn hình)")

        basis = s.get("basis", "fact")
        if basis not in BASIS_VALUES:
            r.err(w, f"basis phải là một trong {sorted(BASIS_VALUES)}")
            basis = "fact"
        if basis in LABELLED_BASIS and not any(n.get("type") == basis for n in notes):
            r.err(w, f"basis='{basis}' nhưng không có note type '{basis}' hiển thị trên trang")
        if basis == "fact":
            has_num = bool(re.search(r"\d", json.dumps(s.get("body", ""), ensure_ascii=False) + json.dumps(s.get("title", ""), ensure_ascii=False)))
            if level in ("high", "ultra") and not s.get("sources"):
                r.err(w, f"mức {level}: bước dựa trên sự thật phải có 'sources'")
            elif level == "medium" and has_num and not s.get("sources"):
                r.warn(w, "có số liệu nhưng không ghi 'sources'")

        if s.get("layout", "split") not in LAYOUTS:
            r.err(w, f"layout phải là một trong {sorted(LAYOUTS)}")
        vis = s.get("visual")
        vlist = vis if isinstance(vis, list) else ([vis] if vis else [])
        if vis is not None and not isinstance(vis, (dict, list)):
            r.err(f"{w}.visual", "phải là object hoặc danh sách object")
            vlist = []
        for v in list(vlist):
            if isinstance(v, dict) and v.get("pattern") == "slider":
                vlist = vlist + [x for x in (v.get("before"), v.get("after")) if isinstance(x, dict)]
        for k, v in enumerate(vlist):
            if not isinstance(v, dict):
                r.err(f"{w}.visual[{k}]", "phải là object")
                continue
            pat = v.get("pattern")
            if pat not in PATTERNS:
                r.err(f"{w}.visual[{k}]", f"pattern '{pat}' không tồn tại ({', '.join(sorted(PATTERNS))})")
            if pat == "custom":
                h = v.get("html", "")
                if re.search(r"<script|\son\w+\s*=|javascript:", h, re.I):
                    r.err(f"{w}.visual[{k}]", "custom html không được chứa script hoặc thuộc tính on*")
            if pat == "timeline" and len(v.get("points") or []) > 7:
                r.warn(f"{w}.visual[{k}]", "timeline quá 7 điểm sẽ chật")
            if pat == "calc":
                inputs = v.get("inputs", []) or []
                if not isinstance(inputs, list):
                    r.err(f"{w}.visual[{k}].inputs", "phải là danh sách")
                    inputs = []
                names = set()
                for ii, inp in enumerate(inputs):
                    if not isinstance(inp, dict):
                        r.err(f"{w}.visual[{k}].inputs[{ii}]", "phải là object")
                        continue
                    input_id = inp.get("id")
                    if not isinstance(input_id, str) or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", input_id):
                        r.err(f"{w}.visual[{k}].inputs[{ii}].id", "chỉ được dùng chữ, số và '_' và không bắt đầu bằng số")
                    elif input_id in names:
                        r.err(f"{w}.visual[{k}].inputs[{ii}].id", "bị trùng")
                    else:
                        names.add(input_id)
                exprs = [o.get("expr") for o in v.get("outputs", [])]
                exprs += [rule.get("if") for o in v.get("outputs", []) for rule in o.get("status", [])]
                b = v.get("bars") or {}
                exprs += [row.get("valueExpr") for row in b.get("rows", [])] + [b.get("maxExpr"), (b.get("limit") or {}).get("valueExpr")]
                for e in exprs:
                    if e is None:
                        continue
                    pr = expr_problems(e, names)
                    if pr:
                        r.err(f"{w}.visual[{k}]", f"biểu thức \"{e}\": {pr}")
            if pat == "quiz":
                for qi, q in enumerate(v.get("questions", [])):
                    if not isinstance(q.get("answer"), int) or not (0 <= q["answer"] < len(q.get("options", []))):
                        r.err(f"{w}.visual[{k}].questions[{qi}]", "answer phải là chỉ số của một option")
            if pat == "sequence":
                ids = {p_.get("id") for p_ in v.get("participants", [])}
                for mi, m_ in enumerate(v.get("messages", [])):
                    if m_.get("from") not in ids or m_.get("to") not in ids:
                        r.err(f"{w}.visual[{k}].messages[{mi}]", "from/to phải là id của participants")
                if len(ids) > 5:
                    r.warn(f"{w}.visual[{k}]", "sơ đồ trình tự quá 5 bên sẽ chật trên điện thoại")
            if pat == "flow":
                ncol = max([n.get("col", 0) for n in v.get("nodes", [])] + [0]) + 1
                if v.get("lanes") and ncol >= 4:
                    r.warn(f"{w}.visual[{k}]", f"luồng có làn với {ncol} cột sẽ phải cuộn ngang trên điện thoại; cân nhắc ≤ 3 cột hoặc dùng checks")
            if pat == "grid" and ((v.get("cols") and len(v["cols"]) > 24) or (v.get("colCount", 0) > 24)):
                r.warn(f"{w}.visual[{k}]", "lưới quá 24 cột sẽ khó đọc trên điện thoại")
            out = []
            walk_strings(v, f"{w}.visual[{k}]", out)
            for p, val in out:
                texts.append((p, "visual", val))

    audience = brief.get("audience")
    goal = audience.get("goal") if isinstance(audience, dict) else None
    if brief.get("skeleton") == "quyet-dinh" or goal == "decide":
        pats = []
        for st_ in steps:
            vv = st_.get("visual")
            for x in (vv if isinstance(vv, list) else ([vv] if vv else [])):
                pats.append(x.get("pattern"))
        if not any(p_ in ("compare", "matrix") for p_ in pats):
            (r.err if brief.get("skeleton") == "quyet-dinh" else r.warn)("quyết định", "thiếu bước so sánh phương án (compare hoặc matrix); người duyệt cần thấy ít nhất 2 hướng")
        if len(steps) < 4:
            r.warn("quyết định", "lõi lập luận thường cần ≥ 4 bước: cần duyệt gì, vì sao, phương án, rủi ro/điểm dừng")
        last = steps[-1] if steps else {}
        lv = last.get("visual")
        lpats = [x.get("pattern") for x in (lv if isinstance(lv, list) else ([lv] if lv else []))]
        if not (set(lpats) & {"list", "checks"} or last.get("checks")):
            r.warn("quyết định", "bước cuối nên là danh sách việc cần quyết (list/checks) kèm hạn")
        obj = brief.get("objections")
        if level in ("medium", "high", "ultra"):
            if not obj:
                r.err("brief.objections", "trang quyết định phải liệt kê 3–5 câu người duyệt sẽ hỏi, mỗi câu trỏ tới bước trả lời hoặc ghi 'gap'")
            else:
                for oi, o in enumerate(obj):
                    if isinstance(o.get("step"), int):
                        if not (1 <= o["step"] <= len(steps)):
                            r.err(f"brief.objections[{oi}]", "step phải là số thứ tự bước (bắt đầu từ 1)")
                    elif o.get("gap"):
                        r.warn(f"brief.objections[{oi}]", f"chưa trả lời: \"{o.get('q', '')}\"; đưa vào 'cần xác nhận' khi báo lại")
                    else:
                        r.err(f"brief.objections[{oi}]", "cần 'step' (bước trả lời) hoặc 'gap' (lý do chưa trả lời)")

    for where, kind, val in texts:
        vals = localized_values(val, langs)
        if isinstance(val, dict):
            missing = [l for l in langs if not str(val.get(l, "")).strip()]
            if missing:
                r.err(where, f"thiếu bản dịch: {', '.join(missing)}")
        elif multi and isinstance(val, str) and re.search(r"[^\W\d_]", val) and re.search(r"\s", val.strip()):
            r.warn(where, f"chuỗi chưa dịch: \"{val[:40]}\" (bỏ qua nếu là tên riêng/mã)")
        for lang, text in vals.items():
            plain = strip_tags(text)
            raw = str(text)
            low = plain.lower()
            for phrase in LEAK.get(lang, []) + (LEAK["en"] if lang not in LEAK else []):
                if phrase.lower() in low and phrase.lower() not in allow:
                    r.err(f"{where} [{lang}]", f"rò rỉ yêu cầu: \"{phrase}\" (nói về tài liệu/người viết, không nói về sự việc)")
            if kind in LIMITS:
                lim = LIMITS[kind].get(lang, LIMITS[kind]["default"])
                if len(plain) > lim:
                    r.warn(f"{where} [{lang}]", f"{len(plain)} ký tự, nên ≤ {lim}")
            if kind == "body" and sentences(text, lang) > 2:
                r.warn(f"{where} [{lang}]", f"{sentences(text, lang)} câu, tối đa nên là 2")
            if kind == "title" and plain.strip().lower().rstrip(".:") in GENERIC_TITLES.get(lang, set()):
                r.err(f"{where} [{lang}]", f"tiêu đề là nhãn chung \"{plain}\"; tiêu đề phải là kết luận của bước")
            if sharing == "external":
                for name, rx in SENSITIVE:
                    if rx.search(raw) or rx.search(plain):
                        r.err(f"{where} [{lang}]", f"dữ liệu nhạy cảm ({name}) trong tài liệu gửi ra ngoài; chạy redact.py hoặc bỏ")
    if not r.errors:
        r.info("story", f"{len(steps)} bước · {len(langs)} ngôn ngữ · mức {level} · {sharing}")
    return r


def render_check(story_path, outdir, report):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        report.warn("render", "không có playwright; bỏ qua kiểm tra hiển thị")
        return
    sys.path.insert(0, str(HERE))
    from build import build_html
    outdir = Path(outdir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    html_path = outdir / "preview.html"
    html_path.write_text(build_html(json.loads(Path(story_path).read_text(encoding="utf-8-sig"))), encoding="utf-8")
    shots = {}
    clip_sel = [".text h2", ".chip", ".check", ".fl-node", ".b-name", ".stat .v", ".cmp-it", ".lst li", ".legend span", ".g-head div"]
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for (w, h, tag) in [(1200, 820, "desktop"), (390, 844, "mobile")]:
            page = browser.new_page(viewport={"width": w, "height": h}, reduced_motion="reduce")
            errs = []
            page.on("pageerror", lambda e: errs.append(str(e)))
            page.on("console", lambda m: errs.append(m.text) if m.type == "error" and "Failed to load resource" not in m.text else None)
            page.goto(html_path.as_uri())
            page.wait_for_timeout(300)
            info = page.evaluate("window.__onboard ? {count: window.__onboard.count, langs: window.__onboard.langs, format: window.__onboard.format} : null")
            if not info:
                report.err(f"render/{tag}", "trang không khởi tạo được (window.__onboard không tồn tại)")
                continue
            for lang in info["langs"]:
                page.evaluate(f"window.__onboard.setLang({json.dumps(lang)})")
                for i in range(info["count"]):
                    where = f"render/{tag}/{lang}/bước {i + 1}"
                    try:
                        page.evaluate(f"window.__onboard.go({i})")
                    except Exception as e:  # lỗi dựng hình của bước này
                        report.err(where, f"lỗi khi dựng bước: {str(e).splitlines()[0][:160]}")
                        continue
                    page.wait_for_timeout(120)
                    res = page.evaluate("""([sels, i]) => {
                      const d = document.documentElement, v = window.__onboard.visual(i);
                      const clipped = [];
                      sels.forEach(s => document.querySelectorAll(s).forEach(e => {
                        const must = s === '.stat .v';
                        if (e.scrollWidth > e.clientWidth + 1 && (must || getComputedStyle(e).overflow !== 'visible')) clipped.push(s + ': ' + (e.textContent || '').trim().slice(0, 30));
                      }));
                      return { pageOverflow: d.scrollWidth > window.innerWidth + 1, visOverflow: v.scrollWidth > v.clientWidth + 2,
                               visEmpty: v.children.length === 0, clipped: clipped };
                    }""", [clip_sel, i])
                    if res["pageOverflow"]:
                        report.err(where, "trang tràn ngang")
                    if res["visOverflow"]:
                        report.err(where, "hình tràn khỏi khung")
                    if res["visEmpty"] and story_has_visual(story_path, i):
                        report.err(where, "hình không hiển thị")
                    for c in res["clipped"][:4]:
                        report.warn(where, f"chữ bị cắt: {c}")
                    if info.get("format") == "onepage" and i > 0:
                        continue
                    shot = outdir / f"{tag}-{lang}-{i + 1:02d}.png"
                    page.screenshot(path=str(shot), full_page=(tag == "mobile" or info.get("format") == "onepage"))
                    shots.setdefault((tag, lang), []).append(shot)
            for e in errs:
                report.err(f"render/{tag}", f"lỗi JavaScript: {e}")
            page.close()
        browser.close()
    try:
        from PIL import Image
        for (tag, lang), files in shots.items():
            ims = [Image.open(f) for f in files]
            tw = 600 if tag == "desktop" else 300
            th = int(ims[0].height * tw / ims[0].width) if tag == "desktop" else 640
            cols = 2 if tag == "desktop" else 4
            rows = (len(ims) + cols - 1) // cols
            sheet = Image.new("RGB", (tw * cols, th * rows), "white")
            for k, im in enumerate(ims):
                im2 = im.copy()
                im2.thumbnail((tw, th) if tag == "desktop" else (tw, 10000))
                sheet.paste(im2.crop((0, 0, min(tw, im2.width), min(th, im2.height))), ((k % cols) * tw, (k // cols) * th))
            sheet.save(outdir / f"sheet-{tag}-{lang}.png")
        report.info("render", f"ảnh chụp và sheet-*.png nằm trong {outdir}")
    except Exception as e:  # pillow optional
        report.info("render", f"không tạo được contact sheet ({e})")


def story_has_visual(story_path, i):
    s = json.loads(Path(story_path).read_text(encoding="utf-8-sig"))
    return bool((s.get("steps") or [])[i].get("visual"))


def main():
    configure_utf8()
    ap = argparse.ArgumentParser(description="Kiểm tra story.json của skill onboard")
    ap.add_argument("story")
    ap.add_argument("--render", metavar="OUTDIR", help="build và chụp từng bước mọi ngôn ngữ vào OUTDIR")
    ap.add_argument("--json", action="store_true", help="in kết quả dạng JSON")
    a = ap.parse_args()
    story = json.loads(Path(a.story).read_text(encoding="utf-8-sig"))
    rep = static_check(story)
    if a.render:
        render_check(a.story, a.render, rep)
    if a.json:
        print(json.dumps({"errors": rep.errors, "warnings": rep.warnings, "infos": rep.infos}, ensure_ascii=False, indent=2))
    else:
        for line in rep.errors + rep.warnings + rep.infos:
            print(line)
        print(f"\n=> {len(rep.errors)} lỗi, {len(rep.warnings)} cảnh báo")
    sys.exit(0 if rep.ok() else 1)


if __name__ == "__main__":
    main()

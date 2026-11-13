#!/usr/bin/env python3
"""content_lint.py — kiểm "quy tắc cứng" khi viết content (CLAUDE.md §6, §7).

Hai chế độ:
  1. Hook (PostToolUse):  python3 scripts/content_lint.py --hook
     Đọc JSON hook từ stdin, chỉ lint file trong content/ (.md/.html). Luôn exit 0
     (không chặn write); in cảnh báo để Claude thấy và tự sửa trước khi đổi Status.
  2. Standalone:          python3 scripts/content_lint.py <file...> [--strict]
     In báo cáo. Với --strict, exit 1 nếu có lỗi (dùng ở cổng "Draft Ready").

Cấu hình theo dự án (nếu có): project/brand/rules.yaml, khóa:
  lint.banned_words: [..]      # thêm từ cấm của brand
  lint.spelling: en-GB|en-US   # kiểm vài cặp chính tả phổ biến
  content.min_internal_links: N
Không có file đó thì dùng mặc định bên dưới.
"""
import sys, os, re, json, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEFAULT_BANNED = [
    "state-of-the-art", "world-class", "cutting-edge", "best-in-class",
    "game-changing", "seamless", "eco-friendly", "unparalleled", "robust",
    "vibrant", "bustling", "charming", "picturesque", "must-visit", "ultimate",
    "amazing", "incredible", "stunning", "delve into", "unlock", "embark on a journey",
    "in today's fast-paced world", "navigate the landscape",
]
# Mở đầu/đóng bài sáo mòn (AI tells)
AI_TELLS = [
    r"in conclusion", r"in this article, we will", r"it'?s important to note that",
    r"whether you'?re a beginner or an expert", r"at the end of the day",
]
# Vài cặp chính tả US↔UK để cảnh báo khi sai market
UK_SPELLING = {"color": "colour", "organize": "organise", "center": "centre",
               "traveler": "traveller", "neighborhood": "neighbourhood", "program": "programme"}
US_SPELLING = {v: k for k, v in UK_SPELLING.items()}


def load_rules():
    rules = {"banned": list(DEFAULT_BANNED), "spelling": None, "min_links": 2}
    p = os.path.join(ROOT, "project", "brand", "rules.yaml")
    if not os.path.exists(p):
        return rules
    try:
        import yaml  # optional
        with open(p, encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    except Exception:
        # đọc thô vài khóa nếu không có pyyaml
        return rules
    lint = (data.get("lint") or {})
    rules["banned"] += [w.lower() for w in (lint.get("banned_words") or [])]
    rules["spelling"] = lint.get("spelling")
    rules["min_links"] = ((data.get("content") or {}).get("min_internal_links")) or 2
    return rules


def strip_frontmatter_and_code(text):
    # bỏ YAML frontmatter và code block để không báo nhầm
    text = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S)
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    return text


def body_only(text):
    # chỉ lấy phần Draft_EN/Draft_<lang>, bỏ "Client Confirmation List" trở xuống
    cut = re.split(r"(?i)client confirmation list|review appendix", text)[0]
    return cut


def lint_file(path, rules):
    with open(path, encoding="utf-8", errors="replace") as f:
        raw = f.read()
    text = strip_frontmatter_and_code(raw)
    body = body_only(text)
    issues = []

    # 1. em dash & semicolon trong thân bài
    if "—" in body:
        issues.append(("ERR", "em dash (—) trong thân bài — thay bằng dấu phẩy/ngoặc/câu mới"))
    for m in re.finditer(r";", body):
        # bỏ qua ; trong entity HTML như &nbsp;
        start = max(0, m.start() - 6)
        if "&" not in body[start:m.start()]:
            issues.append(("ERR", "dấu chấm phẩy (;) trong thân bài"))
            break

    low = body.lower()
    # 2. từ cấm / cliché
    for w in rules["banned"]:
        if re.search(r"\b" + re.escape(w) + r"\b", low):
            issues.append(("WARN", f"từ cấm/cliché: \"{w}\""))
    # 3. AI tells
    for pat in AI_TELLS:
        if re.search(pat, low):
            issues.append(("WARN", f"mẫu câu AI-tell: /{pat}/"))

    # 4. chính tả theo market
    if rules["spelling"] == "en-GB":
        for us, uk in UK_SPELLING.items():
            if re.search(r"\b" + us + r"\b", low):
                issues.append(("WARN", f"chính tả US \"{us}\" — brand dùng en-GB (\"{uk}\")"))
    elif rules["spelling"] == "en-US":
        for uk, us in US_SPELLING.items():
            if re.search(r"\b" + uk + r"\b", low):
                issues.append(("WARN", f"chính tả UK \"{uk}\" — brand dùng en-US (\"{us}\")"))

    # 5. định dạng số: 5.000 kiểu châu Âu (nên 5,000)
    if re.search(r"\b\d{1,3}\.\d{3}\b", body):
        issues.append(("WARN", "số kiểu \"5.000\" — dùng dấu phẩy ngăn nghìn (\"5,000\")"))

    # 6. internal link tối thiểu (markdown link tới cùng domain hoặc đường dẫn nội bộ)
    md_links = re.findall(r"\]\((https?://[^)]+|/[^)]+)\)", body)
    internal = [l for l in md_links if l.startswith("/") or "http" in l]
    if len(md_links) < rules["min_links"]:
        issues.append(("WARN", f"chỉ {len(md_links)} link, cần ≥ {rules['min_links']} internal link"))

    # 7. CTA cuối bài
    if not re.search(r"(?i)(contact|download|explore|book|enquir|get in touch|learn more|check availability)", body[-800:]):
        issues.append(("WARN", "không thấy CTA rõ ở cuối bài"))

    # 8. dữ kiện số chưa gắn tag (gợi ý, không chắc chắn)
    #    câu có số + đơn vị nhưng không có nguồn/tag gần đó → nhắc kiểm facts.yaml
    return issues


def iter_target_files(args):
    for a in args:
        if os.path.isdir(a):
            yield from glob.glob(os.path.join(a, "**", "*.md"), recursive=True)
            yield from glob.glob(os.path.join(a, "**", "*.html"), recursive=True)
        else:
            yield a


def run_standalone(argv):
    strict = "--strict" in argv
    files = [a for a in argv if not a.startswith("--")]
    rules = load_rules()
    total_err = 0
    for path in iter_target_files(files):
        if not os.path.exists(path):
            print(f"✗ không tìm thấy: {path}")
            continue
        issues = lint_file(path, rules)
        errs = [i for i in issues if i[0] == "ERR"]
        total_err += len(errs)
        rel = os.path.relpath(path, ROOT)
        if not issues:
            print(f"✓ {rel}: sạch")
        else:
            print(f"• {rel}: {len(errs)} lỗi, {len(issues)-len(errs)} cảnh báo")
            for lvl, msg in issues:
                print(f"    [{lvl}] {msg}")
    return 1 if (strict and total_err) else 0


def run_hook():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    ti = payload.get("tool_input", {}) or {}
    path = ti.get("file_path") or ti.get("path") or ""
    if not path:
        return 0
    rel = os.path.relpath(path, ROOT) if os.path.isabs(path) else path
    if not rel.startswith("content" + os.sep):
        return 0
    if not (path.endswith(".md") or path.endswith(".html")):
        return 0
    if not os.path.exists(path):
        return 0
    rules = load_rules()
    issues = lint_file(path, rules)
    if issues:
        print(f"[content_lint] {rel}:")
        for lvl, msg in issues:
            print(f"  [{lvl}] {msg}")
        print("  → sửa trước khi đổi Status sang 'Draft Ready'.")
    return 0  # không chặn write


if __name__ == "__main__":
    if "--hook" in sys.argv:
        sys.exit(run_hook())
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    sys.exit(run_standalone(sys.argv[1:]))

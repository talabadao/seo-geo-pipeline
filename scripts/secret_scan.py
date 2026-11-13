#!/usr/bin/env python3
"""secret_scan.py — chặn commit chứa secret (CLAUDE.md §3).

Hook (PreToolUse, matcher Bash): python3 scripts/secret_scan.py --hook
  Đọc JSON hook từ stdin. Chỉ xử lý lệnh có 'git commit'. Quét diff đã stage;
  nếu thấy secret, in lý do và exit 2 (chặn). Ngược lại exit 0.

Standalone: python3 scripts/secret_scan.py [path...]
  Quét file chỉ định (mặc định: diff đã stage).
"""
import sys, os, json, re, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PATTERNS = [
    (r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----", "private key"),
    (r"(?i)\bpassword\s*[:=]\s*['\"]?[^\s'\"]{6,}", "password gán giá trị"),
    (r"(?i)\b(api[_-]?key|secret|token)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}", "api key / token"),
    (r"AKIA[0-9A-Z]{16}", "AWS access key"),
    (r"ghp_[A-Za-z0-9]{36}", "GitHub token"),
    (r"AIza[0-9A-Za-z_\-]{35}", "Google API key"),
    (r"xox[baprs]-[0-9A-Za-z\-]{10,}", "Slack token"),
]
# Không báo nhầm trên file mẫu
ALLOW_FILES = ("credentials.example.yaml", ".env.example", "secret_scan.py")


def scan_text(text):
    hits = []
    for pat, label in PATTERNS:
        if re.search(pat, text):
            hits.append(label)
    return hits


def staged_files():
    try:
        out = subprocess.run(["git", "diff", "--cached", "--name-only"],
                             cwd=ROOT, capture_output=True, text=True, timeout=20)
        return [f for f in out.stdout.splitlines() if f.strip()]
    except Exception:
        return []


def staged_diff():
    try:
        out = subprocess.run(["git", "diff", "--cached"], cwd=ROOT,
                             capture_output=True, text=True, timeout=20)
        return out.stdout
    except Exception:
        return ""


def check_staged():
    problems = []
    files = staged_files()
    # Chặn commit nếu stage file nhạy cảm
    for f in files:
        base = os.path.basename(f)
        if base in ALLOW_FILES:
            continue
        if f.startswith(".credentials/") and base not in ("README.md", "credentials.example.yaml"):
            problems.append(f"{f}: file trong .credentials/ không được commit")
        if base in ("wp-config.php", ".env") or base.startswith(".env."):
            if not base.endswith(".example"):
                problems.append(f"{f}: file cấu hình nhạy cảm")
    # Quét nội dung diff
    diff = staged_diff()
    added = "\n".join(l[1:] for l in diff.splitlines() if l.startswith("+") and not l.startswith("+++"))
    for label in scan_text(added):
        problems.append(f"nội dung stage có vẻ chứa {label}")
    return problems


def run_hook():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    cmd = (payload.get("tool_input", {}) or {}).get("command", "")
    if "git commit" not in cmd:
        return 0
    problems = check_staged()
    if problems:
        print("[secret_scan] CHẶN COMMIT — nghi có secret:")
        for p in problems:
            print("  - " + p)
        print("  → bỏ file khỏi stage / chuyển secret sang .credentials/ rồi commit lại.")
        return 2  # exit code 2 = chặn tool trong Claude Code hook
    return 0


def run_standalone(paths):
    problems = []
    if not paths:
        problems = check_staged()
    else:
        for p in paths:
            try:
                with open(p, encoding="utf-8", errors="replace") as f:
                    for label in scan_text(f.read()):
                        problems.append(f"{p}: {label}")
            except Exception as e:
                print(f"✗ {p}: {e}")
    if problems:
        print("Nghi có secret:")
        for p in problems:
            print("  - " + p)
        return 1
    print("✓ không thấy secret")
    return 0


if __name__ == "__main__":
    if "--hook" in sys.argv:
        sys.exit(run_hook())
    sys.exit(run_standalone([a for a in sys.argv[1:] if not a.startswith("--")]))

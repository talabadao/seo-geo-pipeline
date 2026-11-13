#!/usr/bin/env bash
# sync-core.sh — kéo bản mới của Core từ template về repo dự án (chiến lược cập nhật v1).
# Chỉ đồng bộ .claude/, core/, scripts/ và CLAUDE.md. KHÔNG đụng project/, website/, content/,
# audits/, reports/, data/, .credentials/.
#
# Dùng trong repo DỰ ÁN:
#   scripts/sync-core.sh [TEMPLATE_GIT_URL] [BRANCH]
# Mặc định: template của agency, nhánh main.
set -euo pipefail

TEMPLATE_URL="${1:-https://github.com/talabadao/seo-geo-pipeline.git}"
BRANCH="${2:-main}"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "→ Lấy Core từ $TEMPLATE_URL ($BRANCH)"
git clone --depth 1 --branch "$BRANCH" "$TEMPLATE_URL" "$TMP" >/dev/null 2>&1

for path in .claude core scripts CLAUDE.md; do
  echo "→ Đồng bộ $path"
  rsync -a --delete "$TMP/$path" "./$(dirname "$path")/" 2>/dev/null || cp -r "$TMP/$path" "./"
done

echo "✓ Xong. Xem 'git diff' rồi commit. project/ và nội dung dự án KHÔNG bị đụng."
echo "  Nếu có tùy biến riêng, đặt trong project/overrides/ để không bị ghi đè lần sau."

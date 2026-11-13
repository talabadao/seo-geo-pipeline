# SEO/GEO Pipeline — Template

Template Claude Code cho quy trình SEO/GEO của agency. Mỗi khách hàng = một repo private
`seo-<slug>` tạo từ template này. Claude Code chạy phần lớn tác vụ phân tích, lập kế hoạch, viết
nội dung, audit kỹ thuật và báo cáo; người duyệt.

> Toàn bộ luật vận hành ở [`CLAUDE.md`](./CLAUDE.md). Kế hoạch triển khai ở
> [`docs/implementation-plan.md`](./docs/implementation-plan.md).

## Tạo dự án mới (mục tiêu ≤ 30 phút)

1. **Tạo repo:** GitHub › "Use this template" → `talabadao/seo-<slug>`, để **Private**.
2. **Mở trên claude.ai/code**, bật các connector: Google Drive, Sheets, Docs, Agency Analytics,
   DataForSEO, SERP API, SE Ranking, Firecrawl (và Figma nếu làm UI/UX).
3. **Chạy `/new-project "HOP### - Tên khách" domain.com`** — Claude tìm folder + Plan/Masterfile +
   Onboarding của dự án trên Drive, map ID vào `project/config.yaml`, đọc Onboarding và dựng brand
   pack nháp trong `project/brand/`.
4. **Điền nốt `project/brand/`** từ brand guideline của khách (hoặc chạy `/p01-onboarding`).
5. **Điền `.credentials/credentials.yaml`** (git-ignored) nếu cần đăng nhập CMS/hosting.
6. Bắt đầu pipeline: `/p02-access` → `/p03-foundation` → … (xem `docs/pipeline.md`).

## Cấu trúc

```
CLAUDE.md              Luật vận hành + rule viết content
core/                  Kiến thức dùng chung (KHÔNG sửa trong repo dự án)
  content-types/       infrastructure · velocity · authority
  formats/             khuôn từng dạng bài (toplist, travel-guide, what-is, ...)
  industries/          playbook theo ngành (hospitality, b2b-manufacturing, ...)
  markets/             chính tả/giọng/SERP theo thị trường & ngôn ngữ
  doc-templates/       khuôn Content Doc (Draft_EN/Draft_XX + Confirmation List)
  html-templates/      component HTML cho blog
  sheet-schemas/       định nghĩa cột 7 tab Plan + tab Masterfile
  checklists/          P02 access, P04d technical, QA content
  rules/               rule chi tiết (content, GEO, internal-link)
.claude/skills/        các lệnh /slash (research, outline, write, translate, ...)
.claude/agents/        subagent (serp-researcher, tech-auditor, ...)
scripts/               content_lint.py, forecast.py, crawl.py, ... + sync-core.sh
project/               ← PHẦN RIÊNG DỰ ÁN (điền sau khi clone)
  config.yaml          khách, ngôn ngữ, ID file Drive, analytics, ngân sách
  brand/               brand.md, facts.yaml, rules.yaml, internal-links.csv, glossary.csv, learned.md
  research/, overrides/, decisions.md
.credentials/          secret của dự án (git-ignored)
website/               source website (nếu hợp đồng cho phép, private)
content/ audits/ reports/ data/
```

## Cập nhật Core cho các dự án đang chạy

- **v1:** trong repo dự án, chạy `scripts/sync-core.sh` để kéo bản mới của `.claude/`, `core/`,
  `scripts/` từ template. Script không đụng `project/`, `website/`, `content/`, `audits/`,
  `reports/`.
- **v2:** đóng gói Core thành Claude Code plugin; dự án chỉ khai báo plugin, cập nhật một lần.

## Nguyên tắc an toàn

- Repo **private**. Không commit mật khẩu/PII (xem `.gitignore` + `.credentials/README.md`).
- Claude ghi vào bản nháp hoặc Status chờ duyệt; **không gửi gì trực tiếp cho khách**.
- Cổng duyệt: PIC chạy → SEN duyệt → AM/PM gửi khách.

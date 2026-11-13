---
name: outline
description: "Tạo outline SEO/GEO cho một keyword từ research brief + brand pack + format + industry + market. Bản nâng cấp của seo-outline: đọc project/brand thay vì Claude Project, chọn độ dài theo format, thêm phần GEO (answer chunk, entity, prompt), dùng URL thật cho internal link, xuất ra file + Google Doc + cập nhật Status. Dùng khi user gõ /outline hoặc sau /research. KHÔNG viết bài."
---

# outline  (nâng cấp seo-outline)

Tạo outline, **không** viết bài. Ghép lớp theo CLAUDE.md §6:
`brand > overrides > format > content-type > industry > market > core`.

## Trước khi bắt đầu
1. Đọc `project/config.yaml`, `project/brand/*` (brand.md, facts.yaml, rules.yaml, internal-links.csv,
   learned.md). Nếu thiếu brand pack → dừng, báo chạy `/p01-onboarding`.
2. Đọc research brief `content/YYYY-MM/<slug>/research.md`. Nếu chưa có → chạy `/research` trước.
3. Xác định **Content Type** (Infrastructure/Velocity/Authority) + **format** từ Content Plan
   (`core/formats/README.md` để route). Đọc file format tương ứng + `core/industries/<ngành>.md`
   + `core/markets/<locale>.md`.

## Khác với skill cũ (quan trọng)
- Nguồn brand = `project/brand/*`, KHÔNG phải "Claude Project".
- Danh sách domain loại khi phân tích đối thủ lấy từ `core/markets` + `core/industries`, KHÔNG viết
  cứng (hospitality giữ OTA trong research; B2B loại marketplace).
- **Độ dài theo format + `config.yaml › content.word_range`**, không cố định 1,200–1,500.
- Năm hiện tại tính theo ngày chạy, không viết cứng.
- Thêm **GEO**: mỗi H2 có answer chunk; liệt kê entity bắt buộc; prompt cần trả lời; dữ kiện
  facts.yaml để AI trích; nguồn AI Overview đang trích.
- Internal link = **URL thật** từ `internal-links.csv` (không bịa).
- Dữ kiện ngoài facts.yaml → đánh dấu để `/write` gắn tag.

## Cấu trúc outline (mỗi section)
H2 = một câu hỏi thật của người đọc (không lặp keyword). Mỗi section ghi:
- Summary (2–3 câu) · Main ideas (3–5 bullet) · Format (paragraph/list/table) · Word count ước tính
- **Answer chunk** (câu trả lời trực tiếp mở section) · **Entity** cần nêu
- E-E-A-T note · Internal link (URL thật + anchor) · External link (nguồn chuẩn) · Image nếu cần
Mở bằng: Title (H1), main keyword, secondary/LSI, meta description (140–160), tổng word count.
Kết: Conclusion (CTA + URL nội bộ thật) + FAQ 5–7 (từ PAA/research).

## Checklist trước khi trình
Vượt đối thủ ở một góc; mỗi H2 phục vụ reader; intent khớp; H1 có keyword; meta 140–160;
internal/external link xác định; dữ liệu 2026–2027 (theo ngày chạy); độ dài cộng khớp mục tiêu.

## Ghi ra
`content/YYYY-MM/<slug>/outline.md` → Google Doc "Outline – <title>" trong Content/YYYY-MM →
Content Plan: Status = `Outline Ready`, điền link Doc. Báo cần PIC/SEN duyệt. **Không viết bài tới
khi được duyệt.**

---
name: translate-content
description: "Dịch tự nhiên (không word-for-word) một bài hoặc trang HTML từ tiếng Anh (US/UK) sang Thái, Nga, Hàn, Nhật, Trung giản thể/phồn thể, Việt, Tây Ban Nha, Pháp, Đức... Giữ nguyên cấu trúc HTML/markdown, tag, ảnh, bảng; đổi internal link sang path ngôn ngữ đích; giữ thuật ngữ/tên brand theo glossary; chạy lint theo market đích. Dùng khi user gõ /translate hoặc sau /write với dự án đa ngôn ngữ."
---

# translate-content

Dịch sang ngôn ngữ trong `config.yaml › languages.secondary`. Dịch **tự nhiên, theo ngữ cảnh**,
không dịch cứng. Tái dùng kỹ năng org khi có: `translate-html`, `natural-vietnamese-writing`,
`bhaya-translate-html`; áp dụng tinh thần đó cho mọi ngôn ngữ.

## Input
File đã viết (`content/YYYY-MM/<slug>/draft.md` hoặc HTML) + ngôn ngữ đích. Đọc
`core/markets/<locale>.md` + `project/brand/glossary.csv`.

## Quy tắc
- **Giữ cấu trúc:** mọi tag HTML/markdown, thuộc tính, ảnh, video, bảng, embed giữ nguyên; chỉ dịch
  text node.
- **Tự nhiên, không literal:** viết lại theo cách người bản ngữ tìm kiếm/đọc; dịch lại SEO title &
  meta cho tự nhiên, không dịch từng chữ.
- **Glossary:** từ/tên đánh dấu `do_not_translate` giữ nguyên (tên brand, tên phòng/outlet, mã kỹ
  thuật). Thuật ngữ ngành theo market.
- **Internal link:** đổi path sang ngôn ngữ đích (ví dụ `/about` → `/th/about`), map theo quy ước
  `core/markets/<locale>.md`. Nếu URL nguồn không có bản dịch → giữ text, bỏ link (như bhaya rule).
- **Bảng & FAQ:** nếu market file có template riêng (ví dụ accordion), dùng template đó.
- **Số/ngày/tiền:** theo `core/markets/<locale>.md`.
- Giữ nguyên các tag `[NEED CLIENT CONFIRMATION]`/`[VERIFY]` (không dịch nội dung tag).

## Xuất ra
- `content/YYYY-MM/<slug>/translations/<locale>.md` (hoặc .html)
- Thêm phần `Draft_<lang>` vào cùng Google Doc, ngay dưới `Draft_EN`.
- Chạy `content_lint` theo market đích (chính tả/định dạng số của ngôn ngữ đó).
- Báo PIC; cập nhật Content Plan nếu có cột Publish URL (<lang>). Không gửi khách.

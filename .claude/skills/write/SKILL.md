---
name: write
description: "Viết bài hoàn chỉnh từ outline + brand pack, xuất ra Content Doc format The Sukosol (Draft_EN + bảng meta + Client Confirmation List). Bản nâng cấp của seo-article-writer: ghi vào content/ và Google Doc (không dùng path claude.ai), đối chiếu facts.yaml và tự gắn tag [NEED CLIENT CONFIRMATION]/[VERIFY], chèn disclaimer theo rules.yaml, chạy content_lint, đọc learned.md để không lặp lỗi cũ. Dùng khi user gõ /write hoặc sau khi outline được duyệt."
---

# write  (nâng cấp seo-article-writer)

Viết bài từ outline đã duyệt. Tuân thủ CLAUDE.md §6 + `core/rules/content-rules.md` +
`core/rules/geo-rules.md`.

## Trước khi viết
1. Đọc outline `content/YYYY-MM/<slug>/outline.md` + research brief.
2. Đọc `project/brand/*` — đặc biệt `facts.yaml`, `rules.yaml`, `learned.md`.
3. Viết voice brief nội bộ (3 tính từ giọng; 3 điều brand không bao giờ nói; reading level; chính
   tả market; thuật ngữ) từ `brand.md`.
4. Đọc format để biết độ dài/thành phần/FAQ word count.

## Quy tắc viết (bắt buộc)
- **Theo outline chính xác:** đúng H2/H3, đúng thứ tự, không thêm/bớt section.
- **Answer-first:** mỗi section mở bằng câu trả lời trực tiếp.
- **Đối chiếu dữ kiện với facts.yaml:**
  - có trong `approved:` → dùng thẳng.
  - không có / khách cần xác nhận → `[NEED CLIENT CONFIRMATION: nội dung | nguồn]` + thêm vào
    Client Confirmation List.
  - team tự kiểm được → `[VERIFY: nội dung]`.
  - nằm trong `verify:` (bị chặn) → **không khẳng định**; viết vòng hoặc bỏ, ghi chú.
  - không có nguồn và không tự kiểm được → `[STAT NEEDED: ...]`, tuyệt đối không bịa.
- **Disclaimer:** chèn theo `rules.yaml › disclaimers` đúng loại nội dung (commercial terms, product
  suitability, certifications, sustainable materials...).
- **Off-limits & từ cấm:** tuân `rules.yaml › off_limits` + `banned_words`; thay cliché bằng
  `superlative_swaps`.
- **Internal link:** đúng URL thật outline chỉ định; anchor mô tả; ≥ min_internal_links.
- **Punctuation cứng:** không em dash (—), không chấm phẩy (;) trong thân bài.
- **learned.md:** áp dụng mọi bài học trước đó của dự án.

## Thành phần
Title (H1 từ outline) · meta description verbatim · Intro 100–150 từ (mở bằng tình huống, không
keyword) · các H2/H3 · Conclusion 80–120 từ (CTA + URL nội bộ) · FAQ 5–7 (35–75 từ/câu theo format).

## Xuất ra (format The Sukosol — xem core/doc-templates/content-doc.md)
1. `content/YYYY-MM/<slug>/draft.md` — chạy **content_lint**; sửa tới khi 0 ERR.
2. Chạy agent `content-reviewer` (đóng vai SEN) chấm theo checklist.
3. Ghi vào Google Doc của bài: `Draft_EN` (bảng meta + bài) + **Client Confirmation List** ở cuối.
4. Nếu có ngôn ngữ 2 → gọi `/translate` để thêm `Draft_<lang>`.
5. Content Plan: Status = `Draft Ready` (chỉ khi lint 0 ERR), điền link Doc.

## Handoff note (chat, 3–6 dòng)
Word count vs mục tiêu; section gắn cờ (verify/thiếu số); directive outline không theo được và vì
sao; cần SEN duyệt. KHÔNG dán bài vào chat; bài nằm trong Doc. Không gửi khách.

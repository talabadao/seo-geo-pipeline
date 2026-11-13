---
name: new-project
description: "Khởi tạo một dự án SEO/GEO mới trong repo đã clone từ template. Tìm folder Drive + Plan/Masterfile/Onboarding của khách, map ID vào project/config.yaml, đọc Onboarding và dựng brand pack nháp. Dùng khi bắt đầu một khách mới, khi config.yaml còn trống, hoặc khi user gõ /new-project."
---

# new-project

Khởi tạo dự án mới. **Lưu ý quyền Drive:** tài khoản chạy Claude hiện chỉ có quyền **xem** folder
dự án, nên skill này chỉ *tìm và map* file có sẵn, **không tạo** file Drive. Khi được cấp Editor,
bật bước tạo folder/copy Sheet mẫu (đánh dấu TODO bên dưới).

## Input
`/new-project "<Tên khách>" domain.com` — kèm **folder URL/ID** nếu biết (khuyến nghị). Mã dự án
(HOP###, AD##, ...) tùy agency nên **match theo TÊN khách là chính**, mã là phụ.

## Các bước

1. **Tìm folder dự án** — KHÔNG giả định một root duy nhất (các agency/khách nằm ở nhiều nơi):
   - Nếu user đưa folder URL/ID → dùng thẳng làm `root_folder_id`.
   - Nếu không: `search_files` `title contains '<Tên khách>'` (và/hoặc mã), mimeType folder, trên cả
     My Drive lẫn Shared Drive. Nếu ra nhiều kết quả → hỏi user chọn. Nếu 0 → báo chưa có folder, dừng.
2. **Tìm file/folder con** (đệ quy qua `parentId`). Tên có thể khác nhau giữa dự án:
   - Thư mục "SEO - GEO" (nếu có) là nơi chứa Plan/Masterfile; nếu không, tìm ngay trong root.
   - Plan (`title contains 'Plan'`) → `plan_sheet_id`; Masterfile (`contains 'Masterfile'`) →
     `masterfile_sheet_id`.
   - Onboarding (`contains 'On-Boarding' | 'Onboarding' | 'Inquiry'`) → `onboarding_sheet_id` (CÓ THỂ
     KHÔNG TỒN TẠI — xem bước 5 fallback).
   - Folder Content / Research / Audit / Website Audit / Offsite / UI-UX / Reports → các *_folder_id
     (map đúng tên folder thật, đừng ép tên).
3. **Kiểm format Plan** = 7-tab core (Foundation, Problem Pattern(s), Tracking, Content Plan,
   Technical Baseline, Offsite, Measurement). Dự án có thể thêm tab (Measurement V3, Audit Website...)
   — chấp nhận, chỉ cảnh báo nếu THIẾU tab core. Format cũ (Ad-Lib/Bhaya) → hỏi có chuẩn hóa không.
4. **Ghi `project/config.yaml`** (trong repo DỰ ÁN, không phải template): project.* (gồm `code`),
   languages (từ Foundation/Onboarding target language), serp_locations (từ Foundation Target
   Location), drive.*, competitors (từ Foundation), analytics.gsc_property = sc-domain:<domain>.
5. **Nguồn onboarding → brand pack** `project/brand/` (theo thứ tự ưu tiên có gì dùng nấy):
   - (a) Sheet Onboarding Questions nếu có; (b) **tab Foundation của Plan**; (c) brand guideline trong
     folder Brand/Report; (d) hỏi user phần còn thiếu.
   - `brand.md` (định vị, voice, audience, mùa vụ) · `facts.yaml` (số liệu + mục `verify:`) ·
     `rules.yaml` (từ/claim tránh, chính tả) · `glossary.csv` (tên giữ nguyên).
   - **Cross-check Foundation vs brand guideline:** chỗ lệch (ví dụ Nam Dinh vs Ninh Binh) đưa vào
     `facts.yaml › verify:` kèm cả hai nguồn.
6. **internal-links.csv:** nếu có tab Site URL/sitemap → URL thật; chưa có → để trống, ghi chú chạy
   `/site-inventory`.
7. **Báo cáo:** ID đã map, brand pack còn thiếu, xung đột facts cần xác nhận, bước tiếp theo.

## TODO khi có quyền Editor Drive
- Copy cây folder + Plan/Masterfile/Onboarding từ "Drive Template" và đặt tên theo quy ước
  (`[YYYY] SEO/GEO Plan - <Client>`, folder tháng `YYYY-MM`).

## Ghi ra
`project/config.yaml`, `project/brand/*`, một dòng trong `project/decisions.md`.
Không gửi gì cho khách.

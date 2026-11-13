---
name: new-project
description: "Khởi tạo một dự án SEO/GEO mới trong repo đã clone từ template. Tìm folder Drive + Plan/Masterfile/Onboarding của khách, map ID vào project/config.yaml, đọc Onboarding và dựng brand pack nháp. Dùng khi bắt đầu một khách mới, khi config.yaml còn trống, hoặc khi user gõ /new-project."
---

# new-project

Khởi tạo dự án mới. **Lưu ý quyền Drive:** tài khoản chạy Claude hiện chỉ có quyền **xem** folder
dự án, nên skill này chỉ *tìm và map* file có sẵn, **không tạo** file Drive. Khi được cấp Editor,
bật bước tạo folder/copy Sheet mẫu (đánh dấu TODO bên dưới).

## Input
`/new-project "HOP### - Tên khách" domain.com` (hoặc hỏi user nếu thiếu).

## Các bước

1. **Tìm folder dự án** trong Drive root của agency (folder "New projects"):
   - `search_files` với `title contains '<Tên khách>'` hoặc `'HOP###'`, mimeType folder.
   - Lấy `root_folder_id`. Nếu không thấy: báo user chưa có folder, dừng.
2. **Tìm các file bên trong** (đệ quy qua `parentId`):
   - Onboarding Sheet (`title contains 'On-Boarding'`) → `onboarding_sheet_id`
   - Plan Sheet (`title contains 'Plan'`) → `plan_sheet_id`
   - Masterfile Sheet (`title contains 'Masterfile'`) → `masterfile_sheet_id`
   - Folder Content / Website Audit / Offsite / UI-UX / Reports → các *_folder_id
3. **Xác nhận format Plan** = 7 tab chuẩn (Foundation…Measurement). Nếu Plan dùng format cũ
   (Ad-Lib/Bhaya), báo user và hỏi có chuyển sang chuẩn không (câu hỏi B3).
4. **Ghi `project/config.yaml`:** điền project.*, languages (từ Onboarding target language),
   serp_locations, drive.*, analytics.gsc_property (= sc-domain:<domain>). Giữ các ID tìm được.
5. **Đọc Onboarding** (`read_file_content`) → dựng brand pack nháp trong `project/brand/`:
   - `brand.md`: định vị, voice (suy từ mô tả business), audience, mùa vụ
   - `facts.yaml`: số liệu/claim nêu trong Onboarding (mục chưa chắc → `verify:`)
   - `rules.yaml`: từ/claim cần tránh; chính tả theo thị trường chính
   - `glossary.csv`: tên brand/sản phẩm giữ nguyên
   - Đánh dấu rõ phần suy luận cần người xác nhận.
6. **Lập internal-links.csv**: nếu có tab Site URL hoặc sitemap, lấy URL thật; nếu chưa, để trống
   và ghi chú chạy `/site-inventory`.
7. **Báo cáo:** liệt kê ID đã map, phần brand pack còn thiếu, và bước tiếp theo (`/p01-onboarding`
   để hoàn thiện, hoặc `/p02-access`).

## TODO khi có quyền Editor Drive
- Copy cây folder + Plan/Masterfile/Onboarding từ "Drive Template" và đặt tên theo quy ước
  (`[YYYY] SEO/GEO Plan - <Client>`, folder tháng `YYYY-MM`).

## Ghi ra
`project/config.yaml`, `project/brand/*`, một dòng trong `project/decisions.md`.
Không gửi gì cho khách.

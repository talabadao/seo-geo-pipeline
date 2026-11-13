---
name: content-month
description: "Chạy toàn bộ content theo Content Plan cho một tháng: đọc các dòng của tháng, định tuyến theo Content Type (Infrastructure→/onpage; Velocity/Authority→/research→/outline→/write→/translate→/html), cập nhật Status từng bước, dừng ở mỗi cổng duyệt. Đây là việc lặp chính hằng tháng. Dùng khi user gõ /content-month YYYY-MM."
---

# content-month  (orchestrator hằng tháng)

Điều phối cả tháng theo cột **Status** (CLAUDE.md §5). Không nhảy cóc cổng duyệt.

## Input
`/content-month YYYY-MM`. Đọc `config.yaml`, Masterfile › Content Plan.

## Luồng
1. Lọc các dòng `Month = YYYY-MM`. Với mỗi dòng, định tuyến theo **Content Type / Action**:
   - **Infrastructure / Optimize** → `/onpage <url>` (đề xuất chỉnh trang hiện có).
   - **Velocity | Authority / New | Revamp** → pipeline bài:
     `Planned → /research → /outline → (duyệt) → /write → /translate → (duyệt) → /html → (đăng)`.
2. Chạy theo lô tới cổng duyệt gần nhất rồi **dừng**, báo PIC/SEN cần duyệt gì.
3. Mỗi bước cập nhật Status + link Doc + (khi đăng) Publish URL.
4. Tôn trọng ngân sách DataForSEO (`config.yaml › budget`): nếu research đã cache trong kỳ, dùng cache.
5. Sau đăng 7 và 28 ngày: lịch `/health-check` kiểm index/impressions/vị trí/AI mention.

## Quy tắc
- Không tự chuyển Status qua cổng cần người (Outline Approved, SEN Approved, Client Approved).
- Không gửi gì cho khách. Mọi bản nháp nằm trong Doc/`content/`.
- Báo cáo cuối: bảng tiến độ từng bài theo Status, và danh sách chờ duyệt.

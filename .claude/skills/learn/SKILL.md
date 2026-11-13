---
name: learn
description: "Ghi lại bài học từ feedback của khách hoặc SEN cho một dự án, để các bài sau không lặp lỗi. Đọc comment/sửa trên Doc hoặc Sheet, rút thành quy tắc ngắn, thêm vào project/brand/learned.md (và rules.yaml nếu là quy tắc cứng). Dùng khi user gõ /learn hoặc sau một vòng sửa của khách/SEN."
---

# learn  (vòng học theo dự án)

Biến feedback thành quy tắc dùng lại. Mọi skill content đọc `learned.md` trước khi viết.

## Input
`/learn` + nguồn feedback: comment trên Google Doc/Sheet, hoặc đoạn feedback user dán.

## Các bước
1. Đọc feedback (Doc comments qua connector, hoặc text user cung cấp).
2. Phân loại mỗi điểm:
   - **Quy tắc cứng** (từ cấm, chính tả, định dạng, cấm chủ đề) → thêm vào `project/brand/rules.yaml`
     (và nếu là từ cấm → `lint.banned_words` để content_lint bắt tự động).
   - **Ưu tiên giọng/cấu trúc/góc nhìn** → thêm dòng vào `project/brand/learned.md`.
   - **Dữ kiện sai/đổi** → cập nhật `project/brand/facts.yaml`.
3. Ghi `learned.md` theo format: ngày · nguồn · bài/ngữ cảnh · bài học · áp dụng từ nay.
4. Ghi một dòng vào `project/decisions.md`.
5. Báo PIC các thay đổi đã áp (và nếu thêm từ cấm, lint sẽ bắt từ bài kế tiếp).

## Nguyên tắc
Chỉ ghi quy tắc rút từ feedback thật của người; không tự nghĩ ra quy tắc. Không gửi gì cho khách.

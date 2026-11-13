# Khuôn Brand Guideline theo ngành

Dùng để tạo/chuẩn hóa brand guideline mỗi khách, rồi rút gọn thành brand pack
(`project/brand/*`) cho Claude viết bài. Một brand guideline B2B đầy đủ (ví dụ ngành sản xuất) là nguồn tốt để rút gọn.
Mỗi ngành có thể có khuôn riêng (hospitality vs b2b-manufacturing); phần lõi chung như dưới.

## 1. Brand Overview — brand là gì, định vị, tagline, lịch sử, sở hữu
## 2. Brand Identity
  - 2.1 Voice (3–6 tính từ giọng, kèm ví dụ câu từ website)
  - 2.2 Tone theo loại nội dung (bảng: loại trang → giọng)
  - 2.3 Positioning statement; 2.4 Differentiators; 2.5 Boilerplate (short/standard)
## 3. Target Audience — ICP, phân khúc, địa lý/ngôn ngữ, "không hợp với ai"
## 4. Products/Services & Commercial model — danh mục, điều khoản chuẩn (MOQ, lead time...)
## 5. Content Objectives — mục tiêu, content pillar, mục tiêu theo loại bài
## 6. Competitors — tham chiếu, quy tắc không nêu tên/so sánh
## 7. Content Rules
  - 7.1 Off-limit topics (giá, tên khách, guarantee, claim chưa chứng nhận, sustainability quá mức...)
  - 7.2 Required disclaimers (theo loại nội dung)
  - 7.3 Internal linking conventions (bảng topic → URL đích)
  - 7.4 SEO & quality standards (E-E-A-T, answer-first, verified facts)
  - 7.5 Language & style (ngôn ngữ, chính tả, tên công ty/sản phẩm, số, từ cấm → từ thay thế)
## 8. Channel notes — website, blog, social, email, profile PDF
## 9. Governance — ai duyệt gì; review định kỳ
## Phụ lục A — Approved Fact Sheet (giá trị đã duyệt + nguồn)  → thành facts.yaml
## Phụ lục B — Items to Resolve (⚠ Verify: mâu thuẫn/chưa chứng thực)  → facts.yaml mục verify
## Phụ lục C — Source pages reviewed

→ Rút gọn thành brand pack:
  §2 → brand.md · §3,§5 → brand.md/audience · §7.1,7.2,7.5 → rules.yaml · §7.3 → internal-links.csv
  · Phụ lục A → facts.yaml (approved) · Phụ lục B → facts.yaml (verify, bị chặn)

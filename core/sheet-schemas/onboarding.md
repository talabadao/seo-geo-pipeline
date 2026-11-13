# Schema — On-Boarding Questions (P01)

Sheet riêng, tên `<Client> | On-Boarding Questions`. 6 nhóm câu hỏi. Skill /p01-onboarding đọc
các câu trả lời (cột trả lời thường ở phải, có khi dùng TRUE/FALSE cho ô lựa chọn) rồi dựng brand pack.

Nhóm:
1. **Business Information** — tên, email, contact, URL, mô tả business, địa chỉ GMB, brand guideline link
2. **Business Model & Location** — target country/language, audience, top products, vấn đề khách giải
   quyết, sales cycle, cách kiếm tiền, đối thủ, USP, mùa vụ
3. **Goals & Success** — mục tiêu SEO, kỳ vọng 3–6 / 6–12 tháng, keyword local, keyword chính
4. **Direct Booking** — có report doanh thu direct không, cách track/attribute
5. **GEO Specific** — tác giả/chuyên gia, top 10 câu khách hỏi, vì sao đáng tin hơn đối thủ, kênh
   nội dung khác, có track AI traffic không, từ/claim cần tránh, ai duyệt thay đổi kỹ thuật
6. **Access to Online Analytics** — CMS, GBP, GA4, GSC... (TRUE/FALSE đã cấp quyền)

Mapping onboarding → brand pack:
- mô tả business, USP, audience, mùa vụ → `brand.md`
- số liệu/claim nêu ra → `facts.yaml` (mục chưa chắc → ⚠ Verify)
- từ/claim cần tránh → `rules.yaml`
- top 10 câu khách hỏi → gợi ý Problem Pattern + FAQ
- đối thủ → `config.yaml › competitors`
- target country/language → `config.yaml › languages, serp_locations`

# core/formats — khuôn từng dạng bài

Mỗi format mô tả: intent, khi nào dùng, cấu trúc H1/H2, độ dài, thành phần bắt buộc, ghi chú
GEO/answer-chunk, schema, pattern internal link, lỗi hay gặp. Skill `/outline` chọn format theo
cột **Content Type** + gợi ý ở **Topic//Note** trong Content Plan, rồi ghép với industry + market
+ brand (CLAUDE.md §6).

Chọn format (gợi ý theo tiêu đề trong Content Plan):
- "10+ / best / top ... hotels|restaurants|things" → velocity/toplist
- "things to do in ..." → velocity/things-to-do
- "how to get from A to B" → velocity/how-to-get-there
- "best time to visit ..." → velocity/best-time-to-visit
- "... weather" → velocity/weather
- "... food / what to eat / dish" → velocity/food-guide
- "<event> <year>" → velocity/event-festival
- "where to stay in / hotels near ..." → velocity/area-neighbourhood
- "<destination> travel guide / complete guide" → velocity/travel-guide
- "what is ..." → velocity/what-is
- "X vs Y" → velocity/comparison
- "which <model> fits / guide to choosing" → velocity/buyer-guide
- trang sản phẩm/dịch vụ/danh mục/địa điểm → infrastructure/*
- awards / reviews / case study / about → authority/*

Có thể chia sâu hơn cho ngành cụ thể trong `project/overrides/formats/`.

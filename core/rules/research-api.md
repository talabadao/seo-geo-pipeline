# Nguyên tắc Research & Phân tích đối thủ bằng API

Mục tiêu: research một lần, cache lại, dùng cho outline + write + translate. Ưu tiên connector MCP
hơn web search. Tôn trọng `config.yaml › budget.dataforseo_usd_per_month` (mặc định $5).

## Connector nào cho việc gì

| Việc | Connector (tool) | Khi nào |
| --- | --- | --- |
| Search volume, KD, CPC, related, long-tail | **DataForSEO** `api_request` → `keywords_data/google_ads/search_volume/live`, `dataforseo_labs/google/related_keywords/live` | Mọi keyword trước khi đưa vào Tracking/Content Plan |
| Keyword của đối thủ, keyword gap | **DataForSEO** `dataforseo_labs/google/ranked_keywords/live`, `.../domain_intersection/live` | Phân tích đối thủ (P03) |
| Backlink, ref domain, anchor, new/lost | **DataForSEO** `backlinks/*` | Backlink gap (Offsite) |
| SERP top 10, PAA, AI Overview | **SERP API** `search` (google, đúng location) | Mỗi bài — hiểu đang cạnh với ai + AI đang trích gì |
| Rank tracking, site audit, AI visibility/prompt | **SE Ranking** `PROJECT_*`, `DATA_*`, `SEV_*` | Theo dõi định kỳ, GEO visibility |
| Đọc nội dung trang đối thủ | **Firecrawl** `firecrawl_scrape` (markdown) | Lấy H1/H2/H3, góc, độ sâu, khoảng trống |
| Đọc nhiều trang/không rõ URL | **Firecrawl** `firecrawl_search` / `firecrawl_agent` | Khi cần quét rộng |

KHÔNG dùng web search của Claude cho SERP/volume — kém nhất quán và tốn hơn.

## Quy tắc tiết kiệm credit (bắt buộc)
1. **Cache mọi kết quả** vào `data/serp/<slug>.json`, `data/keywords/<slug>.json`,
   `data/serp/<slug>-competitors.json`. Trước khi gọi, kiểm cache trong kỳ.
2. **Gom batch:** hỏi volume nhiều keyword một lần thay vì từng cái.
3. **Giới hạn Firecrawl ở 5 URL đối thủ** đã lọc, không cào cả SERP.
4. Nếu một lần research sẽ vượt ngân sách tháng → dừng, báo PIC.

## Lọc đối thủ (trước khi đọc)
Từ top 10, chọn 5 đối thủ hợp hồ sơ site (cùng ngành/mô hình). Loại domain theo
`core/markets` + `core/industries`:
- **Hospitality:** GIỮ OTA trong research (đối thủ SERP thật), loại social/PR/bách khoa.
- **B2B:** loại marketplace (Alibaba, Made-in-China), social, bách khoa.
Ghi lý do loại mỗi URL vào research brief.

## Phân tích đối thủ (mỗi URL)
H1/H2/H3 theo thứ tự · góc & subtopic đã phủ · độ sâu (nông/vừa/sâu) · khoảng trống · claim nghi ngờ.
→ So sánh để tìm pattern (ai cũng có) và cơ hội khác biệt (chưa ai làm tốt).

## GEO trong research
Ghi: prompt nào (tab Tracking) bài cần trả lời · entity bắt buộc nêu · nguồn AI Overview đang trích
(để biết phải hơn ai) · dữ kiện brand (facts.yaml) có thể dùng để AI có lý do trích.

## Nguyên tắc dữ liệu
Chỉ dùng số từ connector, ghi rõ nguồn + ngày. Không suy diễn volume/vị trí. Số liệu ngành do team
cung cấp để trong `project/research/`, trích có tên nguồn + năm.

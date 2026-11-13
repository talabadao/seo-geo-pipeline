---
name: research
description: "Nghiên cứu trước khi lên outline cho một keyword/bài: lấy SERP top 10, PAA, AI Overview, đọc đối thủ phù hợp, lấy volume/KD/related từ DataForSEO, soát nguồn AI đang trích, và tổng hợp thành một research brief dùng lại được. Chạy trước /outline để tiết kiệm credit (research một lần, outline + write + translate dùng chung). Dùng khi user gõ /research hoặc bắt đầu một bài Velocity/Authority mới."
---

# research  (bước trước /outline)

Gom toàn bộ nghiên cứu cho một bài **một lần**, cache lại, để `/outline` và `/write` không phải gọi
API lặp. Tôn trọng `config.yaml › budget.dataforseo_usd_per_month` (mặc định $5) — nếu một keyword
đã có brief trong kỳ, đọc cache thay vì gọi lại.

## Input
`/research "<keyword>"` (hoặc một dòng ID trong Content Plan). Đọc `config.yaml` (locale,
serp_locations, competitors) và `project/brand/*` trước.

## Nguồn & thứ tự (ưu tiên connector, cache mọi kết quả)
1. **Intent & volume** — DataForSEO: volume, KD, CPC, related & long-tail, "people also ask".
   Cache `data/keywords/<slug>.json`. SE Ranking làm nguồn phụ.
2. **SERP** — SERP API: top 10 organic, PAA, **AI Overview** (ghi lại claim chính + nguồn AI trích).
   Cache `data/serp/<slug>.json`. KHÔNG dùng web search của Claude cho bước này.
3. **Lọc 5 đối thủ** hợp hồ sơ site (cùng ngành/mô hình). Loại domain theo `core/markets` +
   `core/industries` (hospitality: GIỮ OTA trong research; B2B: loại marketplace). Ghi lý do loại.
4. **Đọc đối thủ** — Firecrawl `firecrawl_scrape` 5 URL: lấy H1/H2/H3, góc đã phủ, độ sâu, khoảng
   trống, claim nghi ngờ. Cache `data/serp/<slug>-competitors.json`.
5. **GEO** — ghi: prompt nào trong tab Tracking bài này cần trả lời; nguồn nào AI Overview đang
   trích (để biết phải hơn ai); entity bắt buộc nêu.
6. **Brand hook** — từ `facts.yaml`/Problem Pattern: dữ kiện riêng của brand bài có thể dùng để AI
   có lý do trích; internal link ứng viên từ `internal-links.csv`.

## Output → `content/YYYY-MM/<slug>/research.md`
```
# Research — <keyword>
Locale/SERP location · Intent (Informational/Commercial/...) · Volume/KD
## SERP snapshot: top 10 (url + góc), PAA, AI Overview (claim + nguồn trích)
## Đối thủ phân tích (5): mỗi url — góc, độ sâu, khoảng trống
## Đối thủ đã loại: url — lý do
## Khác biệt hoá: bài này làm gì competitor không
## GEO: prompt cần trả lời · entity bắt buộc · nguồn AI đang trích
## Brand hook: dữ kiện facts.yaml dùng được · internal link ứng viên
## Cảnh báo: dữ kiện cần [VERIFY]/[NEED CLIENT CONFIRMATION]
```

Báo PIC: brief sẵn sàng cho `/outline`. Không gửi khách.

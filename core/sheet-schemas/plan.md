# Schema — SEO/GEO Plan (7 tab, chuẩn The Sukosol)

Cột "ngôn ngữ 2" đọc từ `config.yaml › languages.secondary`. Skill ghi đúng header này, không đổi.

## Tab 1 — Foundation  (P03, skill /p03-foundation)
Cột: `Category | Category Details | Description`
Các nhóm dòng (cột Category là nhãn nhóm, merge dọc):
- **Product/Services** — từng dòng một sản phẩm/dịch vụ + ghi chú doanh thu/đối tượng
- **Ideal Customer Profile(s) / ICP(s)** — từng phân khúc + mô tả hành vi
- **USP** — từng điểm khác biệt + diễn giải
- **Target location** — từng vùng + ngôn ngữ
- **Competitors** — từng đối thủ + vị thế
- **Targeted Category** — các Category Leader sẽ "sở hữu" (dùng ở tab Problem Pattern)

## Tab 2 — Problem Pattern  (P04a, skill /p04a-patterns)
Mỗi **Category Leader** là một khối, mở đầu bằng dòng tiêu đề
`Category Leader N - <tên> (<nhóm>)`. Trong khối, header 10 cột:
`Pattern | Trigger | Need | Constraints | Buying criteria | Objections | Proof | Prompts (track) | Keywords (track) | Content`

## Tab 3 — Tracking  (P04b, skill /p04b-tracking)
`Category | Keyword (En) | Keyword (<lang>) | Search volume | Type | Matched URL on Website | Prompts Tracking`
- Type ∈ {Page, Blog, Page/Blog}. Search volume lấy từ DataForSEO; dạng "1-10" cho volume rất thấp.
- Prompts Tracking: các câu hỏi AI cần theo dõi, gộp theo cụm Category.

## Tab 4 — Content Plan  (P04c, skill /p04c-content-plan)
`Month | Keywords//Pages | Volume | Topic//Note | Content Type | Action | Doc | Status | Publish URL (En) | Publish URL (<lang>)`
- Content Type ∈ {Infrastructure, Velocity, Authority}; Action ∈ {Optimize, New, Revamp}.
- Doc = link Google Doc; Status điều khiển vòng đời (CLAUDE.md §5); Publish URL điền khi đăng.

## Tab 5 — Technical Baseline  (P04d, skill /p04d-tech-baseline)
`Layer | Item | Status | Finding (evidence) | Action | Priority`
- Layer ∈ {ACCESS, LEGIBILITY, ENTITY, ARCHITECTURE, TAG TRACKING} (dòng nhãn layer in hoa).
- Status ∈ {Pass, Partial, Audit needed}. Finding phải có bằng chứng định lượng.
- Priority ∈ {High, Medium, Low}.

## Tab 6 — Offsite  (P04e, skill /p04e-offsite)
`Area | Details | Timeline`
Area ví dụ: Google Business Profile, GBP Posting Cadence, OTA Entity Audit, Local Partnerships,
Citations/Directories, Awards/Partnerships.

## Tab 7 — Measurement  (P04e, skill /forecast)
3 khối forecast, mỗi khối theo tháng (Jan..Dec):
- **Organic Traffic Forecast**, **AI Traffic Forecast**, **Booking Forecast**
- Dòng mỗi khối: `Actual - <năm>` · `Market trend` · `Ideal Growth` (2%) · `Goal` · `Stretch Goal`
- Công thức giữ nguyên: Market trend = round((tháng_này - tháng_trước)/tháng_trước, 2) trên năm
  trước; Goal = tháng_trước × (1 + Market trend); Stretch = × (1 + Market trend + 0.02).
- Claude CHỈ điền các dòng `Actual` từ Agency Analytics; không sửa công thức.

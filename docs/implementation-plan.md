# SEO/GEO Pipeline × Claude Code: Kế hoạch triển khai

**Phiên bản:** v0.2 (đã chốt 4 quyết định bên dưới, các câu còn lại ở Mục 13)
**Ngày:** 13/11/2026
**Phạm vi:** Template GitHub dùng chung cho quy trình SEO/GEO của Liam's Pod (P01–P07 + Handover), chạy bằng Claude Code, kết nối Google Drive/Sheets/Docs, Agency Analytics, SERP API, Firecrawl, DataforSEO và SE Ranking.

**Thay đổi so với v0.1:** đã đọc được 4 folder Drive mẫu, nên plan được viết lại theo format thật đang dùng:

- Chọn format Plan 7 tab của The Sukosol và I'Msignia làm chuẩn, vì các tab này khớp 1-1 với P03–P04e (Mục 2.2).
- Output của skill viết bài theo đúng format Content Doc hiện tại: `Draft_EN` / `Draft_TH`, bảng meta, danh sách xác nhận với khách (Mục 2.3).
- Forecast giữ đúng công thức của tab Measurement (Mục 2.5).
- Thêm các rủi ro mới phát hiện: quyền Drive chỉ ở mức xem, và mật khẩu CMS đang lưu dạng plain text trong Sheet (Mục 1).

**Phase 1 đã dựng (13/11/2026)** — xem `CLAUDE.md`, `core/`, `.claude/skills/`, `scripts/`:
backbone (CLAUDE.md + content rules + security), config schema + brand pack .example (khuôn), 7-tab
sheet-schemas, 22 format (12 velocity travel + 7 infrastructure + 3 authority), 2 playbook ngành,
markets, content_lint + secret_scan hook (đã test), 7 skill content (new-project, research, outline,
write, translate, content-month, learn) + 4 subagent, sync-core.sh. Brand pack để dạng .example (không chứa dữ liệu khách); dữ liệu CWG chỉ nằm trong repo dự án private.

**Đã chốt (13/11/2026):**

| # | Quyết định | Hệ quả |
| --- | --- | --- |
| A1 | Template repo + mỗi khách một repo private `seo-<client>` | Làm `sync-core.sh` ở Phase 1, chuyển sang plugin ở v2 |
| A2 | Chạy chủ yếu trên web/app claude.ai/code | Dùng connector của org, không cần cấu hình MCP trên từng máy. Health check hằng tuần dùng scheduled task. Mỗi phiên cần bật đủ connector, nên README sẽ có checklist bật connector |
| B2 | Giữ đúng format Plan 7 tab của The Sukosol | Schema trong repo bám đúng cột hiện có. Không thêm tab mới khi team chưa yêu cầu |
| E1 | Pilot kép: CWG (P01→P04) + The Sukosol (P05–P06) | Phase 2 thử content trên Sukosol, Phase 3 dựng Plan cho CWG |

---

## 0. Tóm tắt

1. **Kiến trúc 3 lớp.** Lớp Core (repo template này) chứa skill, agent, hook, format bài, playbook ngành và quy tắc thị trường, dùng chung cho mọi dự án. Mỗi khách hàng có một Client Repo tạo từ template, chứa brand, source website, content, audit và report. Google Drive là nơi team và khách làm việc hằng ngày.
2. **Chuẩn hóa theo format mới nhất.** SEO/GEO Plan gồm 7 tab: Foundation → Problem Pattern → Tracking → Content Plan → Technical Baseline → Offsite → Measurement. Masterfile là bản sao của Plan, thêm các tab SEO Assets, GBP Posts và Site URL. Drive template và schema trong repo đều dựng theo format này.
3. **Mỗi bước P01–P07 ứng với một skill gọi bằng `/lệnh`.** Skill ghi kết quả vào đúng tab hoặc đúng folder. Luồng duyệt là PIC chạy → SEN duyệt → AM/PM gửi khách. Claude không bao giờ gửi thẳng cho khách.
4. **Content engine ghép theo lớp:** Core + Content Type (Infrastructure / Velocity / Authority) + format bài + playbook ngành + quy tắc thị trường + brand pack. Output là Google Doc theo đúng format team đang dùng.
5. **Mọi con số do script hoặc công thức Sheet tính, Claude chỉ diễn giải.** Forecast giữ công thức hiện có, Claude điền số Actual lấy từ Agency Analytics.
6. **Pilot kép (đề xuất):** CWG chạy P01→P04 như một dự án mới. The Sukosol thử phần content hằng tháng và báo cáo (P05–P06) trên một dự án đang chạy.

---

## 1. Hiện trạng đã kiểm tra (13/11/2026)

| Hạng mục | Trạng thái | Ghi chú |
| --- | --- | --- |
| Repo `talabadao/seo-geo-pipeline` | Chỉ có file plan này | Branch làm việc: `claude/seo-geo-template-setup-42iuoh` |
| Google Drive / Sheets / Docs connector | **Hoạt động đủ**: tìm, đọc, tạo, copy file, ghi Sheet và Doc | Đã đọc được cả 4 folder mẫu |
| Quyền trên 4 folder mẫu | **Chỉ xem** (`canEdit = false`) | Claude đọc được nhưng chưa ghi được. Folder dự án mới cần cấp quyền Editor cho tài khoản chạy Claude (câu hỏi B1) |
| Connector đã kết nối ở org nhưng **chưa bật trong phiên này** | AgencyAnalytics, Firecrawl, SE Ranking, SEO Data, SERP API (cùng Canva, Supabase, Vercel) | Cần bật trong cài đặt connector trước khi thử Phase 0 |
| Chưa có connector | Figma và Asana (có trong danh mục, chưa cài), Google Tag Manager (không có connector) | Cách làm thay ở Mục 9 |
| Skill `seo-outline`, `seo-article-writer` | Đã đọc | Đánh giá chi tiết ở Mục 7.4 |
| Brand Guideline CWG | Đã đọc | Dùng làm mẫu "brand pack": có fact sheet đã duyệt (Phụ lục A) và danh sách mục cần xác minh (Phụ lục B) |
| Skill có sẵn của org | category-definer, problem-pattern-identifier, geo-infra-audit, geo-visibility-report, llms-txt-builder, keyword-list-proposal, business-research-proposal, ai-content-writer, ai-writing-tells, natural-english-writing, natural-vietnamese-writing, translate-html, bhaya-translate-html, local-area-researcher, pr-writer | `category-definer` sinh ra tab Foundation, `problem-pattern-identifier` sinh ra tab Problem Pattern, nên tái sử dụng |
| ⚠ **Bảo mật** | Tab **SEO Assets** của Masterfile The Sukosol có lưu **mật khẩu CMS dạng plain text** | Nên chuyển sang trình quản lý mật khẩu và đổi mật khẩu đó. Template sẽ cấm Claude đọc hoặc chép cột này (Mục 11) |

---

## 2. Những gì học được từ 4 dự án mẫu

### 2.1 So sánh cấu trúc

| Dự án | Ngành | Thời điểm | Plan | Masterfile | Folder |
| --- | --- | --- | --- | --- | --- |
| Ad-Lib Hotels | Chuỗi khách sạn | 03/2026 | Không có Plan riêng | 11 tab, format cũ: Access & Tracking Setup, Business & Campaign Overview, Execution Roadmap, Content Plan, GEO Optimisation, Performance Forecast… | Content/<tháng>, Research, Off-page, Audit |
| Bhaya Cruises | Du thuyền | 10/2025 | "SEO Plan – Client Approval and Follow-Up" | 17 tab, format cũ: SEO Process, Traffic Forecast, Keyword List, GEO, Current Blog Auditing, Topic Content Proposal, Page optimisation, Data…, kèm vài tab "SheetXX" chưa đặt tên | Technical, Link Building, Content Creation, Page Optimisation, Others |
| **The Sukosol** | Khách sạn 5 sao, Bangkok | 10–11/2026 | **7 tab chuẩn mới** | Plan + SEO Assets + GBP Posts | SEO/GEO/{Content/11-26, Website Audit, Offsite} |
| **I'Msignia** | Resort | 10–11/2026 | **7 tab chuẩn mới** | Plan + SEO Asset + Site URL | Content/Nov_26, Website Audit, Offsite, GA4 Leads Tracking |

**Kết luận:** Sukosol và I'Msignia đã dùng chung một format, và format này khớp với sơ đồ pipeline, nên được chọn làm chuẩn cho template. Ad-Lib và Bhaya là format cũ (câu hỏi B3). Cả 4 dự án đều thuộc ngành lưu trú, còn CWG là B2B sản xuất. Vì vậy hai playbook ngành cần làm trước là **hospitality** và **b2b-manufacturing**.

Tên file và folder hiện chưa thống nhất: có nơi ghi `SEO//GEO Plan`, có nơi ghi `[2026] SEO/GEO Plan`, folder tháng có nơi đặt `11/26`, có nơi `Nov_26`. Template sẽ cố định quy ước đặt tên (Mục 5).

### 2.2 Map tab ↔ bước pipeline ↔ skill

| Tab (file) | Bước | Cột chuẩn | Skill tạo / cập nhật |
| --- | --- | --- | --- |
| *Onboarding Questions* (Sheet riêng) | P01 | 6 nhóm câu hỏi: Business Information · Business Model & Location · Goals & Success · Direct Booking · GEO Specific · Access to Online Analytics | `/p01-onboarding` |
| **SEO Assets** (Masterfile) | P02 | No · Assessment · Detail · Status · Related info | `/p02-access` |
| **Foundation** | P03 | Category · Category Details · Description. Các nhóm dòng: Product/Services, ICP(s), USP, Target location, Competitors, Targeted Category | `/p03-foundation` (dùng lại `category-definer`) |
| **Problem Pattern** | P04a | Mỗi khối là một *Category Leader*, gồm các cột Pattern · Trigger · Need · Constraints · Buying criteria · Objections · Proof · Prompts (track) · Keywords (track) · Content | `/p04a-patterns` (dùng lại `problem-pattern-identifier`) |
| **Tracking** | P04b | Category · Keyword (EN) · Keyword (ngôn ngữ 2) · Search volume · Type (Page/Blog) · Matched URL · Prompts Tracking | `/p04b-tracking` |
| **Content Plan** | P04c | Month · Keywords//Pages · Volume · Topic//Note · Content Type · Action · Doc · Status · Publish URL (EN) · Publish URL (ngôn ngữ 2) | `/p04c-content-plan` |
| **Technical Baseline** | P04d | Layer (Access / Legibility / Entity / Architecture / Tag tracking) · Item · Status (Pass / Partial / Audit needed) · Finding (evidence) · Action · Priority | `/p04d-tech-baseline` |
| **Offsite** | P04e | Area · Details · Timeline | `/p04e-offsite` |
| **Measurement** | P04e | 3 khối forecast: Organic Traffic, AI Traffic, Booking | `/forecast` |
| **GBP Posts** (Masterfile) | P05 | Month · Page/Blog · Doc · Status | `/gbp-posts` |
| **Site URL** (Masterfile) | P05 | Danh sách URL của site | `/site-inventory` |

Cột "ngôn ngữ 2" khác nhau theo dự án (Sukosol là Thai). Schema trong repo sẽ đọc ngôn ngữ từ `config.yaml` thay vì viết cứng.

### 2.3 Format Content Doc hiện tại (giữ làm chuẩn output)

Ví dụ: Doc "things to do in bangkok" trong Sukosol/Content/11-26.

- Mỗi bài là một Google Doc, đặt tên theo keyword chính, nằm trong folder tháng.
- Phần `Draft_EN` gồm:
  - bảng meta: URL (hoặc URL revamp), SEO title, Meta description
  - H1 → thân bài (có bảng, list, link ngoài tới nguồn chính thức) → Conclusion có CTA → FAQ
  - **Review appendix "Client Confirmation List"**, xóa trước khi đăng
- Phần `Draft_TH` (ngôn ngữ thứ 2) nằm ngay bên dưới.
- Trong bài dùng 2 loại tag:
  - `[NEED CLIENT CONFIRMATION: nội dung | nguồn]`: dữ kiện cần khách xác nhận
  - `[VERIFY: …]`: dữ kiện team cần tự kiểm tra

→ Skill viết bài sẽ xuất đúng format này, không dùng file `.md` + YAML như skill gốc. Hai loại tag trên được gắn tự động khi một dữ kiện không có trong `facts.yaml` (Mục 7.4).

### 2.4 Phân loại content theo GEO OS

- **Content Type:**
  - **Infrastructure:** trang "tiền" như home, room, dining, meeting, service, product
  - **Velocity:** bài blog hoặc guide để lấy traffic và trả lời prompt
  - **Authority:** trang bằng chứng như awards, reviews, case study, about
- **Action:** Optimize / New / Revamp.
- Thư viện format trong repo sẽ tổ chức theo 3 Content Type này (Mục 4).

### 2.5 Forecast hiện tại (tab Measurement)

- Có 3 khối: **Organic Traffic**, **AI Traffic**, **Booking**.
- Các dòng trong mỗi khối:
  - `Actual – <năm>`: số thực tế theo tháng
  - `Market trend`: % thay đổi so với tháng trước, tính trên năm trước, ví dụ `=round((E3-D3)/D3,2)`. Một số ô được nhập tay
  - `Ideal Growth`: 2%
  - `Goal`: tháng trước × (1 + Market trend)
  - `Stretch Goal`: tháng trước × (1 + Market trend + 2%)
- **Cách làm trong template:** giữ nguyên công thức trong Sheet, vì team đã quen và khách đã thấy. Claude chỉ điền các dòng Actual từ Agency Analytics và viết phần diễn giải.
- Ở v2 có thể thêm một forecast bottom-up dựa trên Content Plan (volume × CTR theo vị trí × ramp-up) làm số tham chiếu (Mục 8.2).
- Cần chốt nguồn số liệu cho từng khối (câu hỏi C2).

### 2.6 Technical audit hiện tại

- **Plan › Technical Baseline:** tóm tắt theo 5 layer, mỗi dòng có bằng chứng cụ thể, ví dụ "251 of 496 sitemap URLs redirect…", "LCP 5.9 s".
- **Sheet Website Audit riêng** có các tab dạng export crawl: URL, Website Structure, Content Audit, Noindex, Canonical, 301, 404, URL /tag/, Multiple-H1, Missing H1, Page Title Duplicate, Non-canonical, Image.
- **Các file phát sinh:** Website Fix List, Schema Markup (Doc), Website Translation Fix, Rank Math Switching, GA4 Leads Tracking.
- Template sẽ có skill riêng cho từng loại file này (Mục 9).

---

## 3. Kiến trúc tổng thể

```
┌──────────────────────────────────────────────────────────────────────┐
│  CORE (repo này: seo-geo-pipeline, bật "Template repository")        │
│  .claude/skills · .claude/agents · hooks · core/ · scripts/          │
└───────────────┬──────────────────────────────────────────────────────┘
                │ "Use this template" khi có dự án mới
                │ scripts/sync-core.sh để kéo bản cập nhật sau này
┌───────────────▼──────────────────────────────────────────────────────┐
│  CLIENT REPO  (talabadao/seo-<client-slug>, private)                 │
│  project/config.yaml · project/brand/* · website/ (source)           │
│  content/ · audits/ · reports/ · data/                               │
└───────┬─────────────────────┬─────────────────────┬──────────────────┘
        │ Claude Code         │                     │
┌───────▼───────┐   ┌─────────▼─────────┐  ┌────────▼─────────────────┐
│ Google Drive  │   │ Data connectors   │  │ Website (live + source)  │
│ Onboarding,   │   │ Agency Analytics  │  │ Firecrawl · Playwright   │
│ Plan,         │   │ DataforSEO        │  │ PageSpeed/Lighthouse     │
│ Masterfile,   │   │ SERP API          │  │ GTM container JSON       │
│ Content Docs  │   │ SE Ranking        │  │ Figma (khi có connector) │
└───────────────┘   └───────────────────┘  └──────────────────────────┘
```

### 3.1 Chiến lược repo

- `seo-geo-pipeline` là **template repo**. Mỗi dự án mới được tạo bằng "Use this template" thành `talabadao/seo-<client-slug>` ở chế độ private (câu hỏi A1).
- **Vấn đề:** GitHub không tự đẩy thay đổi của template xuống các repo đã tạo.
  - **v1:** `scripts/sync-core.sh` kéo `.claude/`, `core/` và `scripts/` từ template về repo dự án. Script không đụng vào `project/`, `website/`, `content/`, `audits/`, `reports/`.
  - **v2:** khi skill đã ổn định, đóng gói Core thành Claude Code plugin marketplace. Cập nhật một lần là mọi dự án đều nhận.
- **Ranh giới:** không sửa `core/` và `.claude/` trong repo dự án. Phần tùy biến riêng đặt trong `project/overrides/`.

### 3.2 Nơi lưu chính cho từng loại dữ liệu

| Dữ liệu | Nơi lưu chính | Cách Claude dùng |
| --- | --- | --- |
| Onboarding, Plan, Masterfile, trạng thái content | Google Sheets | Đọc/ghi qua connector. Cột `Status` của Content Plan điều khiển luồng làm việc |
| Outline, bản nháp, HTML | Git (`content/`) → Google Doc theo format 2.3 | Viết trong repo, chạy lint, rồi đẩy sang Doc. Khi khách comment trên Doc thì đọc ngược lại |
| Brand, fact sheet, quy tắc | Git (`project/brand/`), bản gốc trên Drive | Claude đọc từ repo vì có version và diff được |
| Source website | Git (`website/` hoặc submodule) | Audit code, đề xuất patch hoặc mở PR |
| Dữ liệu analytics, keyword, SERP | Connector → snapshot ở `data/` | Cache để không gọi API lặp lại và để so sánh các kỳ |
| Audit, báo cáo | Git (`audits/`, `reports/`) → Sheets/Docs để giao | |

---

## 4. Cấu trúc repo (template)

```
seo-geo-pipeline/
├── CLAUDE.md                     # "Luật vận hành": pipeline, vai trò, cổng duyệt, quy tắc chung
├── README.md                     # Hướng dẫn tạo dự án mới trong 30 phút
├── .claude/
│   ├── settings.json             # permissions, hooks (content-lint, secret-scan)
│   ├── skills/                   # mỗi skill = 1 thư mục SKILL.md (+ references/, scripts/)
│   └── agents/                   # subagent chuyên trách (3.3)
├── core/
│   ├── content-types/            # infrastructure.md, velocity.md, authority.md
│   ├── formats/
│   │   ├── velocity/             # where-to-stay listicle, area/local guide, things-to-do,
│   │   │                         # event/festival guide, how-to-get-there, best-time-to-visit,
│   │   │                         # buyer guide, explainer, comparison
│   │   ├── infrastructure/       # homepage, room/product, service, meeting/wedding venue,
│   │   │                         # location hub, dining outlet, category page
│   │   └── authority/            # awards & reviews, case study, about/heritage, team/author
│   ├── industries/               # hospitality.md, b2b-manufacturing.md (làm trước), ...
│   ├── markets/                  # en.md (biến thể GB/US/AU), th-TH.md, vi-VN.md, ko-KR.md, ...
│   │                             # chính tả, giọng địa phương, SERP location, domain loại trừ
│   ├── doc-templates/            # content-doc (Draft_EN/Draft_XX + Client Confirmation List)
│   ├── html-templates/           # component blog: TOC, key takeaways, bảng, FAQ, CTA, author box
│   ├── sheet-schemas/            # onboarding.yaml, plan.yaml, masterfile.yaml, website-audit.yaml
│   └── checklists/               # P02 access, P04d technical baseline, QA content
├── scripts/                      # Python: content_lint.py, crawl.py, analytics_snapshot.py,
│                                 # forecast.py, gtm_build.py, validate_project.py, sync-core.sh
├── project/                      # ← PHẦN RIÊNG CỦA DỰ ÁN (điền sau khi clone)
│   ├── config.yaml
│   ├── brand/
│   │   ├── brand.md              # voice, tone theo loại nội dung, định vị, audience
│   │   ├── facts.yaml            # số liệu đã duyệt + mục "⚠ verify" (bị chặn khi viết)
│   │   ├── rules.yaml            # chủ đề cấm, từ cấm và từ thay thế, disclaimer, quy ước tên
│   │   ├── internal-links.csv    # URL thật của site (crawl sitemap) + chủ đề + anchor gợi ý
│   │   ├── glossary.csv          # thuật ngữ không dịch / dịch cố định theo ngôn ngữ
│   │   └── source/               # bản gốc: brand guideline, onboarding export
│   ├── research/                 # dữ liệu ngành do team cung cấp
│   ├── overrides/                # format hoặc rule riêng của dự án
│   └── decisions.md              # nhật ký feedback và quyết định của khách
├── website/                      # source website (hoặc git submodule)
├── content/YYYY-MM/<slug>/       # brief.md, outline.md, draft.md, draft.html, translations/
├── audits/                       # technical/, uiux/, geo/, tracking/
├── reports/                      # weekly/, monthly/, executive/
└── data/                         # snapshot analytics/keyword/SERP (file lớn đưa vào .gitignore)
```

### 4.1 `project/config.yaml` (ví dụ với CWG)

```yaml
project:
  name: Capital World Group
  slug: cwg
  domain: capitalworldgroup.com
  industry: b2b-manufacturing        # → core/industries/b2b-manufacturing.md
  business_model: leadgen            # leadgen | booking | ecommerce | local
  cms: wordpress
  stage: P01                         # bước hiện tại trong pipeline
  team: { am_pm: "", pic: "", sen: "" }
languages:
  primary: en-GB                     # → core/markets/en.md (CWG dùng chính tả Anh)
  secondary: []                      # ví dụ Sukosol: [th-TH] → cột "Keyword (Th)", "Draft_TH"
serp_locations: [United States, Italy, Brazil]
drive:                               # Claude điền tự động khi chạy /new-project
  root_folder_id: ""
  onboarding_sheet_id: ""
  plan_sheet_id: ""
  masterfile_sheet_id: ""
  content_folder_id: ""
  website_audit_folder_id: ""
  offsite_folder_id: ""
  uiux_folder_id: ""
analytics:
  agency_analytics_campaign_id: ""
  gsc_property: "sc-domain:capitalworldgroup.com"
  ga4_property_id: ""
  gtm_container_id: ""
  conversion_events: [generate_lead, file_download]   # dùng cho khối "Booking/Leads" trong Measurement
  ai_referrers: [chatgpt.com, perplexity.ai, gemini.google.com, copilot.microsoft.com, claude.ai]
  page_groups:                       # dùng cho bộ lọc báo cáo
    insights: "^/(what-is|oem-vs|custom-garment|vietnam-)"
    products: "^/products/"
  branded_regex: "capital world|cwg|kiara garment|hp vina"
competitors: []                      # domain ưu tiên phân tích (lấy từ Foundation)
content:
  word_range: [1000, 1800]
  min_internal_links: 2
  cta_options: ["Contact our team", "Download our company profile"]
budget:
  dataforseo_usd_per_month: 30       # giới hạn chi phí API mỗi dự án
```

### 4.2 Subagent

| Agent | Nhiệm vụ | Lý do tách riêng |
| --- | --- | --- |
| `serp-researcher` | Lấy top 10, PAA, AI Overview, đọc 5 trang đối thủ | Nhiều dữ liệu thô, không nên làm đầy ngữ cảnh chính |
| `competitor-analyst` | Phân tích domain đối thủ, keyword gap, backlink gap | Chạy song song cho nhiều đối thủ |
| `content-reviewer` | Đóng vai SEN, chấm bài theo checklist trước khi chuyển người duyệt | Góc nhìn độc lập với người viết |
| `tech-auditor` | Đọc source và kết quả crawl, phân loại lỗi theo 5 layer | Source website rất lớn |

---

## 5. Cấu trúc Google Drive chuẩn và cách tạo tự động

### 5.1 Cây folder (dựa trên Sukosol/I'Msignia, bổ sung UI-UX, Tracking, Reports)

```
<Client>/
├── <Client> | On-Boarding Questions          (Sheet – P01)
├── Brand/                                     brand guideline, logo, tài liệu khách gửi
└── SEO-GEO/
    ├── [YYYY] SEO/GEO Plan - <Client>         (Sheet, 7 tab – gửi khách đầu tiên)
    ├── [YYYY] SEO/GEO Masterfile - <Client>   (Sheet = Plan + SEO Assets + GBP Posts + Site URL)
    ├── Content/
    │   └── YYYY-MM/                           1 Doc/bài: Draft_EN + Draft_<lang>
    ├── Website Audit/                         Website Audit, Fix List, Schema Markup, Translation Fix…
    ├── Tracking/                              Tracking Plan (GTM/GA4), GA4 Leads Tracking
    ├── UI-UX/                                 link Figma + báo cáo audit + đề xuất chỉnh sửa
    ├── Offsite/                               backlink plan, outreach content, GBP post content, citation
    ├── Reports/                               monthly, executive
    └── Research/                              dữ liệu ngành, đối thủ, export DataforSEO
```

Quy ước đặt tên: folder tháng dùng `YYYY-MM`, file dùng tiền tố `[YYYY]` và dấu `/` đơn. Lý do: sắp xếp đúng thứ tự và tìm kiếm dễ.

### 5.2 Tạo dự án mới tự động (`/new-project`)

1. Team dựng một lần **"Drive Template"**: copy Plan, Masterfile và Onboarding của Sukosol rồi xóa dữ liệu, chỉ giữ header, công thức, định dạng và data validation.
2. Khi chạy `/new-project <tên khách> <domain>`, Claude:
   - tạo cây folder
   - copy 3 Sheet mẫu và đặt tên theo quy ước
   - ghi toàn bộ ID vào `project/config.yaml`
   - điền sẵn domain và tên khách vào Onboarding
3. **Điều kiện:** tài khoản kết nối Drive phải có quyền Editor trên folder gốc chứa các dự án, tốt nhất là một Shared Drive của team (câu hỏi B1).

---

## 6. Map pipeline → skill

| Bước | Skill / lệnh | Người chạy → Người duyệt | Input | Output (ghi vào đâu) | Cổng duyệt |
| --- | --- | --- | --- | --- | --- |
| **Handover** | `/handover` | PIC mới | Plan, Masterfile, Onboarding, lịch sử repo | Brief tóm tắt, rủi ro, câu hỏi cho buổi catch-up với PIC cũ + AM/PM | — |
| **P01** Onboarding | `/new-project`, `/p01-onboarding` | AM/PM + PIC | Onboarding Questions, brand guideline | `config.yaml`, brand pack (`brand.md`, `facts.yaml`, `rules.yaml`), danh sách câu trả lời còn thiếu gửi AM/PM | AM/PM xác nhận form đủ |
| **P02** Access & Tracking | `/p02-access` | PIC → AM/PM + PIC | config, live site | Tab **SEO Assets** (chỉ ghi TRUE/FALSE, không ghi mật khẩu) + quét HTML tìm GA4/GTM ID + đối chiếu Agency Analytics. Mục thiếu được gắn cờ | Đủ quyền truy cập |
| **P03** Research & Strategy | `/p03-foundation`, `/p03-market` | PIC → PIC | Onboarding, đối thủ, dữ liệu ngành | Tab **Foundation** + báo cáo thị trường/đối thủ trong Research/ (DataforSEO, SERP API, Firecrawl) | — |
| **P04a** Problem Patterns | `/p04a-patterns` | PIC | Foundation + GSC queries | Tab **Problem Pattern** theo từng Category Leader | |
| **P04b** Keywords & Prompts | `/p04b-tracking` | PIC | Problem Pattern | Tab **Tracking**: keyword (2 ngôn ngữ), volume, Type, Matched URL, bộ prompt | |
| **P04c** Content Plan | `/p04c-content-plan` | PIC | P04a–b + Technical Baseline | Tab **Content Plan** ≥ 6 tháng: Infrastructure (optimize) + Velocity/Authority (new/revamp) | |
| **P04d** Technical | `/p04d-tech-baseline` | PIC | Crawl + source + PSI | Tab **Technical Baseline** (5 layer) + Sheet Website Audit | |
| **P04e** Complete Plan | `/p04e-offsite`, `/forecast`, `/p04e-review` | PIC → **SEN** | P04a–d + Agency Analytics | Tab **Offsite**, tab **Measurement**, checklist tự kiểm toàn bộ Plan | **SEN duyệt** → AM/PM gửi khách |
| P04 vòng sửa | `/p04-revise` | PIC | Comment của khách trên Sheet | Bản sửa + ghi `decisions.md` | Lặp đến khi khách duyệt |
| P04 → P05 | `/p04-to-masterfile` | PIC | Plan đã duyệt | Đồng bộ Plan sang Masterfile | |
| **P05** Technical SEO | `/tech-audit`, `/tech-fix` | PIC → SEN | Source + crawl | Website Audit, Fix List, Schema Markup doc + patch/PR cho dev | SEN |
| **P05** Content SEO | `/content-month`, `/outline`, `/write`, `/html`, `/translate` | PIC → SEN | Content Plan | Doc theo format 2.3, cập nhật Status/Doc/URL trong Content Plan | SEN, sau đó khách |
| **P05** On-page SEO | `/onpage <url>` | PIC | Dòng Infrastructure trong Content Plan | Title/meta/H1/heading/schema/internal link đề xuất | |
| **P05** Off-page/Local | `/offpage-plan`, `/gbp-posts` | PIC | Offsite, backlink đối thủ (DataforSEO) | Prospect list, outreach template, nội dung GBP theo tháng → tab **GBP Posts** | |
| **P05** Analytics/GEO | `/gtm-plan`, `/gtm-build`, `/gtm-verify`, `/llms-txt` | PIC → SEN | Source + live site | Tracking Plan, file container GTM để import, kết quả kiểm tra, llms.txt | SEN trước khi publish container |
| **P06a** Health Check | `/health-check` (tự chạy hằng tuần) | PIC → SEN | Agency Analytics + crawl mẫu | Báo cáo tuần + cảnh báo, cập nhật Asana nếu có connector (câu hỏi A3) | |
| **P06b/c** Reports | `/report monthly`, `/report executive` | PIC → SEN | Agency Analytics, Masterfile | Báo cáo tháng / báo cáo cho lãnh đạo khách trong Reports/ | SEN |
| **P06d** Client Meeting | `/meeting-prep`, `/meeting-notes` | AM/PM + PIC | Báo cáo, ghi chú họp | Agenda, action item ghi vào Masterfile | |
| **P06** SEO Diagnosis | `/diagnose <url/nhóm trang>` | PIC | Analytics, index, SERP | Đi theo cây Path 1/2/3 trong sơ đồ (Mục 10.4) | |
| **P06e/f** GEO | `/geo-visibility`, `/geo-gap`, `/geo-fix-mentions` | PIC | Prompts trong Tracking, câu trả lời của AI | Gap so với đối thủ → content bổ sung. Mention sai → tìm nguồn → sửa thông tin trên site | |
| **P07a** CRO | `/cro-audit` | PIC → SEN | GA4 funnel + screenshot | Đề xuất tối ưu booking/lead | |
| **P07b** AI Conversion | `/geo-expand` | PIC | P06e/f | Mở rộng prompt, tối ưu trang được AI trích dẫn | |
| **UI/UX** | `/uiux-audit` | PIC/Designer | Screenshot desktop/mobile (+ Figma nếu có) | Báo cáo có chú thích trong UI-UX/ (Mục 9.4) | |

**Quy tắc chung trong CLAUDE.md:** mỗi skill khi chạy xong phải:

1. ghi output vào repo
2. cập nhật ô tương ứng trong Sheet (Status, Doc, URL)
3. ghi một dòng vào `decisions.md` hoặc change log
4. báo PIC biết bước tiếp theo cần ai duyệt

Nếu thiếu input, skill dừng lại và liệt kê những gì cần AM/PM bổ sung, đúng như ghi chú "return to P01 and contact AM/PM" trong sơ đồ.

---

## 7. Hệ thống content (việc chính hằng tháng)

### 7.1 Ghép skill theo lớp

```
seo-outline / seo-article-writer   (quy trình chung, đã nâng cấp)
   + core/content-types/<type>.md   Infrastructure / Velocity / Authority: mục tiêu, CTA, mức độ bán hàng
   + core/formats/<type>/<format>.md  cấu trúc, độ dài, thành phần bắt buộc, schema
   + core/industries/<ngành>.md     E-E-A-T, thuật ngữ, góc nhìn người mua, YMYL, domain loại trừ
   + core/markets/<locale>.md       chính tả, giọng địa phương, SERP location
   + project/brand/*                voice, facts, rules, internal links, disclaimer
   + project/overrides/*            ngoại lệ riêng của dự án
```

Thứ tự ưu tiên khi các lớp mâu thuẫn: **brand > overrides > format > content type > industry > market > core**. Mỗi lần phải áp dụng thứ tự này, skill ghi lý do vào handoff note.

### 7.2 Vòng content hằng tháng (điều khiển bằng cột Status)

```
/content-month 2026-12
  1. Đọc Masterfile › Content Plan: các dòng Month = Dec 2026
  2. Dòng Infrastructure / Optimize → /onpage: đề xuất chỉnh trang hiện có
     Dòng Velocity hoặc Authority / New, Revamp → /outline → /write
  3. /outline: SERP + đối thủ + Problem Pattern + prompt → content/2026-12/<slug>/outline.md
              → Doc "<keyword>" trong Content/2026-12 → Status = Outline Ready
  4. PIC/SEN duyệt trên Doc → Status = Outline Approved
  5. /write: đọc comment → draft → content-lint → content-reviewer
              → ghi Draft_EN vào Doc (bảng meta + bài + Client Confirmation List)
              → /translate → Draft_<lang> → Status = Draft Ready
  6. SEN duyệt → khách duyệt (xác nhận các tag NEED CLIENT CONFIRMATION)
              → /html → đăng → điền Publish URL → Status = Published
  7. Sau 7 và 28 ngày: /health-check kiểm tra index, impressions, vị trí, AI mention
```

Status đề xuất: `Planned → Outline Ready → Outline Approved → Draft Ready → SEN Approved → Client Approved → Published → Monitoring`. Hiện Sheet mới chỉ dùng `Draft`, nên danh sách này cần chốt (câu hỏi E3).

### 7.3 Ví dụ format Velocity rút ra từ Content Plan của Sukosol

| Mẫu tiêu đề | Format | Thành phần bắt buộc |
| --- | --- | --- |
| "10+ Hotels Near CentralWorld Bangkok: Where to Stay…" | Listicle where-to-stay | Bảng so sánh, tiêu chí chọn, đặt khách sạn của khách ở vị trí có lý do rõ ràng (không tự xếp hạng 1) |
| "Vijit Chao Phraya 2026: Dates, Fireworks & Where to Stay" | Event guide | Ngày/giờ có nguồn chính thức, cách đi, nơi ở gần, `[VERIFY]` cho mọi mốc thời gian |
| "How to Get From Bangkok to Phuket: Flights, Bus & Train Compared" | How-to-get-there | Bảng so sánh thời gian/chi phí, nguồn chính thức |
| "Things to Do in Bangkok…" | Area / things-to-do guide | Bảng theo khoảng cách từ khách sạn, lịch trình mẫu theo ICP, FAQ |
| "Best Time to Visit Bangkok: Weather & Festival Guide" | Seasonal guide | Bảng theo tháng, mùa cao/thấp điểm lấy từ Onboarding |

### 7.4 Nâng cấp 2 skill hiện có

**`seo-outline`**

1. Skill đang đọc brand từ "Claude Project". Cần đổi sang đọc `project/brand/*`, `config.yaml` và dòng tương ứng trong Content Plan.
2. Danh sách domain bị loại khi phân tích đối thủ (báo VN, OTA, sàn TMĐT) đang viết cứng. Danh sách này phải đổi theo ngành:
   - Với khách sạn, OTA thường là đối thủ thật trên SERP. Ít nhất cần ghi nhận OTA vào research thay vì loại bỏ hoàn toàn.
   - Với B2B như CWG, cần loại các marketplace như Alibaba.
   - Danh sách sẽ chuyển vào `core/industries/` và `core/markets/`.
3. Độ dài cố định 1,200–1,500 từ cần thay bằng độ dài theo format và brand. Ví dụ CWG: buyer guide 1,000–1,800 từ, news 150–300 từ.
4. Năm "2026–2027" đang viết cứng. Nên tính theo ngày chạy.
5. Cần nối outline với Plan: lấy Problem Pattern (Trigger, Need, Objections, Proof), prompt trong tab Tracking và volume/KD từ DataforSEO.
6. **Bổ sung phần GEO:**
   - mỗi H2 có một câu trả lời trực tiếp (answer chunk)
   - danh sách entity bắt buộc phải nêu
   - dữ kiện riêng của brand lấy từ `facts.yaml` hoặc cột Proof, để AI có lý do trích dẫn
   - các prompt mà bài cần trả lời
   - các nguồn đang được AI Overview trích dẫn
7. Output cần ghi ra file, đẩy sang Doc và cập nhật Status trong Sheet, thay vì chỉ nằm trong chat.
8. Internal link cần dùng URL thật từ `internal-links.csv` (crawl sitemap hoặc tab Site URL).

**`seo-article-writer`**

1. `/mnt/user-data/outputs` và `present_files` chỉ có trên claude.ai. Cần đổi sang ghi vào `content/…` rồi đẩy sang Doc theo **format 2.3**.
2. Số từ cho FAQ không thống nhất (phần hướng dẫn ghi 50–75 từ, template ghi 35–50 từ). Nên lấy theo format.
3. Các quy tắc cứng (cấm em dash, cấm dấu chấm phẩy, cấm cliché, từ cấm của brand) đang dựa vào việc Claude tự kiểm. Cần chuyển thành script `content_lint.py` chạy tự động qua hook.
4. Cần thêm bước đối chiếu số liệu với `facts.yaml`:
   - dữ kiện không có trong fact sheet → gắn `[NEED CLIENT CONFIRMATION: … | nguồn]` hoặc `[VERIFY: …]`, rồi đưa vào Client Confirmation List
   - mục đang "⚠ Verify" thì bị chặn, ví dụ ISO 14001, GOTS, tỉnh Nam Dinh/Ninh Binh của CWG
5. Disclaimer theo loại nội dung phải được tự chèn từ `rules.yaml`, vì brand CWG mục 7.2 bắt buộc.
6. Chưa xuất HTML và schema (Article, FAQPage, BreadcrumbList). Việc này giao cho `/html`.
7. Thêm một lượt line-edit cuối bằng skill `ai-writing-tells` + `natural-english-writing` (hoặc `natural-vietnamese-writing`), rồi để agent `content-reviewer` chấm điểm trước khi chuyển SEN.

### 7.5 Kiểm tra tự động (hooks)

- `content_lint.py` chạy sau mỗi lần Claude ghi file trong `content/`. Script kiểm:
  - em dash, dấu chấm phẩy, cliché, từ cấm của brand (ví dụ "state-of-the-art", "world-class", "eco-friendly")
  - chính tả Anh/Mỹ theo market, định dạng số (5,000 chứ không phải 5.000)
  - số internal link tối thiểu, có CTA, có disclaimer
  - số liệu không có trong `facts.yaml` mà chưa được gắn tag
- Bài chưa qua lint thì không được chuyển sang Status "Draft Ready".

### 7.6 Định dạng HTML cho blog

- Mỗi format có một template HTML gồm các thành phần: key takeaways, mục lục, bảng thông số, callout, FAQ dạng accordion kèm FAQPage JSON-LD, CTA box, author box với "Reviewed by" và "Last reviewed".
- Style dùng biến (màu, font, bo góc) lấy từ `project/brand/` để khớp giao diện site.
- Trước khi giao, Claude chụp preview desktop và mobile bằng trình duyệt headless để kiểm tra hiển thị.
- Cần 1–2 mẫu HTML đang dùng và cách đăng bài hiện tại (câu hỏi D2).

### 7.7 Dịch content

- Tái sử dụng skill `translate-html`. Mỗi dự án có `glossary.csv` (thuật ngữ không dịch, tên brand, tên phòng/nhà máy) và bản đồ internal link riêng cho từng ngôn ngữ, theo cách skill `bhaya-translate-html` đang làm.
- Bản dịch được ghi vào phần `Draft_<lang>` của cùng Doc. Sau khi dịch, chạy lint theo quy tắc của thị trường đích.

---

## 8. Research, Plan & Forecast

### 8.1 Nguồn dữ liệu

| Việc | Nguồn chính | Nguồn phụ |
| --- | --- | --- |
| Volume, KD, CPC, intent, related keywords | DataforSEO (nếu "SEO Data" là DataforSEO, câu hỏi C1) | SE Ranking |
| SERP top 10, PAA, AI Overview | SERP API | DataforSEO SERP |
| Đọc nội dung trang đối thủ | Firecrawl | Trình duyệt headless |
| Domain đối thủ: ranked keywords, keyword gap, backlinks | DataforSEO Labs + Backlinks | SE Ranking |
| GSC/GA4 lịch sử | Agency Analytics | — |
| AI visibility (prompt, mention, citation) | Cần chốt công cụ (câu hỏi C3) | DataforSEO AI Optimization / SE Ranking |
| Dữ liệu ngành | File team cung cấp trong `project/research/` và Drive/Research | Nguồn chính thống có tên và năm |

### 8.2 Forecast (tab Measurement)

1. **Giữ công thức hiện có** (Mục 2.5). `/forecast` lấy số theo tháng từ Agency Analytics:
   - Organic Traffic
   - AI Traffic: lọc theo `ai_referrers` trong config
   - Booking/Leads: theo `conversion_events`
   Sau đó Claude điền các dòng Actual. Market trend và Goal tự tính bằng công thức có sẵn.
2. Claude viết phần diễn giải: mùa vụ lấy từ Onboarding (ví dụ Sukosol: cao điểm Oct–Feb, thấp điểm Mar–Apr và Sep), các tháng bất thường, và rủi ro.
3. **v2, tham chiếu bottom-up:** với mỗi dòng Velocity trong Content Plan, uplift = volume × CTR ở vị trí mục tiêu × hệ số ramp-up theo tháng kể từ khi đăng. Kết quả đặt ở cột phụ để SEN so với Goal, không thay công thức chính.
4. Mọi phép tính nằm trong Sheet hoặc `scripts/forecast.py`. Claude không tự nhẩm số.

---

## 9. Technical, Tracking và UI/UX

### 9.1 Đưa source website lên repo

| Nền tảng | Cách lấy | Claude làm được gì |
| --- | --- | --- |
| WordPress (phổ biến nhất ở các dự án mẫu: Yoast, Rank Math, WPML, WPBakery) | Theme + danh sách plugin (không lấy `wp-content/uploads`, `wp-config.php`). Nội dung lấy qua WP REST API hoặc crawl | Audit template, schema, head tags, plugin SEO, WPML/hreflang. Đề xuất thay đổi theo từng file |
| Custom (Next.js, Laravel…) | Git submodule hoặc copy vào `website/` | Audit code + **tạo patch/PR** cho dev |
| Shopify | Theme qua Shopify CLI | Audit Liquid template |
| Webflow / Wix / SquareSpace | Không có source, chỉ crawl | Audit dựa trên HTML render |

**Bảo mật:** dùng `.gitignore` mẫu theo từng nền tảng, quét secret (gitleaks) trước khi commit. Source chỉ được đưa lên khi hợp đồng/NDA cho phép (câu hỏi D1).

### 9.2 Technical audit kết hợp 3 nguồn

1. **Crawl:** Firecrawl map/crawl, hoặc script crawl bằng trình duyệt headless cho site render bằng JS. Nếu team có Screaming Frog thì upload CSV export.
2. **Source:** head tags, canonical, hreflang, robots, sitemap, schema, lazy-load, script chặn render, định dạng ảnh.
3. **Hiệu năng:** PageSpeed Insights API hoặc Lighthouse chạy trực tiếp trong môi trường (Chromium có sẵn).

Output:

- Tab **Technical Baseline** (5 layer, mỗi dòng có bằng chứng định lượng như ví dụ Sukosol)
- Sheet **Website Audit** với các tab đúng như mẫu (URL, Website Structure, Content Audit, Noindex, Canonical, 301, 404, Multiple-H1, Missing H1, Page Title Duplicate, Non-canonical, Image)
- **Website Fix List** cho dev
- Doc **Schema Markup** chứa JSON-LD sẵn để dán
- Với site có source thì kèm patch

### 9.3 Google Tag Manager (chưa có connector)

1. Phân tích site và source để liệt kê các điểm chuyển đổi: book now, form, click tel/mailto/WhatsApp/Zalo, chat, booking engine, tải PDF, CTA offer.
2. Viết **Tracking Plan** vào folder Tracking/: tên event, trigger, parameter, có phải key event không. Ví dụ Sukosol: `book_now_click`, `generate_lead`, `click_to_call`, `chat_start`, `offer_click`, `dining_reserve`.
3. Sinh **file container JSON** (tag, trigger, variable) để PIC import vào GTM bằng Admin › Import Container › **Merge** vào một workspace mới. Claude không tự publish container.
4. Kiểm tra bằng trình duyệt headless: mở trang, thực hiện hành động, bắt request gửi về GA4 (`/g/collect`) để đối chiếu tên event và parameter. Với booking engine thì kiểm thêm cross-domain.
5. Ghi kết quả vào layer Tag tracking của Technical Baseline và vào **GA4 Leads Tracking**.

### 9.4 UI/UX audit (folder mới)

- Chụp screenshot desktop và mobile cho từng loại template trang: home, room/product, blog, contact, booking.
- Đánh giá theo heuristic UX, CRO và 2 rule GEO infrastructure (dùng lại skill `geo-infra-audit`).
- Output: báo cáo có chú thích trên ảnh và đề xuất theo mức ưu tiên, lưu trong UI-UX/.
- **Figma:** connector Figma có trong danh mục nhưng chưa cài.
  - Nếu cài, Claude đọc được frame, screenshot và cấu trúc thiết kế để so với site thật.
  - Nếu chưa cài, designer đưa ảnh và chú thích lên Figma.
  - Mẫu audit mong muốn cần chốt (câu hỏi D3).

---

## 10. Monitoring và Reporting

### 10.1 Bộ lọc hỏi đáp Agency Analytics

```
/analytics week                          # tuần trước so với tuần trước nữa
/analytics month 2026-10 vs yoy          # tháng 10 so với cùng kỳ năm ngoái
/analytics last-28d group=insights       # theo nhóm trang khai báo trong config
/analytics month query=non-branded       # tách branded/non-branded bằng regex trong config
/analytics quarter country=TH device=mobile
/analytics month source=ai               # traffic từ ChatGPT, Perplexity, Gemini…
```

- Mỗi lần chạy lưu snapshot vào `data/analytics/` để so sánh các kỳ mà không phải gọi lại API.
- Sau khi có bảng số, có thể hỏi tự do, ví dụ "Vì sao clicks nhóm insights giảm?" hoặc "Top 10 trang tăng mạnh nhất?".
- Giai đoạn sau có thể thêm một dashboard HTML có bộ lọc tuần/tháng.

### 10.2 Weekly Health Check tự động (P06a)

- Dùng scheduled task của Claude Code, chạy sáng thứ Hai cho từng dự án. GitHub Actions không dùng được connector của claude.ai nên không phù hợp.
- Kiểm tra:
  - clicks, sessions và conversions giảm vượt ngưỡng
  - trang top bị rơi hạng
  - 404/5xx mới từ crawl mẫu
  - bài mới đã được index chưa
  - robots.txt và sitemap có thay đổi
  - prompt GEO bị mất mention
- Sơ đồ ghi "update status in Asana". Nếu cài Asana connector thì Claude cập nhật task trực tiếp. Nếu không, Claude ghi báo cáo tuần để PIC tự cập nhật (câu hỏi A3).

### 10.3 Báo cáo tháng và báo cáo executive

- Số liệu lấy từ script. Claude viết phần insight, nguyên nhân và kế hoạch tháng sau.
- Báo cáo executive ngắn gọn, tập trung vào lead/booking và AI visibility.

### 10.4 Cây chẩn đoán (đi theo đúng sơ đồ P06)

- **Path 1, content kém:**
  1. Chưa index → kiểm tra và sửa nguyên nhân kỹ thuật.
  2. Đã index nhưng không có giá trị → quay lại content research.
  3. Intent có khớp không → brief có lệch trend không → kiểm tra brand fit và nội dung người dùng cảm nhận.
  4. Vẫn không cải thiện → quay lại phân tích onboarding.
- **Path 2, mọi thứ ổn nhưng hiệu quả yếu:** nghi lỗi kỹ thuật → full-site technical audit, gồm UX/UI và tốc độ trang.
- **Path 3, kỹ thuật cũng ổn:** kiểm tra giao diện và CTA → chuyển sang P07a.
- **GEO P06e:** chỉ số kém → tìm GEO gap so với đối thủ dựa trên research P03 → thêm phần còn thiếu vào nội dung site.
- **GEO P06f:** mention sai hoặc tiêu cực → tìm nguồn → sửa thông tin chính thức trên site → khi ổn định thì chuyển sang P07b.

---

## 11. Bảo mật, chi phí, vận hành

- **Credential:**
  - Không lưu mật khẩu trong Sheet, Doc hay repo. Tab SEO Assets chỉ giữ trạng thái TRUE/FALSE và email tài khoản.
  - Mật khẩu chuyển sang trình quản lý mật khẩu của team, và nên đổi mật khẩu CMS của Sukosol vì đã nằm trong Sheet.
  - CLAUDE.md sẽ cấm Claude đọc cột "Related info" của SEO Assets.
- Repo dự án để private, phân quyền theo pod. Không commit file chứa thông tin cá nhân (PII) hoặc credential. Hook quét secret chạy trước mỗi commit.
- API key cho các dịch vụ gọi trực tiếp (PageSpeed, DataforSEO nếu không qua connector) lưu dưới dạng secret của environment, không đặt trong repo.
- **Chi phí API:** cache kết quả SERP và keyword trong `data/cache/` có thời hạn, và đặt ngân sách mỗi dự án trong `config.yaml`.
- Claude chỉ ghi vào bản nháp hoặc Status đang chờ duyệt, không gửi gì trực tiếp cho khách.
- `validate_project.py` kiểm tra config, ID file trên Drive và quyền connector trước khi chạy skill.

---

## 12. Lộ trình triển khai

Thời gian dưới đây là ước tính, sẽ chỉnh sau khi chốt Mục 13.

| Phase | Nội dung | Kết quả nghiệm thu |
| --- | --- | --- |
| **0. Chốt và thử connector** (2–3 ngày) | Trả lời câu hỏi ★. Bật AgencyAnalytics, SEO Data, SERP API, Firecrawl, SE Ranking. Cấp quyền Editor trên Drive. Chạy thử từng connector và ghi khả năng/giới hạn vào `docs/connectors.md` | Bảng năng lực connector. Kiến trúc được chốt |
| **1. Khung template** (tuần 1) | CLAUDE.md, cấu trúc thư mục, `sheet-schemas` theo format Sukosol, Drive Template, `/new-project`, chuyển brand guideline thành brand pack, sync-core, quét secret. Tạo repo CWG | Tạo dự án mới (repo + Drive) trong ≤ 30 phút. Claude trả lời đúng fact của CWG và chặn các mục "⚠ Verify" |
| **2. Content engine** (tuần 2–3) | Nâng cấp outline + writer, 3 content type, 6–8 format Velocity/Infrastructure, playbook hospitality và b2b-manufacturing, content-lint, Doc writer theo format 2.3, HTML, dịch, `/content-month` | 3 bài Sukosol tháng 12 đi trọn từ Content Plan đến Doc + HTML, 0 lỗi lint, SEN chấm đạt |
| **3. Research và Plan** (tuần 3–5) | Foundation, Problem Pattern, Tracking (keyword + prompt), Content Plan, Technical Baseline, Offsite, Measurement, `/p04e-review`, sửa theo comment, Plan → Masterfile | Plan CWG đủ 7 tab. SEN chỉ phải sửa ≤ 20% |
| **4. Technical, Tracking, UI/UX** (tuần 5–6) | Đưa source lên, tech audit 3 nguồn, Website Audit, Fix List, Schema doc, on-page, GTM plan/build/verify, UI/UX audit | Audit CWG + container GTM import được và kiểm tra đạt |
| **5. Monitoring, Report, GEO** (tuần 6–7) | `/analytics`, health check hằng tuần, báo cáo tháng/executive, cây chẩn đoán, GEO visibility/gap/mentions, off-page/GBP | Báo cáo tháng Sukosol tạo tự động. Health check chạy đúng lịch |
| **6. CRO, Handover, Rollout** (tuần 8+) | P07, `/handover`, tài liệu và đào tạo team, chuyển plugin (v2), áp dụng cho I'Msignia và các dự án khác | 2–3 dự án khác chạy trên template |

---

## 13. Câu hỏi cần chốt

Câu ★ là câu đang chặn Phase 0–1. Câu đánh dấu ✅ đã có câu trả lời từ dữ liệu Drive.

**A. Kiến trúc và vận hành**
- ✅ A1. Template + repo riêng cho từng khách.
- ✅ A2. Chạy trên web/app claude.ai/code. Còn cần biết: bao nhiêu người dùng (PIC/JR/INT), và tài khoản GitHub của họ có trong org `talabadao` chưa?
- A3. Có cần tích hợp Asana không (sơ đồ P06a ghi "update status in Asana")? Nếu có thì cài Asana connector.

**B. Google Drive**
- ✅ Cấu trúc Plan/Masterfile và format Content Doc: đã đọc từ Sukosol và I'Msignia.
- ★B1. Tài khoản đang kết nối chỉ có quyền **xem** trên các folder mẫu. Folder dự án mới sẽ nằm ở đâu (Shared Drive của team hay My Drive của `analytics@`), và có cấp quyền Editor cho tài khoản chạy Claude không?
- ✅ B2. Giữ đúng format Plan 7 tab của The Sukosol.
- B3. Ad-Lib và Bhaya (format cũ) có cần chuyển sang format mới, hay giữ nguyên?
- B4. Đồng ý chuyển mật khẩu ra khỏi tab SEO Assets và đổi mật khẩu CMS của Sukosol?

**C. Dữ liệu và connector**
- ★C1. Connector "SEO Data" có phải DataforSEO không? SE Ranking dùng cho việc gì (rank tracking?). Search volume trong tab Tracking đang lấy từ nguồn nào (có giá trị dạng "1-10")? Ngân sách API mỗi dự án mỗi tháng?
- C2. Trong tab Measurement:
  - "Organic Traffic" là GA4 organic sessions hay GSC clicks?
  - "AI Traffic" đang lọc theo nguồn nào?
  - "Booking" lấy từ GA4 purchase, key event hay báo cáo của khách?
- C3. Prompt tracking và AI visibility hiện đo bằng công cụ gì?
- C4. GTM: dùng cách Claude sinh file JSON để PIC import là đủ, hay muốn gọi thẳng GTM API?

**D. Website và content**
- ★D1. Lấy source website bằng cách nào (theme qua SFTP, git của dev, export)? Claude chỉ đề xuất, hay được tạo patch/PR cho dev? Hợp đồng có cho phép đưa source lên GitHub không?
- D2. Bài được đăng thế nào (Custom HTML block, Gutenberg, WPBakery…)? Claude chỉ giao file, hay được đăng bản nháp qua WP REST API? Gửi 1–2 mẫu HTML blog đang dùng.
- D3. Figma: có cài Figma connector không? Mẫu UI/UX audit mong muốn trông thế nào (link file Figma mẫu nếu có)?
- D4. Các skill org (category-definer, problem-pattern-identifier, geo-infra-audit, ai-writing-tells, translate-html…): đưa vào repo để quản lý version, hay giữ ở claude.ai và chỉ gọi tới?
- D5. Có tài liệu GEO OS trên Drive không (định nghĩa Category Leader, Infrastructure/Velocity/Authority, quy tắc infrastructure)? Gửi link để đưa vào `core/`.
- D6. Những ngôn ngữ nào hay phải dịch? (Đã thấy: Thai, và de/es/fr/ko/zh/vi ở Bhaya.)

**E. Pilot và cổng duyệt**
- ✅ E1. Pilot CWG + The Sukosol. Còn cần biết: CWG đã có folder Drive, Onboarding Questions, campaign Agency Analytics và source website chưa?
- E2. Claude được ghi thẳng vào Plan/Masterfile và Doc mà khách đang xem, hay chỉ ghi vào bản nháp nội bộ rồi PIC chép sang?
- E3. Chốt danh sách Status cho Content Plan (đề xuất ở Mục 7.2).

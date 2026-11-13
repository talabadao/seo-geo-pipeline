# SEO/GEO Pipeline × Claude Code: Kế hoạch triển khai

**Phiên bản:** v0.1 (bản nháp, chờ trả lời các câu hỏi ở Mục 12)
**Ngày:** 13/11/2026
**Phạm vi:** Template GitHub dùng chung cho quy trình SEO/GEO của Liam's Pod (P01–P07 + Handover), chạy bằng Claude Code, kết nối Google Drive/Sheets/Docs, Agency Analytics, SERP API, Firecrawl và DataforSEO.

---

## 0. Tóm tắt

1. **Kiến trúc 3 lớp.** Lớp Core gồm skill, agent, hook, format bài, playbook ngành và quy tắc thị trường, dùng chung cho mọi dự án. Lớp Project Template là cấu trúc thư mục cùng file config mẫu. Mỗi khách hàng có một Client Repo riêng, tạo từ template, chứa brand, source website, content, audit và report.
2. **Phân vai lưu trữ.** Google Sheets là nơi lưu chính cho Plan, Masterfile và Content Tracker, vì team và khách cùng làm việc ở đó. Git là nơi lưu chính cho skill, config, bản nháp, audit và lịch sử thay đổi. Google Docs là định dạng giao cho khách. Claude đọc và ghi cả ba nơi qua connector.
3. **Mỗi bước P01–P07 ứng với một skill gọi bằng `/lệnh`.** Mỗi skill có input, output, nơi lưu và cổng duyệt rõ ràng, khớp với vai trò trong pipeline: PIC chạy, SEN duyệt, AM/PM gửi khách. Claude không bao giờ gửi thẳng cho khách.
4. **Skill viết content được ghép từ nhiều lớp:** Core skill + format theo loại bài + playbook ngành + quy tắc thị trường/ngôn ngữ + brand pack của dự án. Nhờ vậy không cần nhân bản skill cho từng dự án mà vẫn tối ưu được cho từng loại bài, ngành và thị trường.
5. **Mọi con số do script tính, Claude chỉ diễn giải.** Áp dụng cho forecast, báo cáo và so sánh kỳ, để kết quả lặp lại được và không bị LLM "đoán số".
6. **Triển khai trong 6 phase, pilot trên Capital World Group.** Content engine được ưu tiên làm trước vì đó là việc lặp lại hàng tháng.

---

## 1. Hiện trạng đã kiểm tra

| Hạng mục | Trạng thái | Ghi chú |
| --- | --- | --- |
| Repo `talabadao/seo-geo-pipeline` | Trống | Branch làm việc: `claude/brave-allen-8m31rd` |
| Connector của org | Đã kết nối: AgencyAnalytics, Firecrawl, Google Docs, Google Drive, Google Sheets, SERP API, SEO Data, SE Ranking, Canva, Supabase, Vercel | Trong phiên này mới bật Drive và Sheets |
| Google Drive connector | **Chỉ có công cụ xem lịch sử phiên bản file** | Các công cụ tìm, đọc, tạo và upload đang tắt, nên chưa đọc được 4 folder mẫu (xem câu hỏi B1) |
| Chưa có connector | Figma, Google Tag Manager, Asana | Có cách làm thay ở Mục 8 và Mục 9. "DataforSEO" có thể chính là connector "SEO Data" (xem câu hỏi C1) |
| Skill `seo-outline` | Đã đọc | Quy trình 3 phase tốt, cần chuyển sang dùng trong Claude Code và bổ sung phần GEO (Mục 6.3) |
| Skill `seo-article-writer` | Đã đọc | Quy tắc viết tốt, nhưng đường dẫn output là của claude.ai và các quy tắc cứng chưa được kiểm tự động (Mục 6.3) |
| Brand Guideline CWG | Đã đọc | Rất phù hợp làm mẫu "brand pack": có fact sheet đã duyệt (Phụ lục A) và danh sách mục cần xác minh (Phụ lục B) |
| Skill có sẵn của org | category-definer, problem-pattern-identifier, geo-infra-audit, geo-visibility-report, llms-txt-builder, keyword-list-proposal, business-research-proposal, ai-content-writer, ai-writing-tells, natural-english-writing, natural-vietnamese-writing, translate-html, local-area-researcher, pr-writer | Nên tái sử dụng thay vì viết lại (xem câu hỏi D4). P04a "Problem Patterns" khớp với `problem-pattern-identifier` |

---

## 2. Kiến trúc tổng thể

```
┌──────────────────────────────────────────────────────────────────────┐
│  CORE (repo này: seo-geo-pipeline, bật "Template repository")        │
│  .claude/skills · .claude/agents · hooks · core/formats              │
│  core/industries · core/markets · core/sheet-schemas · scripts/      │
└───────────────┬──────────────────────────────────────────────────────┘
                │ "Use this template" khi có dự án mới
                │ scripts/sync-core.sh để kéo bản cập nhật về sau này
┌───────────────▼──────────────────────────────────────────────────────┐
│  CLIENT REPO  (talabadao/seo-<client-slug>, private)                 │
│  project/config.yaml · project/brand/* · website/ (source)           │
│  content/ · audits/ · reports/ · data/                               │
└───────┬─────────────────────┬─────────────────────┬──────────────────┘
        │ Claude Code         │                     │
┌───────▼───────┐   ┌─────────▼─────────┐  ┌────────▼─────────────────┐
│ Google Drive  │   │ Data connectors   │  │ Website (live + source)  │
│ Sheets · Docs │   │ Agency Analytics  │  │ Firecrawl · Playwright   │
│ Plan,         │   │ DataforSEO        │  │ PageSpeed/Lighthouse     │
│ Masterfile,   │   │ SERP API          │  │ GTM container JSON       │
│ Content Docs  │   │ SE Ranking        │  │                          │
└───────────────┘   └───────────────────┘  └──────────────────────────┘
```

### 2.1 Chiến lược repo

- `seo-geo-pipeline` (repo này) là **template repo**. Mỗi dự án mới được tạo bằng "Use this template" thành `talabadao/seo-<client-slug>` ở chế độ private.
- **Vấn đề:** GitHub không tự đẩy thay đổi của template xuống các repo đã tạo. Khi nâng cấp skill viết bài, 10 dự án đang chạy sẽ không nhận được bản mới.
  - **v1 (đề xuất):** dùng `scripts/sync-core.sh` để kéo `.claude/`, `core/` và `scripts/` từ template về repo dự án. Script không đụng vào `project/`, `website/`, `content/`, `audits/` hay `reports/`. Cách này đơn giản và chạy được ở mọi nơi (web, desktop, CLI).
  - **v2 (khi skill đã ổn định):** đóng gói Core thành Claude Code plugin marketplace. Repo dự án chỉ cần khai báo plugin trong `.claude/settings.json`, nên cập nhật một lần là mọi dự án đều nhận.
- **Ranh giới bắt buộc:** không sửa `core/` và `.claude/` trong repo dự án. Phần tùy biến riêng của dự án đặt trong `project/overrides/` để lần sync sau không ghi đè mất.

### 2.2 Nơi lưu chính cho từng loại dữ liệu

| Dữ liệu | Nơi lưu chính | Cách Claude dùng |
| --- | --- | --- |
| SEO/GEO Plan, Masterfile, Content Plan, trạng thái task | Google Sheets | Đọc/ghi qua Sheets connector, cột `Status` điều khiển luồng làm việc |
| Outline, bản nháp, HTML | Git (`content/`) → bản giao trên Google Docs | Viết vào repo, chạy lint, rồi đẩy sang Docs. Khi khách sửa trên Docs thì đọc ngược lại |
| Brand, onboarding, fact sheet | Git (`project/brand/`), có bản gốc trên Drive | Claude luôn đọc từ repo vì có version, diff được và nhanh |
| Source website | Git (`website/` hoặc submodule) | Audit code, đề xuất patch hoặc mở PR |
| Dữ liệu analytics, keyword, SERP | Connector → snapshot ở `data/` | Lưu cache để không gọi API lặp lại và để so sánh các kỳ |
| Audit, báo cáo | Git (`audits/`, `reports/`) → Sheets/Docs để giao | |

---

## 3. Cấu trúc repo (template)

```
seo-geo-pipeline/
├── CLAUDE.md                     # "Luật vận hành": pipeline, vai trò, cổng duyệt, quy tắc chung
├── README.md                     # Hướng dẫn tạo dự án mới trong 30 phút
├── .claude/
│   ├── settings.json             # permissions, hooks (content-lint, secret-scan)
│   ├── skills/                   # mỗi skill = 1 thư mục SKILL.md (+ references/, scripts/)
│   └── agents/                   # subagent chuyên trách (xem 3.2)
├── core/
│   ├── formats/                  # blog-guide, listicle, comparison, how-to, news, pillar,
│   │                             # service-page, location-page, product/category, landing
│   ├── industries/               # hospitality, b2b-manufacturing, ecommerce, ... (playbook ngành)
│   ├── markets/                  # en-GB, en-US, en-AU, vi-VN, ko-KR, ... (chính tả, SERP
│   │                             # location, domain cần loại trừ khi phân tích đối thủ)
│   ├── html-templates/           # component blog: TOC, key takeaways, bảng, FAQ, CTA, author box
│   ├── sheet-schemas/            # định nghĩa cột cho từng tab của Plan/Masterfile
│   └── checklists/               # access checklist (P02), technical checklist (P04d), QA content
├── scripts/                      # Python: forecast.py, crawl.py, content_lint.py, gtm_build.py,
│                                 # analytics_snapshot.py, validate_project.py, sync-core.sh
├── project/                      # ← PHẦN RIÊNG CỦA DỰ ÁN (điền sau khi clone)
│   ├── config.yaml
│   ├── brand/
│   │   ├── brand.md              # voice, tone theo loại nội dung, định vị, audience
│   │   ├── facts.yaml            # số liệu đã duyệt + mục "⚠ verify" (bị chặn khi viết)
│   │   ├── rules.yaml            # chủ đề cấm, từ cấm và từ thay thế, disclaimer, quy ước tên
│   │   ├── internal-links.csv    # URL thật của site (crawl sitemap) + chủ đề + anchor gợi ý
│   │   ├── glossary.csv          # thuật ngữ không dịch / dịch cố định theo ngôn ngữ
│   │   └── source/               # bản gốc: brand guideline, onboarding form
│   ├── research/                 # dữ liệu ngành do team cung cấp
│   ├── overrides/                # format hoặc rule riêng của dự án
│   └── decisions.md              # nhật ký feedback và quyết định của khách
├── website/                      # source website (hoặc git submodule)
├── content/YYYY-MM/<slug>/       # brief.md, outline.md, draft.md, draft.html, translations/
├── audits/                       # technical/, uiux/, geo/, tracking/
├── reports/                      # weekly/, monthly/, executive/
└── data/                         # snapshot analytics/keyword/SERP (file lớn đưa vào .gitignore)
```

### 3.1 `project/config.yaml` (ví dụ với CWG)

```yaml
project:
  name: Capital World Group
  slug: cwg
  domain: capitalworldgroup.com
  industry: b2b-manufacturing        # → core/industries/b2b-manufacturing.md
  business_model: leadgen            # leadgen | booking | ecommerce | local
  cms: wordpress
  stage: P04                         # bước hiện tại trong pipeline
markets:
  - locale: en-GB                    # → core/markets/en-GB.md (CWG dùng chính tả Anh)
    serp_locations: [United States, Italy, Brazil]
languages: [en]
drive:
  root_folder_id: ""
  plan_sheet_id: ""
  masterfile_sheet_id: ""
  content_folder_id: ""
  technical_sheet_id: ""
analytics:
  agency_analytics_campaign_id: ""
  gsc_property: "sc-domain:capitalworldgroup.com"
  ga4_property_id: ""
  gtm_container_id: ""
  page_groups:                       # dùng cho bộ lọc báo cáo
    insights: "^/(what-is|oem-vs|custom-garment|vietnam-)"
    products: "^/products/"
  branded_regex: "capital world|cwg|kiara garment|hp vina"
competitors: []                      # domain cần ưu tiên phân tích
content:
  word_range: [1000, 1800]
  min_internal_links: 2
  cta_options: ["Contact our team", "Download our company profile"]
budget:
  dataforseo_usd_per_month: 30       # giới hạn chi phí API mỗi dự án
```

### 3.2 Subagent

| Agent | Nhiệm vụ | Lý do tách riêng |
| --- | --- | --- |
| `serp-researcher` | Lấy top 10, PAA, AI Overview, đọc 5 trang đối thủ | Nhiều dữ liệu thô, không nên làm đầy ngữ cảnh chính |
| `competitor-analyst` | Phân tích domain đối thủ, keyword gap, backlink gap | Chạy song song nhiều đối thủ |
| `content-reviewer` | Đóng vai SEN, chấm bài theo checklist trước khi chuyển người duyệt | Góc nhìn độc lập với người viết |
| `tech-auditor` | Đọc source và kết quả crawl, phân loại lỗi | Source website rất lớn |

---

## 4. Cấu trúc Google Drive dự án (bản nháp, sẽ chỉnh sau khi đọc 4 folder mẫu)

```
[Client] SEO-GEO/
├── 00. Onboarding & Brand/        onboarding form, brand guideline, access checklist
├── 01. SEO-GEO Plan               (Sheet, gửi khách đầu tiên)
├── 02. SEO-GEO Masterfile         (Sheet = bản sao của Plan + các tab triển khai)
├── 03. Content/
│   └── 2026-12/                   Docs outline và bài viết theo tháng
├── 04. Technical-Audit            (Sheet)
├── 05. Off-page/                  backlink plan, outreach content, GBP posts
├── 06. UI-UX/                     link Figma audit + đề xuất chỉnh sửa
├── 07. Reports/                   monthly, executive
└── 08. Others/
```

**Các tab dự kiến trong SEO/GEO Plan:** Overview & Goals · Business & Audience · Market & Competitors · Problem Patterns · Keywords · Prompt Tracking · Content Plan (≥ 6 tháng) · Technical Checklist · Forecast · Roadmap.

**Các tab Masterfile bổ sung:** Monthly Tasks · Content Tracker · On-page Tracker · Technical Fix Log · Off-page/Backlink Log · GBP Posts · Internal Link Map · Tracking Plan (GTM/GA4) · Rank & Prompt Tracking · Weekly Health Check · Change Log.

**Tạo folder tự động:** cần Drive connector cho phép tạo folder và copy file. Nếu admin không mở được quyền này, phương án dự phòng là một Google Apps Script "Project Bootstrapper": AM/PM bấm một nút trong Sheet là copy toàn bộ cây folder mẫu, rồi Claude ghi ID các file vào `config.yaml` (xem câu hỏi B2).

---

## 5. Map pipeline → skill

| Bước | Skill / lệnh | Người chạy → Người duyệt | Input | Output | Cổng duyệt |
| --- | --- | --- | --- | --- | --- |
| **Handover** | `/handover` | PIC mới | Plan cũ, onboarding form, Masterfile, lịch sử repo | Brief tóm tắt, rủi ro, câu hỏi cho buổi catch-up với PIC cũ + AM/PM | — |
| **P01** Onboarding | `/new-project`, `/p01-onboarding-check` | AM/PM + PIC | Onboarding form, brand guideline | `config.yaml`, brand pack (`brand.md`, `facts.yaml`, `rules.yaml`), danh sách thông tin còn thiếu gửi AM/PM | AM/PM xác nhận form đủ |
| **P02** Access & Tracking | `/p02-access-audit` | PIC → AM/PM + PIC | config, live site | Checklist GA4/GSC/GTM/CMS/GBP/booking engine (đọc từ Agency Analytics + quét HTML tìm GTM/GA4 ID, cross-domain), mục thiếu được gắn cờ | Đủ quyền truy cập |
| **P03** Research & Strategy | `/p03-research` | PIC → PIC | Brand pack, đối thủ, dữ liệu ngành | Báo cáo thị trường + đối thủ (DataforSEO, SERP API, Firecrawl), tab Market & Competitors | — |
| **P04a** Problem Patterns | `/p04a-categories` → `/p04a-problem-patterns` | PIC | P03 + GSC queries | Category + problem pattern map (dùng lại skill org) | |
| **P04b** Keywords & Prompts | `/p04b-keywords`, `/p04b-prompts` | PIC | P04a | Keyword list (volume/KD/intent/cluster) + bộ prompt theo dõi AI | |
| **P04c** Content Plan | `/p04c-content-plan` | PIC | P04a–b | Roadmap ≥ 6 tháng: cluster, format, URL đích, tháng, internal link | |
| **P04d** Technical Checklist | `/p04d-tech-baseline` | PIC | Crawl + source + PSI | Bức tranh kỹ thuật ban đầu | |
| **P04e** Complete Plan | `/p04e-build-plan`, `/forecast` | PIC → **SEN** | P04a–d + GSC/GA4 lịch sử | Sheet Plan hoàn chỉnh theo template + Forecast | **SEN duyệt** → AM/PM gửi khách |
| P04 vòng sửa | `/p04-revise` | PIC | Comment của khách trên Sheet | Bản sửa + ghi `decisions.md` | Lặp đến khi khách duyệt |
| P04 → P05 | `/p04-to-masterfile` | PIC | Plan đã duyệt | Masterfile (copy Plan + tab triển khai) | |
| **P05** Technical SEO | `/tech-audit`, `/tech-fix` | PIC → SEN | Source + crawl | Sheet issue (mức độ, URL, bằng chứng, cách sửa) + patch/PR cho dev | SEN |
| **P05** Content SEO | `/content-month`, `/outline`, `/write`, `/html`, `/translate` | PIC → SEN | Content Plan | Outline → Draft → HTML → bản dịch (Mục 6) | SEN, sau đó khách |
| **P05** On-page SEO | `/onpage <url>` | PIC | URL + keyword đích | Title/meta/H1/heading/schema/internal link đề xuất + tracker | |
| **P05** Off-page/Local | `/offpage-plan`, `/gbp-posts` | PIC | Backlink đối thủ (DataforSEO), brand | Prospect list, outreach template, GBP post theo tháng | |
| **P05** Analytics/GEO | `/gtm-plan`, `/gtm-build`, `/gtm-verify`, `/llms-txt` | PIC → SEN | Source + live site | Tracking plan, file container GTM để import, kết quả kiểm tra | SEN trước khi publish container |
| **P06a** Health Check | `/health-check` (tự chạy hằng tuần) | PIC → SEN | Agency Analytics + crawl mẫu | Dòng mới trong tab Weekly Health Check + cảnh báo | |
| **P06b/c** Reports | `/report monthly`, `/report executive` | PIC → SEN | Agency Analytics, Masterfile | Báo cáo tháng / báo cáo cho lãnh đạo khách | SEN |
| **P06d** Client Meeting | `/meeting-prep`, `/meeting-notes` | AM/PM + PIC | Báo cáo, ghi chú họp | Agenda, action items ghi vào Masterfile | |
| **P06** SEO Diagnosis | `/diagnose <url/nhóm trang>` | PIC | Analytics, index, SERP | Đi theo đúng cây Path 1/2/3 trong sơ đồ, kết luận bước tiếp theo | |
| **P06e/f** GEO | `/geo-visibility`, `/geo-gap`, `/geo-fix-mentions` | PIC | Prompt tracking, AI responses | Gap so với đối thủ → content bổ sung. Mention sai → tìm nguồn → sửa thông tin trên site | |
| **P07a** CRO | `/cro-audit` | PIC → SEN | GA4 funnel + screenshot | Đề xuất tối ưu booking/lead | |
| **P07b** AI Conversion | `/geo-expand` | PIC | P06e/f | Mở rộng prompt, tối ưu trang được AI trích dẫn | |
| **UI/UX** | `/uiux-audit` | PIC/Designer | Screenshot desktop/mobile | Báo cáo có chú thích, đưa lên Figma (Mục 8.4) | |

**Quy tắc chung trong CLAUDE.md:** mỗi skill khi chạy xong phải (1) ghi output vào repo, (2) cập nhật Status/link trong Sheet, (3) ghi một dòng vào Change Log, (4) báo PIC cần ai duyệt tiếp. Nếu thiếu input, skill dừng lại và liệt kê những gì cần AM/PM bổ sung, đúng như ghi chú "return to P01 and contact AM/PM" trong sơ đồ.

---

## 6. Hệ thống content (việc chính hằng tháng)

### 6.1 Ghép skill theo lớp

```
seo-outline / seo-article-writer   (quy trình chung)
   + core/formats/<loại bài>.md     cấu trúc, độ dài, thành phần bắt buộc, schema
   + core/industries/<ngành>.md     E-E-A-T, thuật ngữ, góc nhìn người mua, YMYL
   + core/markets/<locale>.md       chính tả, giọng địa phương, SERP location, domain loại trừ
   + project/brand/*                voice, facts, rules, internal links, disclaimer
   + project/overrides/*            ngoại lệ riêng của dự án
```

Thứ tự ưu tiên khi các lớp mâu thuẫn: **brand > overrides > format > industry > market > core**. Mỗi lần áp dụng thứ tự này, skill ghi lý do vào handoff note.

### 6.2 Vòng content hằng tháng (điều khiển bằng cột Status trong Sheet)

```
/content-month 2026-12
  1. Đọc Masterfile › Content Plan: các dòng Month = 2026-12 và Status = Planned
  2. Mỗi bài: /outline → content/2026-12/<slug>/outline.md
              → Google Doc "Outline – <title>" trong Drive/03. Content/2026-12
              → Sheet: Status = Outline Ready, gắn link Doc
  3. PIC/SEN duyệt (comment trên Doc) → đổi Status = Outline Approved
  4. /write <ID>: đọc comment → draft.md → content-lint (tự động) → content-reviewer (agent)
              → draft.html theo format → Doc → Status = Draft Ready
  5. SEN duyệt → khách duyệt → đăng bài → điền URL → Status = Published
  6. Sau 7 và 28 ngày: /health-check kiểm tra index, impressions, vị trí, AI mention
```

Status chuẩn: `Planned → Outline Ready → Outline Approved → Draft Ready → SEN Approved → Client Approved → Published → Monitoring`.

### 6.3 Nâng cấp 2 skill hiện có (đánh giá cụ thể)

**`seo-outline`**

1. Skill đọc brand từ "Claude Project". Cần chuyển sang đọc `project/brand/*` và `config.yaml`.
2. Danh sách domain bị loại khi phân tích đối thủ (báo VN, OTA, sàn TMĐT) đang viết cứng. Danh sách này phải đổi theo ngành và thị trường: với khách hotel, OTA là đối thủ thật trên SERP. Với khách B2B như CWG, cần loại các marketplace như Alibaba. Cần chuyển danh sách vào `core/markets/` và `core/industries/`.
3. Độ dài cố định 1,200–1,500 từ đang xung đột với brand CWG (buyer guide 1,000–1,800 từ, news 150–300 từ). Độ dài nên lấy theo format và brand.
4. Năm "2026–2027" đang viết cứng. Nên tính theo ngày chạy.
5. Thiếu dữ liệu keyword (volume, KD, secondary keyword từ DataforSEO) và thiếu liên kết với dòng Content Plan (ID, cluster, problem pattern, prompt cần trả lời).
6. **Thiếu phần GEO:** mỗi H2 cần một câu trả lời trực tiếp (answer chunk), danh sách entity phải nêu, dữ kiện riêng của brand lấy từ `facts.yaml` để AI có lý do trích dẫn, các prompt AI mà bài cần trả lời, và nguồn đang được AI Overview trích dẫn.
7. Output hiện chỉ nằm trong chat. Cần ghi ra file, đẩy sang Google Doc và cập nhật Sheet.
8. Internal link mới chỉ ở mức "gợi ý". Nên lấy URL thật từ `internal-links.csv`, file được tạo bằng cách crawl sitemap.

**`seo-article-writer`**

1. `/mnt/user-data/outputs` và `present_files` là của claude.ai, không có trong Claude Code. Cần đổi sang ghi vào `content/…`.
2. Số từ cho FAQ không thống nhất (Step 2 ghi 50–75 từ, template ghi 35–50 từ). Nên lấy theo format.
3. Các quy tắc cứng (cấm em dash, cấm dấu chấm phẩy, cấm cliché, từ cấm của brand) đang dựa vào việc Claude tự kiểm. Nên chuyển thành script `content_lint.py` chạy tự động qua hook mỗi khi file content được ghi.
4. Chưa có bước đối chiếu số liệu. Cần thêm bước so với `facts.yaml`: số không có trong fact sheet sẽ bị gắn `[VERIFY]`, và mục đang ở trạng thái "⚠ Verify" (ví dụ ISO 14001, GOTS, tỉnh Nam Dinh/Ninh Binh của CWG) bị chặn không cho viết.
5. Chưa tự chèn disclaimer theo loại nội dung, trong khi brand CWG mục 7.2 bắt buộc. Cần đọc từ `rules.yaml`.
6. Chưa xuất HTML và schema (Article, FAQPage, BreadcrumbList). Việc này giao cho `blog-html-formatter`.
7. Nên thêm một lượt line-edit cuối bằng skill org `ai-writing-tells` và `natural-english-writing` / `natural-vietnamese-writing`, rồi để agent `content-reviewer` chấm điểm trước khi chuyển SEN.

### 6.4 Kiểm tra tự động (hooks)

- `content_lint.py` chạy sau mỗi lần Claude ghi file trong `content/`. Script kiểm: em dash, dấu chấm phẩy, cliché, từ cấm của brand (ví dụ "state-of-the-art", "world-class", "eco-friendly"), chính tả Anh/Mỹ, định dạng số (5,000 chứ không phải 5.000), số internal link tối thiểu, có CTA, có disclaimer, số liệu không có trong facts.
- Bài chưa qua lint thì không được chuyển sang Status "Draft Ready".

### 6.5 Định dạng HTML cho blog

- Mỗi format có một template HTML gồm các thành phần: key takeaways/TL;DR, mục lục, bảng thông số, callout, FAQ dạng accordion kèm FAQPage JSON-LD, CTA box, author box với "Reviewed by" và "Last reviewed".
- Style dùng biến (màu, font, bo góc) lấy từ `project/brand/` để khớp giao diện site. CSS viết inline hoặc theo class tùy CMS.
- Trước khi giao, Claude chụp preview bằng trình duyệt headless (desktop + mobile) để kiểm tra hiển thị.
- Cần bạn gửi 1–2 mẫu HTML đang dùng (xem câu hỏi D2).

### 6.6 Dịch content

- Tái sử dụng skill org `translate-html`. Thêm `glossary.csv` (thuật ngữ không dịch, tên brand, tên nhà máy) và một bản đồ internal link riêng cho từng ngôn ngữ.
- Sau khi dịch, chạy lint theo quy tắc của thị trường đích.

---

## 7. Research, Plan & Forecast

### 7.1 Nguồn dữ liệu

| Việc | Nguồn chính | Nguồn phụ |
| --- | --- | --- |
| Volume, KD, CPC, intent, related keywords | DataforSEO (Keywords Data, DataforSEO Labs) | SE Ranking |
| SERP top 10, PAA, AI Overview | SERP API | DataforSEO SERP |
| Đọc nội dung trang đối thủ | Firecrawl | Trình duyệt headless |
| Domain đối thủ: ranked keywords, keyword gap, backlinks | DataforSEO Labs + Backlinks | SE Ranking |
| GSC/GA4 lịch sử | Agency Analytics | — |
| AI visibility (prompt, mention, citation) | Cần chốt công cụ (câu hỏi C3) | DataforSEO AI Optimization / SE Ranking |
| Dữ liệu ngành | File team cung cấp trong `project/research/` | Nguồn chính thống có tên và năm |

### 7.2 Forecast traffic (trong SEO/GEO Plan)

Forecast do `scripts/forecast.py` tính, Claude chỉ viết phần diễn giải và các giả định.

1. **Baseline:** lấy 16 tháng GSC (clicks, impressions) và GA4 (organic sessions, conversions) qua Agency Analytics, tách mùa vụ và xu hướng.
2. **Uplift từ dưới lên:** với mỗi cluster trong Content Plan, uplift = volume × CTR ở vị trí mục tiêu × hệ số ramp-up theo tháng kể từ khi đăng. CTR lấy từ chính GSC của site nếu đủ dữ liệu, nếu không thì dùng đường CTR chuẩn.
3. **3 kịch bản:** Conservative / Base / Aggressive, khác nhau ở vị trí mục tiêu và tốc độ ramp-up.
4. **Conversion:** organic sessions × tỷ lệ chuyển đổi organic lịch sử = leads/bookings dự kiến.
5. **Output:** tab Forecast (theo tháng × kịch bản) + biểu đồ + bảng giả định. Mọi giả định đều sửa được ngay trong Sheet.

Cần bạn gửi mẫu forecast đang dùng để khớp format (câu hỏi E3).

---

## 8. Technical, Tracking và UI/UX

### 8.1 Đưa source website lên repo

| Nền tảng | Cách lấy | Claude làm được gì |
| --- | --- | --- |
| Custom (Next.js, Laravel, …) | Git submodule hoặc copy vào `website/` | Audit code + **tạo patch/PR** cho dev |
| WordPress | Theme + plugin list (không lấy `wp-content/uploads`, `wp-config.php`). Nội dung lấy qua WP REST API hoặc crawl | Audit template, schema, head tags, plugin SEO. Đề xuất thay đổi theo từng file |
| Shopify | Theme qua Shopify CLI | Audit Liquid template |
| Webflow / Wix | Không có source, chỉ crawl | Audit dựa trên HTML render |

**Bảo mật:** dùng `.gitignore` mẫu theo từng nền tảng và quét secret (gitleaks) trước khi commit. Source chỉ đưa lên khi hợp đồng/NDA cho phép (câu hỏi D1).

### 8.2 Technical audit kết hợp 3 nguồn

1. **Crawl:** Firecrawl map/crawl, hoặc script crawl bằng trình duyệt headless cho site render bằng JS. Nếu team có Screaming Frog thì upload CSV export.
2. **Source:** head tags, canonical, hreflang, robots, sitemap, schema, lazy-load, script chặn render, định dạng ảnh, phân trang.
3. **Hiệu năng:** PageSpeed Insights API hoặc Lighthouse chạy trực tiếp trong môi trường (Chromium có sẵn).

Output là Sheet Technical Audit với các cột: Issue · Severity · Affected URLs · Evidence · Fix · Owner · Status. Với site có source thì kèm patch.

### 8.3 Google Tag Manager (chưa có connector)

1. Phân tích site và source để liệt kê các điểm chuyển đổi: form, click tel/mailto/WhatsApp/Zalo, click booking engine, tải PDF (ví dụ company profile của CWG), outbound link, scroll, CTA.
2. Viết tracking plan vào tab Tracking Plan: tên event, trigger, parameter, có phải key event không.
3. Sinh **file container JSON** (tag, trigger, variable) để PIC import vào GTM bằng Admin › Import Container › **Merge** vào một workspace mới. Claude không tự publish container.
4. Kiểm tra bằng trình duyệt headless: mở trang, thực hiện hành động, bắt request gửi về GA4 (`/g/collect`) để đối chiếu tên event và parameter. Với booking engine thì kiểm thêm cross-domain.

### 8.4 UI/UX audit

- Chụp screenshot desktop và mobile cho từng loại template trang (home, service/product, blog, contact, booking).
- Đánh giá theo heuristic UX + CRO + 2 rule GEO infrastructure (dùng lại skill `geo-infra-audit`).
- Output: báo cáo có chú thích trên ảnh, kèm đề xuất theo mức ưu tiên. Hiện chưa có Figma connector, nên ở v1 designer sẽ đưa ảnh và chú thích lên Figma. Nếu có Figma MCP, Claude có thể đọc file Figma để so sánh với thiết kế đề xuất (câu hỏi D3).

---

## 9. Monitoring và Reporting

### 9.1 Bộ lọc hỏi đáp Agency Analytics

```
/analytics week                          # tuần trước so với tuần trước nữa
/analytics month 2026-10 vs yoy          # tháng 10 so với cùng kỳ năm ngoái
/analytics last-28d group=insights       # theo nhóm trang khai báo trong config
/analytics month query=non-branded       # tách branded/non-branded bằng regex trong config
/analytics quarter country=IT device=mobile
```

- Mỗi lần chạy lưu snapshot vào `data/analytics/` để so sánh các kỳ mà không phải gọi lại API.
- Sau khi có bảng số, bạn hỏi tự do, ví dụ "Vì sao clicks nhóm insights giảm?" hoặc "Top 10 trang tăng mạnh nhất?".
- Giai đoạn sau có thể thêm một dashboard HTML có bộ lọc tuần/tháng.

### 9.2 Weekly Health Check tự động (P06a)

- Dùng scheduled task của Claude Code, chạy sáng thứ Hai cho từng dự án (GitHub Actions không dùng được các connector của claude.ai nên không phù hợp).
- Kiểm tra:
  - clicks, sessions và conversions giảm vượt ngưỡng
  - trang top bị rơi hạng
  - 404/5xx mới từ crawl mẫu
  - bài mới đã được index chưa
  - robots.txt và sitemap có thay đổi
  - prompt GEO bị mất mention
- Ghi một dòng vào tab Weekly Health Check và gắn cờ cho PIC. Nếu tích hợp Asana thì cập nhật luôn task (câu hỏi A4).

### 9.3 Báo cáo tháng và báo cáo executive

- Số liệu lấy từ script, Claude viết phần insight, nguyên nhân và kế hoạch tháng sau.
- Báo cáo executive ngắn gọn, tập trung vào lead/booking và AI visibility.

### 9.4 Cây chẩn đoán (đi theo đúng sơ đồ P06)

- **Path 1, content kém:** chưa index → sửa lỗi kỹ thuật. Đã index nhưng không có giá trị → quay lại content research → intent có khớp không → brief lệch trend? → kiểm tra brand fit và nội dung người dùng cảm nhận → vẫn không cải thiện → quay lại phân tích onboarding.
- **Path 2, mọi thứ ổn nhưng hiệu quả yếu:** nghi lỗi kỹ thuật → full-site technical audit (UX/UI, tốc độ trang).
- **Path 3, kỹ thuật cũng ổn:** kiểm tra giao diện và CTA → chuyển sang P07a.
- **GEO P06e:** chỉ số kém → tìm GEO gap so với đối thủ (dựa trên research P03) → thêm phần còn thiếu vào nội dung site.
- **GEO P06f:** mention sai hoặc tiêu cực → tìm nguồn → sửa thông tin chính thức trên site → khi ổn định thì chuyển sang P07b.

Mỗi node trong cây ghi rõ dữ liệu cần kiểm và công cụ dùng, nên PIC nào chạy cũng ra cùng một logic.

---

## 10. Bảo mật, chi phí, vận hành

- Repo dự án để private, phân quyền theo pod. Không commit file chứa thông tin cá nhân (PII) hoặc credential.
- Credential của API gọi trực tiếp (PageSpeed, DataforSEO nếu không qua connector) lưu dưới dạng secret của environment, không đặt trong repo.
- Chi phí API: cache kết quả SERP và keyword trong `data/cache/` có thời hạn, và đặt ngân sách mỗi dự án trong `config.yaml`.
- Nếu gọi API trực tiếp thì cần mở host tương ứng trong network policy của môi trường cloud.
- Claude chỉ ghi vào bản nháp hoặc Status đang chờ duyệt, không gửi gì trực tiếp cho khách.
- `validate_project.py` kiểm tra config, ID file trên Drive và quyền truy cập connector trước khi chạy bất kỳ skill nào.

---

## 11. Lộ trình triển khai

Thời gian dưới đây là ước tính, sẽ chỉnh sau khi có câu trả lời ở Mục 12.

| Phase | Nội dung | Kết quả nghiệm thu |
| --- | --- | --- |
| **0. Chốt và thử connector** (2–3 ngày) | Trả lời câu hỏi, bật công cụ Drive, gửi Sheet mẫu. Chạy thử từng connector và ghi lại khả năng, giới hạn vào `docs/connectors.md` | Bảng năng lực connector. Kiến trúc được chốt |
| **1. Khung template** (tuần 1) | CLAUDE.md, cấu trúc thư mục, schema config + validator, `/new-project` (chuyển brand guideline thành brand pack), sync-core, .gitignore, quét secret. Tạo repo CWG làm pilot | Tạo dự án mới trong ≤ 30 phút. Claude trả lời đúng các fact của CWG và từ chối các mục "⚠ Verify" |
| **2. Content engine** (tuần 2–3) | Nâng cấp outline + writer, 5–6 format, 2 ngành pilot, các thị trường chính, content-lint hook, HTML formatter, dịch, `/content-month` chạy theo Sheet + Docs | 3 bài CWG đi trọn từ dòng Content Plan đến HTML, 0 lỗi lint, SEN chấm đạt |
| **3. Research và Plan** (tuần 3–5) | Keyword, đối thủ/thị trường, category và problem pattern, bộ prompt, Content Plan, `forecast.py`, dựng Plan vào Sheet mẫu, sửa theo comment, Plan → Masterfile | Plan CWG đủ tab. SEN chỉ phải sửa ≤ 20% |
| **4. Technical, Tracking, UI/UX** (tuần 5–6) | Đưa source lên, tech audit 3 nguồn, on-page, GTM plan/build/verify, UI/UX audit | Audit CWG + container GTM import được và kiểm tra đạt |
| **5. Monitoring, Report, GEO** (tuần 6–7) | `/analytics`, health check tự động hằng tuần, báo cáo tháng/executive, cây chẩn đoán, GEO visibility/gap/mentions, off-page/GBP | Báo cáo tháng CWG tự động. Health check chạy đúng lịch |
| **6. CRO, Handover, Rollout** (tuần 8+) | P07, `/handover`, tài liệu và đào tạo team, chuyển plugin (v2), áp dụng cho các dự án khác | 2–3 dự án khác chạy trên template |

---

## 12. Câu hỏi cần chốt trước khi bắt đầu

Danh sách đầy đủ có trong tin nhắn trả lời kèm theo file này. Các câu ★ là câu đang chặn Phase 0–1.

**A. Kiến trúc và vận hành**
- ★A1. Đồng ý mô hình template repo + repo riêng cho từng khách (`talabadao/seo-<slug>`), cập nhật bằng sync-core ở v1 và chuyển sang plugin ở v2?
- ★A2. Bao nhiêu người sẽ dùng (PIC/JR/INT)? Mọi người chạy Claude Code trên web (claude.ai/code), app desktop hay CLI? Org đang dùng gói Claude nào?
- A3. Đồng ý Sheets là nơi lưu chính cho Plan/Tracker, Git là nơi lưu chính cho skill, bản nháp và audit?
- A4. Có cần tích hợp Asana (tự cập nhật status task) không?

**B. Google Drive**
- ★B1. Bạn bật được các công cụ tìm, đọc, tạo và upload của Google Drive connector không? Trong lúc chờ, bạn gửi link trực tiếp 2 Sheet SEO/GEO Plan và Masterfile của 1–2 dự án mẫu (Sheets connector đang chạy được).
- B2. Đã có folder template trống trên Drive chưa, hay dựng từ dự án tốt nhất? Folder dự án mới nên do Claude tạo tự động hay AM/PM copy tay?
- B3. Onboarding form đang ở dạng nào (Google Form → Sheet hay Doc)? Gửi 1 mẫu.

**C. Dữ liệu và connector**
- ★C1. Connector "SEO Data" có phải DataforSEO không? SE Ranking dùng cho việc gì? Volume/KD lấy từ nguồn nào là chuẩn? Ngân sách API mỗi dự án mỗi tháng?
- C2. Tất cả khách đã kết nối GA4 + GSC vào Agency Analytics chưa? Rank tracking lấy từ Agency Analytics hay SE Ranking?
- C3. Hiện đo AI visibility bằng công cụ nào (file "ChatGPT Mentions – Full report" xuất từ đâu)?
- C4. GTM: dùng cách Claude sinh file JSON để PIC import là được, hay muốn gọi thẳng GTM API?

**D. Website và content**
- ★D1. Khách chủ yếu dùng nền tảng nào (WordPress/Shopify/Webflow/custom)? Lấy source bằng cách nào? Claude chỉ đề xuất hay được tạo patch/PR cho dev? Hợp đồng có cho phép đưa source lên GitHub không?
- D2. Bài được đăng thế nào (HTML dán vào Custom HTML block, Gutenberg, Elementor…)? Claude chỉ giao file hay đăng nháp thẳng qua WP REST API? Gửi 1–2 mẫu HTML blog đang dùng.
- D3. Figma: có Figma MCP không, và mẫu UI/UX audit mong muốn trông thế nào?
- D4. Các skill org đã có (category-definer, problem-pattern-identifier, geo-infra-audit, ai-writing-tells, translate-html…): đưa vào repo để quản lý version, hay giữ ở claude.ai và chỉ gọi tới?
- D5. Ngành nào và loại bài nào phổ biến nhất để ưu tiên viết format/playbook trước? Những ngôn ngữ nào hay phải dịch?

**E. Pilot và cổng duyệt**
- ★E1. Pilot với CWG được không? Đã có source website, campaign Agency Analytics và file Drive của CWG chưa?
- E2. Output nào bắt buộc SEN duyệt? Claude được ghi thẳng vào Sheet/Doc khách đang xem, hay chỉ ghi vào bản nháp nội bộ?
- E3. Forecast hiện làm theo phương pháp nào, cho 6 hay 12 tháng? Gửi 1 mẫu.

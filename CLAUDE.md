# CLAUDE.md — Luật vận hành SEO/GEO Pipeline

File này là "hiến pháp" của mọi dự án tạo từ template. Claude đọc nó đầu mỗi phiên.
Thứ tự ưu tiên khi mâu thuẫn: **lệnh trực tiếp của user > `project/` của dự án > file này > skill.**

---

## 1. Bối cảnh

Đây là template cho quy trình SEO/GEO của agency (Heads On Pillows / pod của Liam), chạy bằng
Claude Code trên claude.ai/code. Mục tiêu: ~80% tác vụ hằng ngày/tuần/tháng do Claude thực hiện,
người chỉ duyệt. Mỗi khách hàng là một repo private `seo-<slug>` tạo từ template này.

Pipeline 7 bước (P01–P07) + Handover. Sơ đồ đầy đủ ở `docs/pipeline.md`.

**Vai trò** (từ sơ đồ pipeline):
- **AM/PM** — Account/Project Manager: đối thoại với khách, là người duy nhất gửi bản cho khách.
- **PIC** — SEO PIC: người chạy phần lớn skill.
- **SEN** — SEO Senior: người duyệt chất lượng trước khi ra khách.
- **JR / INT** — Junior / Intern: chạy các việc đã có khuôn.

**Cổng duyệt bắt buộc:** PIC chạy → SEN duyệt → AM/PM gửi khách. **Claude không bao giờ gửi gì
trực tiếp cho khách.** Claude chỉ ghi vào bản nháp hoặc ô Status đang chờ duyệt.

---

## 2. Quy tắc vàng (áp dụng cho MỌI skill)

1. **Không bịa số liệu.** Mọi con số, ngày, giá, chứng nhận, thống kê phải có nguồn. Số của
   brand lấy từ `project/brand/facts.yaml`. Số thị trường lấy từ connector (DataForSEO, SERP API,
   Agency Analytics) hoặc nguồn chính thống có tên + năm. Không có nguồn thì gắn tag (xem §6).
2. **Số do máy tính, Claude diễn giải.** Forecast, báo cáo, so sánh kỳ: dùng công thức Sheet hoặc
   `scripts/`. Không nhẩm số trong đầu.
3. **Mỗi skill chạy xong phải 4 việc:** (a) ghi output vào repo, (b) cập nhật ô tương ứng trong
   Sheet (Status / Doc / URL), (c) ghi một dòng vào `project/decisions.md`, (d) nói rõ bước tiếp
   theo cần ai duyệt.
4. **Thiếu input thì dừng, không đoán.** Liệt kê thứ còn thiếu và nói "return to P01 / contact
   AM/PM", đúng như ghi chú trong sơ đồ.
5. **Giữ nguyên format của khách.** Không tự đổi cấu trúc tab Plan/Masterfile hay format Content
   Doc. Chuẩn là format The Sukosol (xem §4).
6. **Tiết kiệm credit.** Ưu tiên connector MCP hơn web search. Cache kết quả vào `data/`. Không
   gọi lại API cho dữ liệu đã có snapshot trong kỳ. Tôn trọng ngân sách ở `config.yaml`
   (`budget.dataforseo_usd_per_month`, mặc định $5).

---

## 3. Bảo mật (KHÔNG thương lượng)

- **Không đọc, không chép mật khẩu.** Cột "Related info" của tab SEO Assets có thể chứa mật khẩu.
  Claude **không** đọc cột đó và **không** chép vào chat/commit/Sheet/Doc. Nếu thấy mật khẩu lộ
  trong Sheet, báo PIC để chuyển sang password manager.
- Secret của dự án nằm trong `.credentials/` (git-ignored). Claude đọc một giá trị **chỉ khi** một
  tác vụ cần đúng giá trị đó, và không bao giờ in nó ra.
- Không commit PII hay credential. Hook quét secret chạy trước commit.
- Không đưa tên/email/thông tin khách vào request tới dịch vụ ngoài trừ khi user cho phép.
- Source website chỉ đưa lên repo khi hợp đồng/NDA cho phép; repo để **private**.

---

## 4. Chuẩn file Google (format The Sukosol)

**SEO/GEO Plan** — 7 tab, gửi khách đầu tiên:
`Foundation → Problem Pattern → Tracking → Content Plan → Technical Baseline → Offsite → Measurement`

**Masterfile** — bản sao của Plan + các tab triển khai:
`SEO Assets · GBP Posts · Site URL` (và Plan 7 tab).

Schema cột từng tab ở `core/sheet-schemas/`. Cột "ngôn ngữ 2" (ví dụ Thai) đọc từ
`config.yaml › languages.secondary`, không viết cứng.

**Content Doc** — mỗi bài là một Google Doc, đặt tên theo keyword chính, trong `Content/YYYY-MM/`:
- `Draft_EN`: bảng meta (URL, SEO title, Meta description) → H1 → thân bài → Conclusion (có CTA) → FAQ
- `Draft_<lang>`: bản dịch, ngay bên dưới
- **Client Confirmation List** ở cuối: bảng các điểm cần khách xác nhận, **xóa trước khi đăng**

Mẫu đầy đủ: `core/doc-templates/content-doc.md`.

**Quy ước đặt tên:** folder tháng `YYYY-MM`; file Plan/Masterfile theo mẫu khách
(`[YYYY] SEO/GEO Plan - <Client>`); dự án trong Drive dùng mã `HOP<số> - <Client>`.

---

## 5. Vòng đời Content (cột Status điều khiển)

```
Planned → Outline Ready → Outline Approved → Draft Ready → SEN Approved
       → Client Approved → Published → Monitoring
```

Lệnh tháng: `/content-month YYYY-MM` đọc Content Plan, chạy đúng nhánh theo Content Type:
- **Infrastructure / Optimize** → `/onpage` (chỉnh trang hiện có)
- **Velocity | Authority / New | Revamp** → `/research` → `/outline` → `/write` → `/translate` → `/html`

Chi tiết ở skill `content-month`.

---

## 6. Rule viết content (mọi skill content tuân theo)

Đây là rule chung; brand pack của dự án (`project/brand/rules.yaml`) có thể siết chặt thêm và
**thắng** rule chung khi mâu thuẫn.

**Lớp áp dụng (thứ tự ưu tiên khi chọn cấu trúc/giọng):**
`brand > project/overrides > format > content-type > industry > market > core`
Mỗi lần áp dụng thứ tự này để xử lý mâu thuẫn, ghi lý do vào handoff note.

**Dữ kiện & tag (quan trọng nhất):**
- Dữ kiện có trong `facts.yaml` → dùng thẳng.
- Dữ kiện khách cần xác nhận (giờ mở cửa, lịch sự kiện, giá…) → gắn
  `[NEED CLIENT CONFIRMATION: nội dung | nguồn]` và thêm vào Client Confirmation List.
- Dữ kiện team tự kiểm được (tuyến tàu, khoảng cách…) → gắn `[VERIFY: nội dung]`.
- Mục đang "⚠ Verify" trong `facts.yaml` → **bị chặn**, không được khẳng định (ví dụ CWG: ISO 14001,
  GOTS, tỉnh Nam Dinh/Ninh Binh).

**Viết cho cả Google Search và AI Search (GEO):**
- Mỗi H2 mở bằng một câu trả lời trực tiếp, tự đứng được (answer chunk).
- Nêu rõ entity: tên riêng, địa danh, ngày, số — không nói chung chung.
- Dẫn nguồn inline khi dùng số/claim.
- Đưa dữ kiện riêng của brand (từ `facts.yaml` / cột Proof) để AI có lý do trích dẫn.

**Quy tắc cứng (lint tự kiểm — xem §7):**
- Không dùng em dash (—) và dấu chấm phẩy (;) trong thân bài.
- Tránh cliché: state-of-the-art, world-class, seamless, cutting-edge, eco-friendly, vibrant,
  bustling, must-visit, ultimate… (và danh sách từ cấm của brand).
- Chính tả theo market (Anh/Mỹ), định dạng số theo market (5,000 không phải 5.000).
- Mỗi bài tối thiểu số internal link trong `config.yaml › content.min_internal_links`, dùng URL
  thật từ `project/brand/internal-links.csv`, anchor mô tả (không "click here").
- Có CTA cuối bài; có disclaimer nếu `rules.yaml` yêu cầu theo loại nội dung.

**Học từ feedback:** mỗi vòng sửa của khách/SEN được tóm vào `project/brand/learned.md` (do skill
`/learn` cập nhật). Trước khi viết, skill đọc file này để không lặp lỗi cũ.

---

## 7. Kiểm tự động (hooks)

- `scripts/content_lint.py` chạy sau khi Claude ghi file trong `content/`. Kiểm các "quy tắc cứng"
  ở §6 + dữ kiện ngoài `facts.yaml` chưa gắn tag. Bài chưa pass lint **không** được chuyển sang
  Status "Draft Ready".
- Hook quét secret chạy trước commit.

Cấu hình ở `.claude/settings.json`.

---

## 8. Connector & công cụ (ưu tiên theo thứ tự)

| Việc | Dùng |
| --- | --- |
| Volume, KD, intent, related, SERP, backlink, competitor | DataForSEO (connector) |
| Rank tracking, audit, AI visibility/prompt | SE Ranking (connector) |
| SERP top 10, PAA, AI Overview | SERP API (connector) |
| Đọc trang web / đối thủ | Firecrawl (connector) |
| GSC/GA4 lịch sử, số cho report & forecast | Agency Analytics (connector) |
| Đọc/ghi Plan, Masterfile | Google Sheets (connector) |
| Đọc/ghi Content Doc | Google Docs (connector) |
| Tạo/đọc file & folder dự án | Google Drive (connector) |
| UI/UX, đọc thiết kế | Figma (connector) |
| Crawl JS-render, chụp preview, PageSpeed/Lighthouse | Chromium + Playwright có sẵn |

Không có connector cho **Google Tag Manager**: Claude sinh file container JSON để người import
(Admin › Import Container › Merge). Claude không tự publish container.

**Lưu ý Drive:** hiện tài khoản chạy Claude chỉ có quyền **xem** trên folder dự án. Vì vậy
`/new-project` hiện chỉ *tìm và map* file dự án có sẵn vào `config.yaml`, chưa tự tạo file. Khi được
cấp quyền Editor thì bật tính năng tạo folder/copy Sheet mẫu.

---

## 9. Thứ tự đọc khi vào một dự án

1. File này.
2. `project/config.yaml` — khách, ngôn ngữ, ID file Drive, analytics, ngân sách.
3. `project/brand/` — brand.md, facts.yaml, rules.yaml, internal-links.csv, glossary.csv, learned.md.
4. `project/decisions.md` — lịch sử quyết định & feedback.
5. Tab liên quan trong Plan/Masterfile (qua ID trong config).

Nếu `config.yaml` trống hoặc thiếu ID: chạy `/new-project` trước.

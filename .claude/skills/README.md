# .claude/skills — danh mục lệnh

Mỗi thư mục là một skill (SKILL.md). Phase 1 đã dựng các skill content cốt lõi; các skill còn lại
(P02–P07) sẽ bổ sung ở Phase 3–5 theo lộ trình `docs/implementation-plan.md`.

## Đã có (Phase 1)
| Lệnh | Việc |
| --- | --- |
| `/new-project` | Tìm + map file Drive của khách, dựng config + brand pack nháp |
| `/research` | Nghiên cứu SERP/keyword/đối thủ/GEO cho một bài → research.md (cache) |
| `/outline` | Tạo outline SEO/GEO từ research + brand + format (không viết bài) |
| `/write` | Viết bài → Content Doc (Draft_EN + Confirmation List), lint + review |
| `/translate` | Dịch tự nhiên EN → ngôn ngữ đích, giữ cấu trúc, đổi internal link |
| `/content-month` | Điều phối cả tháng theo Content Plan + cổng duyệt |
| `/learn` | Ghi bài học từ feedback khách/SEN vào brand pack |

## Subagent (.claude/agents)
`serp-researcher` · `competitor-analyst` · `content-reviewer` · `tech-auditor`

## Sẽ bổ sung
- P02: `/p02-access` — P03: `/p03-foundation`, `/p03-market` — P04: `/p04a-patterns`,
  `/p04b-tracking`, `/p04c-content-plan`, `/p04d-tech-baseline`, `/p04e-offsite`, `/forecast`,
  `/p04e-review`, `/p04-to-masterfile`
- P05: `/onpage`, `/tech-audit`, `/tech-fix`, `/html`, `/gbp-posts`, `/offpage-plan`, `/gtm-plan`,
  `/gtm-build`, `/gtm-verify`, `/llms-txt`, `/site-inventory`, `/uiux-audit`
- P06–P07: `/analytics`, `/health-check`, `/report`, `/diagnose`, `/geo-visibility`, `/geo-gap`,
  `/geo-fix-mentions`, `/cro-audit`, `/geo-expand`, `/meeting-prep`, `/handover`

Mapping đầy đủ: `docs/pipeline.md`.

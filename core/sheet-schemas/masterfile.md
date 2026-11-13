# Schema — SEO/GEO Masterfile

Masterfile = bản sao của Plan (7 tab) + các tab triển khai. Đồng bộ từ Plan bằng /p04-to-masterfile.

## Tab SEO Assets  (P02, skill /p02-access)
`No. | Assessment | Detail | Status | Related info.`
- Mỗi dòng một hạng mục truy cập: CMS Login, GBP, Google Analytics, GSC, SE Ranking, Agency
  Analytics, SEO Report...
- Status = TRUE/FALSE (đã có quyền hay chưa).
- ⚠ **Related info.**: KHÔNG lưu mật khẩu ở đây. Claude không đọc/không chép cột này. Nếu thấy
  mật khẩu, flag để chuyển sang password manager (CLAUDE.md §3).

## Tab GBP Posts  (P05, skill /gbp-posts)
`Month | Page/Blog | Doc | Status`  — lịch 4 post/tháng, link Doc nội dung GBP.

## Tab Site URL  (P05, skill /site-inventory)
Danh sách URL của site (crawl sitemap). Dùng để lập internal-links.csv và map Matched URL.

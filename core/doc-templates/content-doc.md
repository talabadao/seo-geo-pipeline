# Khuôn Content Doc (chuẩn The Sukosol)

Mỗi bài = một Google Doc, tên = keyword chính, trong `Content/YYYY-MM/`. Gồm `Draft_EN`, rồi
`Draft_<lang>` nếu có ngôn ngữ 2, và **Client Confirmation List** ở cuối (xóa trước khi đăng).

---

```
# Draft_EN

| URL (hoặc URL revamp) | https://domain.com/path/ |
| SEO title             | <= 60 ký tự, keyword gần đầu |
| Meta description      | 140–160 ký tự, có keyword + value + CTA mềm |

# <H1 — tiêu đề bài>

<Intro 100–150 từ: mở bằng tình huống/câu hỏi của người đọc, không mở bằng keyword.
Nói bài giúp người đọc quyết định/hiểu/làm được gì.>

## <H2 — câu hỏi thật của người đọc>
<Câu đầu = trả lời trực tiếp (answer chunk). Sau đó triển khai. Bảng/list theo format.
Link nội bộ bằng anchor mô tả. Dữ kiện có nguồn; chưa chắc thì gắn tag.>

### <H3 nếu H2 đủ rộng>

[... các H2 khác ...]

## Conclusion
<80–120 từ, chốt takeaway thực dụng, kết bằng CTA trỏ tới trang Infrastructure.>

## Frequently Asked Questions
### <Câu hỏi đúng như người đọc hỏi>?
<35–75 từ, tự đứng được như một đoạn AI trích. 5–7 câu.>

<!-- REVIEW APPENDIX: xóa hết phần dưới trước khi đăng -->

## Client Confirmation List (xóa trước khi đăng)
| # | Section | Câu hỏi cho khách |
| 1 | <mục> | <điều cần khách xác nhận, kèm nguồn/năm của dữ kiện cũ> |

# Draft_<lang>
<bản dịch tự nhiên, cùng cấu trúc; link nội bộ đổi sang path ngôn ngữ đó>
```

---

## Quy ước tag trong bài
- `[NEED CLIENT CONFIRMATION: nội dung | nguồn]` — dữ kiện cần khách xác nhận (giờ mở cửa, giá,
  lịch sự kiện). Mỗi tag → một dòng trong Client Confirmation List.
- `[VERIFY: nội dung]` — dữ kiện team tự kiểm được (tuyến tàu, khoảng cách, link chính thức).
- `[STAT NEEDED: ...]` — chỗ cần số mà chưa có nguồn; không được tự bịa.

## Số từ
Lấy theo format (`core/formats/`) và `config.yaml › content.word_range`, không cố định cứng.

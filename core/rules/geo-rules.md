# Rule GEO (tối ưu cho AI Search: Perplexity, ChatGPT Search, Google AI Overviews, Claude)

## Answer chunk
- Mỗi H2 mở bằng 1–2 câu trả lời trực tiếp, tự đứng được khi bị trích rời ngữ cảnh.
- Định nghĩa/kết luận đặt đầu, giải thích sau.

## Entity & citation
- Nêu entity rõ: tên riêng, địa danh, ngày, số. Không "soon", "the hotel", "it".
- Dẫn nguồn inline cho số/claim ("according to <nguồn> <năm>").
- Đưa dữ kiện riêng của brand (facts.yaml / cột Proof) để AI có lý do trích brand.

## Bảng & list
- Bảng tiêu chí/so sánh/khoảng cách: cell ngắn, dễ AI trích và dễ đọc mobile.

## Prompt coverage
- Mỗi bài Velocity bám ≥ 1 prompt trong tab Tracking + ≥ 1 Problem Pattern.
- Khi làm GEO gap (P06e): đối chiếu câu trả lời AI hiện tại vs đối thủ, bổ sung phần site thiếu.

## llms.txt
- Dùng skill llms-txt khi hợp: liệt kê fact brand (NAP, hạng, check-in/out) + link trang canonical.

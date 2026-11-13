# Format: Room / Product Page  (Infrastructure)

Intent: Transactional. Một phòng/sản phẩm cụ thể.

## Cấu trúc
- H1: tên phòng/sản phẩm
- Mô tả: kích thước, sức chứa, cấu hình giường/thông số, ai hợp (ICP)
- Bảng thông số; tiện nghi/đặc tính (list); bằng chứng/review; ảnh có alt
- CTA đặt/kiểm phòng trống; link phòng/sản phẩm liên quan + hub

## Schema: HotelRoom + Offer (hoặc Product + Offer), containedInPlace → #hotel.
## Must: thông số thật từ facts.yaml; một H1; giá gắn tag nếu biến động.
## Pitfalls: đồng bộ tên phòng giữa các trang; không khẳng định sức chứa/giá sai.

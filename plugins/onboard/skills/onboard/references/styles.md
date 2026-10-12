# Phong cách và bố cục

## Phong cách (`style`)

Chỉ đổi vẻ ngoài. Màu ngữ nghĩa (xanh = đạt, đỏ = thiếu/lỗi, vàng = bù/cảnh báo) giữ nguyên ở mọi phong cách.

| `style` | Vẻ ngoài | Hợp khi |
|---|---|---|
| `clean` (mặc định) | Gọn, sáng/tối theo máy người xem | Khách, tài liệu chính thức |
| `dark` | Nền tối cố định, kiểu bảng điều khiển | Vận hành, giám sát, màn hình lớn |
| `sketch` | Giấy chấm, viền vẽ tay, chữ viết tay cho tiêu đề | Workshop nội bộ, đào tạo, ý tưởng |
| `editorial` | Tiêu đề chữ có chân cỡ lớn, kẻ ngang, ít khung | Lãnh đạo, bản tổng quan, câu chuyện |

`theme` (màu thương hiệu) độc lập với `style`: `onboard`, `neutral` hoặc `{ "brand": "#RRGGBB" }`.

## Bố cục từng bước (`layout`)

Chọn theo nội dung của bước, không dùng một kiểu cho cả trang.

| `layout` | Bố cục | Dùng khi |
|---|---|---|
| `split` (mặc định) | Chữ trái, hình phải | Hình và chữ quan trọng ngang nhau |
| `hero` | Hình chiếm toàn khung phía trên, chữ gọn bên dưới | Hình lớn tự nói: lưới nhiều cột, sơ đồ trình tự, bảng nhiệt, thanh kéo so sánh |
| `center` | Tiêu đề lớn giữa trang, hình nhỏ bên dưới | Một kết luận hoặc con số chính, câu hỏi kiểm tra, bước mở đầu / kết thúc |

Một trang tốt thường xen kẽ: mở bằng `hero` hoặc `center`, giữa trang `split`, kết bằng `center`.

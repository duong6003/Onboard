# Khung xương: Giải thích (business rule, quy trình, luồng tích hợp, kiến trúc, phân quyền, mô hình dữ liệu, onboard người mới)

Người đọc cần: hiểu, và áp dụng đúng trong trường hợp của mình.

## Câu hỏi người đọc, theo thứ tự

1. Cái này là gì, dùng để làm gì? (một câu, kèm hình tổng)
2. Nó chạy thế nào? (luồng, quy tắc, từng bước)
3. Ví dụ thật có số trông ra sao?
4. Trường hợp biên, ngoại lệ, chỗ hay hiểu sai?
5. (tùy `goal`) Tôi cần làm gì / kiểm tra gì với nó?

## Ô bắt buộc

| Ô | Nếu thiếu |
|---|---|
| Đối tượng + mục đích | Chặn (điều kiện 2) |
| Cách hoạt động: quy tắc, luồng, công thức | Chặn; không tự nghĩ ra quy tắc nghiệp vụ |
| Ít nhất 1 ví dụ thật có số | Tự dựng ví dụ từ quy tắc đã có, nhãn `illustration` |
| Trường hợp biên | Thiếu: liệt kê câu hỏi mở ở báo lại, không đoán |
| Nguồn quy tắc (tài liệu, phiên bản, ngày) | Ghi "chưa rõ phiên bản" ở báo lại |

## Kế hoạch bước gợi ý (4–8 bước)

| Bước | Ý | Hình gợi ý |
|---|---|---|
| 1 | Bức tranh tổng: các thành phần / vai trò | `flow` có `lanes` |
| 2–4 | Từng giai đoạn của luồng, mỗi bước làm nổi một chặng | `flow` với `highlight` đổi theo bước |
| 5 | Ví dụ có số | `bars`, `stats`, `grid` hoặc `timeline` tùy dữ liệu |
| 6 | Trường hợp biên / hay nhầm | `compare` (đúng vs nhầm) hoặc `checks` |
| 7 | Điều cần nhớ / cần làm | `list` |

## Lỗi hay gặp

- Mở đầu bằng định nghĩa dài; người đọc cần hình tổng trước.
- Ví dụ không có số, hoặc số tự nghĩ mà không gắn nhãn.
- Một bước ôm cả luồng; nên dùng cùng một `flow` và đổi `highlight` qua từng bước.

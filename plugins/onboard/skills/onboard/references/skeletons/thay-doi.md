# Khung xương: Thay đổi (release, tính năng mới, go-live theo giai đoạn, CR đã duyệt, quy trình mới)

Người đọc cần: chuẩn bị. Đọc xong phải biết: cái gì đổi, có ảnh hưởng đến mình không, mình phải làm gì, trước khi nào.

## Câu hỏi người đọc, theo thứ tự

1. Trước đây thế nào, sau này thế nào?
2. Vì sao đổi? (một câu)
3. Ai, cái gì bị ảnh hưởng?
4. Tôi phải làm gì, theo thứ tự nào?
5. Khi nào? Có gì sai thì quay lui thế nào, hỏi ai?

## Ô bắt buộc

| Ô | Nếu thiếu |
|---|---|
| Trước / sau | Chặn |
| Đối tượng bị ảnh hưởng | Suy từ phạm vi thay đổi, nhãn `unconfirmed` |
| Việc người đọc phải làm | Với `goal: operate/prepare`: chặn. Còn lại: ghi "chưa có việc cần làm" |
| Thời điểm, hạn | Ghi "chưa chốt ngày", nhãn `unconfirmed` |
| Phương án quay lui, đầu mối hỗ trợ | Báo lại là thiếu; không tự đặt người |

## Kế hoạch bước gợi ý (4–8 bước)

| Bước | Ý | Hình gợi ý |
|---|---|---|
| 1 | Trước → sau | `compare` |
| 2 | Vì sao đổi | `stats` hoặc `bars` (số trước/sau) |
| 3 | Ai bị ảnh hưởng | `grid` (đối tượng × hạng mục) hoặc `flow` |
| 4 | Lộ trình / giai đoạn | `timeline` (points = mốc, targets = phạm vi từng giai đoạn) |
| 5 | Việc phải làm | `list` có `owner`, `due` |
| 6 | Quay lui, hỗ trợ | `checks` hoặc `list` |

## Lỗi hay gặp

- Kể tính năng mà không nói người đọc phải làm gì.
- Ghi ngày dự kiến như ngày đã chốt.

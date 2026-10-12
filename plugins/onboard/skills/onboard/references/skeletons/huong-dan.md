# Khung xương: Hướng dẫn (hướng dẫn sử dụng, runbook, đào tạo, bàn giao công việc)

Người đọc cần: làm theo được, và biết mình làm đúng chưa.

## Câu hỏi người đọc, theo thứ tự

1. Làm cái này để đạt được gì? Cần chuẩn bị gì (quyền, dữ liệu, công cụ)?
2. Các bước, mỗi bước một thao tác.
3. Làm đúng thì thấy gì?
4. Hay gặp lỗi gì, xử lý ra sao, hỏi ai?

## Ô bắt buộc

| Ô | Nếu thiếu |
|---|---|
| Mục tiêu thao tác | Chặn |
| Điều kiện, quyền cần có | Báo lại là thiếu |
| Các bước thao tác thật (tên nút, màn hình) | Chặn; không tự đặt tên nút/màn hình |
| Dấu hiệu làm đúng | Suy từ hệ thống, nhãn `unconfirmed` |
| Lỗi thường gặp | Thiếu: bỏ bước lỗi, báo lại |

## Kế hoạch bước gợi ý (4–10 bước)

| Bước | Ý | Hình gợi ý |
|---|---|---|
| 1 | Mục tiêu + chuẩn bị | `checks` (điều kiện ✓) |
| 2–n | Mỗi bước một thao tác | `flow` một làn, `highlight` bước hiện tại; ảnh màn hình nếu người dùng gửi (dùng `custom` với ảnh nhúng data URI) |
| n+1 | Làm đúng thì thấy gì | `stats` hoặc `compare` |
| n+2 | Lỗi hay gặp | `checks` (status `key`) |

Với thao tác dài trên giao diện, cân nhắc gợi ý bổ sung bản hướng dẫn tài liệu (Word/Doc) ở phần báo lại; v1 chỉ dựng trang bấm từng bước.

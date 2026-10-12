# Thẻ hỏi nhanh khi gọi /onboard

Hỏi **định hướng đầu ra** (người soạn muốn gì) khác với hỏi **dữ liệu thiếu** (`content-requirements.md`). Định hướng luôn hỏi ngay đầu, trừ khi rơi vào trường hợp bỏ qua bên dưới. Mục tiêu: một lượt bấm, không phải gõ.

## Khi nào bỏ qua thẻ

- Người soạn đã nói rõ cả hình thức, người xem và phong cách trong câu lệnh.
- Câu lệnh có `nhanh`, "không cần hỏi", "cứ làm đi": dùng các phương án đề xuất, ghi lại trong báo lại.
- Đang sửa một trang đã làm trong cùng hội thoại.
- Đã biết một phần: chỉ hỏi phần còn thiếu (1–2 câu).

## Nội dung thẻ (tối đa 3 câu, mỗi câu 2–4 lựa chọn)

Đặt phương án đề xuất lên đầu và ghi "(đề xuất)". Đề xuất dựa trên nguồn và câu lệnh, theo bảng ở §3.

| Câu | Lựa chọn | Ghi vào |
|---|---|---|
| Hình thức? | Bấm từng bước · Trang cuộn kể chuyện · Tóm gọn 1 trang · Slide hoặc video | `format` (xem `formats.md`) |
| Ai xem, đọc để làm gì? | Khách / lãnh đạo, để quyết định · Người mới, để hiểu · QC / Dev, để kiểm tra · Vận hành, để làm theo | `brief.audience` theo bộ cài sẵn trong `audiences.md` |
| Phong cách? | Gọn chuyên nghiệp · Bảng điều khiển tối · Phác thảo bảng trắng · Tạp chí chữ lớn | `style` (xem `styles.md`) |

Chọn "Slide hoặc video" thì hỏi tiếp đúng một câu (slide hay video) ở lượt sau, hoặc tự chọn nếu câu lệnh đã gợi ý ("để chiếu trong họp" → slide; "đăng nhóm / màn hình sảnh" → video).

Ngôn ngữ và mức không cần hỏi trong thẻ: suy từ câu lệnh, ghi trên dòng tóm tắt; người soạn sửa nếu sai.

## Cách hiện

1. Một dòng **mức đề xuất** (`levels.md`).
2. Một dòng **mình hiểu là**: chủ đề, nguồn đã đọc, ngôn ngữ. Ví dụ: "Giải thích rule chèn Spot mới so với rule cũ, nguồn: file Word 14 mục, tiếng Việt."
3. Nếu có dữ liệu thiếu chạm điều kiện chặn: phiếu thiếu thông tin ngắn ngay dưới (cùng lượt, không thêm lượt hỏi).
4. Thẻ: dùng công cụ hỏi có nút bấm nếu môi trường có (ví dụ `ask_user_input`); không có thì liệt kê dạng `1a / 1b …` và nói "trả lời ok để dùng đề xuất".
5. Dừng, chờ trả lời.
6. Khi có trả lời: đánh giá lại mức theo `levels.md` (người xem và mục đích vừa chọn là tín hiệu mới). Mức tăng lên high thì làm đúng hành vi của high (storyboard, câu phản biện) trước khi dựng.

## Bảng đề xuất mặc định

| Tín hiệu trong câu lệnh / nguồn | Hình thức | Phong cách |
|---|---|---|
| Trình bày trong họp, giải thích từng bước | Bấm từng bước | Gọn chuyên nghiệp |
| Gửi để người nhận tự đọc, nội dung dài | Trang cuộn kể chuyện | Gọn chuyên nghiệp |
| Lãnh đạo, cần nhìn tổng thể một lần | Tóm gọn 1 trang | Tạp chí chữ lớn |
| Đính kèm email, đưa vào bộ tài liệu | Slide | Gọn chuyên nghiệp |
| Màn hình sảnh, đăng nhóm, giới thiệu ngắn | Video | Bảng điều khiển tối |
| Workshop nội bộ, đào tạo người mới | Bấm từng bước | Phác thảo bảng trắng |
| Vận hành, giám sát | Bấm từng bước | Bảng điều khiển tối |

## Phần thêm do skill tự đề xuất (không hỏi trong thẻ)

Ghi vào dòng "mình hiểu là" nếu nội dung hợp, người soạn bỏ được bằng một câu:
- Có công thức, ngưỡng, số liệu biến đổi → thêm bước **mô phỏng** (`calc`).
- Onboard người mới, đào tạo → thêm bước **câu hỏi kiểm tra** (`quiz`) ở cuối.
- Trình chiếu không người điều khiển → bật **tự chạy** (`autoplay`).

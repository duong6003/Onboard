# Bài học tích lũy

Đọc file này trước mỗi lần làm. Mỗi dòng là một lần người dùng sửa và đồng ý biến thành quy tắc.

## Cách thêm bài học

Khi người dùng sửa kết quả (ví dụ "quá nhiều chữ", "chỗ này đang tự suy"), hỏi một câu: có nên ghi thành quy tắc cho các lần sau không. Chỉ thêm khi họ đồng ý.
- Thư mục skill ghi được (Claude Code, Cowork): thêm dòng vào bảng dưới.
- Không ghi được (claude.ai): đưa dòng đề xuất vào cuối phần báo lại, mục "Đề xuất bài học", để người dùng cập nhật skill khi đóng gói lại.

Một bài học tốt là quy tắc dùng được cho tình huống khác, không phải mô tả một lần sửa cụ thể.

## Bảng bài học

| Ngày | Bài học | Quy tắc liên quan |
|---|---|---|
| 2026-10-12 | Trang nhiều chữ thì người mới không đọc. Mỗi bước một ý, tối đa 2 câu, hình làm phần chính. | writing-rules §2 |
| 2026-10-12 | Một bước gói cả nhân quả theo thời gian thì khó hiểu. Tách 3 nhịp: bối cảnh → kích hoạt → hậu quả, cùng một hình biến đổi dần. | writing-rules §2, skeletons/su-viec |
| 2026-10-12 | Yêu cầu của người soạn ("1 phút là hiểu", "cho người mới") lọt vào trang. Brief tách khỏi nội dung, tiêu đề phải là kết luận. | writing-rules §1 |
| 2026-10-12 | Hình dựng bằng script bên trong SVG có thể không chạy ở môi trường hiển thị. Luôn build bằng engine và xem ảnh chụp từ check.py trước khi giao. | SKILL.md bước 6 |
| 2026-10-12 | Bản cho khách, QC, BA cần ngôn ngữ chuẩn, thuật ngữ thống nhất, không ví von đời thường thay cho cơ chế. | writing-rules §5, audiences §3 |
| 2026-10-12 | Con số chưa xác nhận (ví dụ thời lượng một lượt) bị trình bày như sự thật. Mọi giả định phải có nhãn trên trang. | writing-rules §3, content-requirements |
| 2026-10-12 | Bản dịch tiếng Nhật do Claude làm cần người quen thuật ngữ phía khách đọc lại. | writing-rules §6 |
| 2026-10-13 | Tài liệu nguồn thường có sẵn câu hướng dẫn cách đọc và phép ví von; lấy ý, không mang lời dẫn và ví von sang trang. | writing-rules §1 |
| 2026-10-13 | Sơ đồ luồng có làn từ 3 cột trở lên dễ chật trên điện thoại; kiểm tra bản mobile, chật thì đổi sang checks. | visuals.md (flow) |
| 2026-10-13 | Nguồn tự nêu người đọc (có cả khách) thì dùng để quyết định ranh giới chia sẻ, không cần hỏi. | content-requirements §4 |
| 2026-10-13 | Mọi lần chạy ra cùng một kiểu trang. Khi gọi /onboard, hỏi người soạn muốn hình thức, người xem, phong cách bằng thẻ bấm chọn; hỏi định hướng khác với hỏi dữ liệu thiếu. | intake.md |
| 2026-10-13 | Bố cục giống hệt nhau ở mọi bước làm trang đơn điệu. Chọn layout theo nội dung từng bước. | styles.md |
| 2026-10-13 | Tài liệu nguồn yêu cầu "xác minh" một sự thật công khai (ví dụ ngày hết hỗ trợ của nền tảng): tra nguồn chính thức, đưa kết quả lên trang kèm nguồn, không suy diễn thêm quyết định ngoài phạm vi tài liệu. | content-requirements §2 |
| 2026-10-13 | Trang xin duyệt bị rút gọn thành thông báo: bỏ mất lý do làm ngay, phương án so sánh và câu trả lời cho câu hỏi đầu tiên của người duyệt. Ngắn không được cắt lý lẽ; luôn liệt kê câu phản biện và trả lời trên trang hoặc hỏi người soạn. | skeletons/quyet-dinh.md |
| 2026-10-13 | Chọn "lãnh đạo, để duyệt" trong thẻ hỏi là tín hiệu nâng mức; phải đánh giá lại mức ngay sau thẻ. | levels.md, intake.md |

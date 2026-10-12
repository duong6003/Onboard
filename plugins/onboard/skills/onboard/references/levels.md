# Mức kiểm soát: low · medium · high · ultra

Mức quyết định skill hỏi bao nhiêu, kiểm nguồn kỹ đến đâu và tự kiểm sâu cỡ nào. Mức cao an toàn hơn nhưng tốn thời gian và câu hỏi hơn.

## 1. Mức do người dùng chỉ định luôn thắng

`/onboard high …`, "làm mức ultra", "làm nhanh thôi" (→ low). Có chỉ định thì dùng đúng mức đó, không tranh luận. Nếu thấy rủi ro rõ ràng (ví dụ chỉ định low nhưng gửi khách), vẫn làm theo và ghi khuyến nghị vào phần báo lại.

## 2. Không chỉ định: tự đề xuất theo tín hiệu

| Tín hiệu | low / medium | high | ultra |
|---|---|---|---|
| Người nhận | Nội bộ team | Khách hàng, cấp trên | Cơ quan nhà nước, đối tác ký kết |
| Mục đích | Hiểu, tham khảo | Ra quyết định | Cam kết, chi phí, hợp đồng |
| Mức nghiêm trọng | Nháp, ý tưởng | Sự cố ảnh hưởng khách | Sự cố production, ảnh hưởng tiền |
| Phạm vi lan truyền | Gửi 1-1 nội bộ | Gửi ra ngoài, đa ngữ | |
| Độ đủ của nguồn | Đầy đủ | Thiếu nhiều mà vẫn gửi ra ngoài: nâng 1 mức | |

Quy tắc chọn:
- Lấy mức cao nhất mà một **tín hiệu rõ ràng** chỉ tới. Đánh giá thấp rủi ro tốn kém hơn hỏi thêm một câu.
- Tín hiệu mơ hồ không được kéo mức lên.
- Không đủ tín hiệu: dùng `medium` và nói rõ "thiếu tín hiệu".
- Giữa low và medium: nội bộ + mục đích hiểu → low; nội bộ nhưng người đọc phải làm theo → medium.

Hiện đề xuất trên **một dòng ở đầu câu trả lời**:

> **Mức đề xuất: high**, vì người nhận là khách và tài liệu dùng để quyết định. Đổi mức: `/onboard medium`.

- low / medium: chạy luôn, không chờ xác nhận.
- high / ultra: dòng đề xuất đi cùng câu hỏi hoặc storyboard (hai mức này vốn có bước duyệt); người dùng hạ mức ngay khi trả lời.
- **Đánh giá lại ngay sau thẻ hỏi nhanh**: câu trả lời trong thẻ (ví dụ chọn "lãnh đạo, để duyệt") là tín hiệu mới; nâng mức nếu cần và nói một dòng trước khi làm tiếp.
- Tín hiệu mới xuất hiện khi đã dựng xong: không tự đổi mức, ghi khuyến nghị vào phần báo lại.

## 3. Hành vi theo mức

| | low | medium | high | ultra |
|---|---|---|---|---|
| Hỏi trước khi viết | Không | Chỉ khi chạm 3 điều kiện chặn (`content-requirements.md`) | Gộp 1 lượt, tối đa 3 câu | Hỏi kỹ, có thể nhiều lượt |
| Duyệt storyboard | Không | Không; tóm storyboard trong phần báo lại | Có, chờ duyệt | Có, rồi duyệt bản nháp chữ trước khi dựng hình |
| Nguồn | Dùng những gì có | Mỗi sự thật có nguồn hoặc có nhãn | Mỗi bước sự thật có `sources` (check.py bắt buộc) | Như high, và không cho phép giả định với sự thật trung tâm: thiếu thì bỏ bước hoặc ghi "chưa xác nhận" |
| Tự kiểm | check.py (tĩnh) | check.py `--render`, xem sheet ngôn ngữ chính | Như medium + xem sheet mọi ngôn ngữ, phép thử 2 câu cho từng câu | Như high + dịch ngược để soát bản dịch, kiểm thuật ngữ thống nhất |
| Báo lại | Gọn: giả định + cần xác nhận | Đủ 5 mục | 5 mục + nguồn của từng con số | 5 mục + nguồn + checklist trước khi gửi |
| Ranh giới chia sẻ không rõ | Coi là nội bộ, ghi vào báo lại | Hỏi (điều kiện chặn), trừ khi nguồn tự nêu người đọc | Hỏi, trừ khi nguồn tự nêu người đọc | Hỏi |

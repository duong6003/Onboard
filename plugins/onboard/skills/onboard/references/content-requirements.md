# Yêu cầu nội dung: đủ đến đâu, thiếu thì làm gì

Nguyên tắc gốc: **sự thật không tự suy**. Thiếu thì nói rõ thiếu gì, vì sao cần, thiếu thì ảnh hưởng thế nào. Mặc định là làm trước, báo lại sau; hỏi là ngoại lệ.

## 1. Ba loại thông tin

| Loại | Ví dụ | Được tự làm? |
|---|---|---|
| Sự thật | Số liệu, mốc giờ, phạm vi, nguyên nhân đã xác nhận, quyết định đã chốt, tên hệ thống | Không. Phải có nguồn hoặc được xác nhận |
| Diễn giải | Cách kể, ví dụ minh họa, so sánh, hình | Có, gắn nhãn `illustration` nếu có chi tiết bịa để minh họa |
| Đề xuất | Cách sửa, bước tiếp theo, mục tiêu | Có, gắn nhãn `proposal` hoặc `target` cho tới khi được chốt |

Câu nối, câu dẫn cũng là nội dung. "Sẽ được báo khi có ngày", "áp dụng ngay", "không còn bỏ sót" là cam kết hoặc kết quả mong đợi: chỉ viết khi nguồn nói vậy, không thì bỏ hoặc gắn nhãn `proposal`/`target`.

Suy ra từ nguồn nhưng nguồn không nói thẳng (ví dụ tính 5 giây/lần từ khoảng cách log) là **sự thật chưa xác nhận**: dùng được, nhưng gắn nhãn `unconfirmed`.

## 2. Tìm trước khi hỏi

Thứ tự:
1. File gửi kèm và nội dung hội thoại.
2. Project, memory, tài liệu đã có trong phiên.
3. Connector nội bộ đang bật (Drive, Microsoft 365, …) nếu có công cụ.
4. Web, **chỉ** cho kiến thức công khai (chuẩn VAST, định nghĩa thuật ngữ). Không bao giờ dùng web để lấp sự thật nội bộ.

## 3. Chấm độ đủ

Mở file khung xương (`skeletons/*.md`), lấy danh sách ô bắt buộc, chấm từng ô:

- ✓ **Có nguồn**: dùng thẳng, ghi vào `sources` của bước.
- ⚠ **Suy ra được, chưa xác nhận**: dùng kèm nhãn, đưa vào mục "cần xác nhận" khi báo lại.
- ✗ **Thiếu**: hỏi (nếu chạm điều kiện chặn) hoặc bỏ bước / thay bằng ghi chú "chưa có".

"Đủ" nghĩa là mọi câu hỏi của khung được trả lời bằng sự thật có nguồn hoặc một mục có nhãn rõ ràng. Không bước nào trình bày điều chưa xác nhận như sự thật.

## 4. Ba điều kiện chặn (phải hỏi trước khi viết)

1. **Sai sẽ gây hại thật**: tài liệu gửi ra ngoài và chỗ thiếu là sự thật trung tâm (số liệu chính, cam kết, nguyên nhân); hoặc trang dùng để ra quyết định và chỗ thiếu là câu phản biện có thể đổi quyết định (xem `skeletons/quyet-dinh.md`), kể cả tài liệu nội bộ.
2. **Thiếu làm đổi cả câu chuyện**: không biết người nhận hay mục đích, và không giả định hợp lý được. Ví dụ: `/onboard` không kèm nội dung; "giải thích quy tắc phân bổ spot" mà không có quy tắc.
3. **Ranh giới chia sẻ không rõ**: không biết nội bộ hay gửi khách (ở mức medium trở lên). Trước khi hỏi, xem nguồn có tự nêu người đọc không (ví dụ "tài liệu dành cho BA, khách hàng…") hoặc đã được viết để gửi ra ngoài không. Có thì dùng: coi là `external`, không hỏi, ghi lý do vào báo lại. Chỉ hỏi khi nguồn cũng không cho biết.

Ngoài 3 điều kiện này: làm tiếp, ghi lại trong phần báo lại. Mức low chỉ dừng ở điều kiện 2.

## 5. Phiếu thiếu thông tin

Khi phải hỏi: gộp **một lượt**, tối đa 3 câu (ultra được nhiều hơn), xếp theo mức quan trọng. Mỗi câu đủ 4 ý:

| Cần gì | Vì sao cần (bước nào, câu hỏi người đọc nào) | Nếu không có thì sao | Phương án mặc định |
|---|---|---|---|

Phương án mặc định luôn là một trong: dùng giả định có nhãn · bỏ bước đó · ghi "chưa xác nhận". Người dùng chỉ cần trả lời "ok mặc định" là đi tiếp được.

Ví dụ:

| Cần gì | Vì sao | Nếu không có | Mặc định |
|---|---|---|---|
| Nội dung Rule 1, Rule 2 của phân bổ spot (văn bản hoặc ví dụ số) | Cả trang là giải thích quy tắc; không có thì không có gì để giải thích | Không thể làm trang | Không có: dừng |
| Tài liệu này gửi khách hay nội bộ? | Quyết định có hiện log, chi phí nội bộ không | Có thể lộ thông tin nội bộ | Coi là gửi khách, che log |
| Mốc go-live giai đoạn 2 | Bước "Khi nào" của khung Thay đổi | Người đọc không biết chuẩn bị đến khi nào | Ghi "chưa chốt ngày", nhãn `unconfirmed` |

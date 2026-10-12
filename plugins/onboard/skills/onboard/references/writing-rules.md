# Quy tắc viết

## 1. Không để yêu cầu rò rỉ vào nội dung (quan trọng nhất)

Có hai ngăn tách biệt:

| Ngăn | Là gì | Hiện trên trang? |
|---|---|---|
| Yêu cầu (brief) | Ai đọc, đọc bao lâu, giọng, mục đích, mức | Không. Chỉ quyết định cách viết. Nằm trong `brief` của story, build.py không đưa ra HTML |
| Nội dung | Điều người đọc cần biết hoặc cần làm | Có |

"1 phút là hiểu" phải thể hiện bằng trang ngắn và rõ thật, không phải bằng dòng chữ "đọc nhanh trong 1 phút".

Các dạng rò rỉ hay gặp:

| Dạng | Sai | Sửa |
|---|---|---|
| Nhắc tiêu chí độ dài | "Đọc nhanh 1 phút", "Tóm tắt ngắn gọn" | Bỏ |
| Gọi tên người đọc / mức độ | "Dành cho người mới", "Giải thích đơn giản" | Bỏ, giải thích đơn giản thật |
| Hướng dẫn cách đọc | "Đọc phần này là đủ", "Các phần sau giải thích chi tiết" | Bỏ |
| Tiêu đề là nhãn cấu trúc | "Tóm tắt", "Tóm lại", "Tổng quan" | Tiêu đề là kết luận: "Cần cả cursor và chạy song song" |
| Nhắc đề bài | "Theo yêu cầu…" | Bỏ |
| Tự khen | "Cực kỳ dễ hiểu", "Rất quan trọng" | Đưa nội dung chứng minh thay vì khen |
| Dẫn vào hình | "Hình dưới đây cho thấy…" | Bỏ; hình tự nói, `caption` nói kết luận |

Tài liệu nguồn thường đã có sẵn kiểu chữ này ("Tóm tắt trong 1 phút", "Đọc tài liệu này như thế nào?", "Tài liệu dành cho…") và phép ví von đời thường. Không mang sang trang: lấy ý, bỏ lời dẫn; giải thích bằng cơ chế thay cho ví von.

Được giữ vì phục vụ người đọc: nhãn trung thực ("Minh họa: …"), điều hướng ("Bước 3/10"), mục bắt buộc của thể loại.

**Phép thử 2 câu** cho mỗi câu chữ:
1. Người đọc không biết đề bài, câu này còn có ích không?
2. Câu này nói về sự việc, hay nói về tài liệu và người viết?

Trượt một trong hai thì cắt. check.py quét các cụm phổ biến ở VI/EN/JA; phần còn lại phải tự rà. Cụm nào hợp lệ trong ngữ cảnh (ví dụ nội dung thật sự là "quy trình cho người mới") thì thêm vào `lint.allow` của story.

## 2. Một bước, một ý

- Tiêu đề là **kết luận** của bước, đọc mỗi tiêu đề nối nhau phải ra cả câu chuyện.
- `body`: tối đa 2 câu. `chips`: tối đa 2. Thêm chữ chỉ khi hình không tự nói được.
- Giới hạn tham khảo: tiêu đề ≤ 70 ký tự (JA ≤ 36), body ≤ 260 (JA ≤ 130), chip ≤ 120 (JA ≤ 60).
- Ý phức tạp (nhân quả theo thời gian, nhiều điều kiện) tách **3 nhịp**: bối cảnh → điều kích hoạt → hậu quả, mỗi nhịp một bước, cùng một hình biến đổi dần.
- Mỗi trang 4–10 bước. Quá 12 thì tách trang.

## 2b. Trang để ra quyết định

- Kết luận trước: bước 1 nói đề xuất và điều cần duyệt; bằng chứng theo sau.
- Mỗi luận điểm đi kèm bằng chứng cụ thể: con số, mốc ngày, nguồn. "Rủi ro cao" không thuyết phục bằng "hết hỗ trợ từ 14/5/2024".
- Nói thẳng điều bất lợi cho đề xuất (ví dụ phương án đề xuất chưa khớp hợp đồng). Người duyệt tin trang hơn khi thấy mặt yếu đã được nêu và có cách xử lý.
- Không trình bày đề xuất như sự thật đã quyết; dùng nhãn `proposal`.

## 3. Nhãn trung thực

Bước có nội dung không phải sự thật đã xác nhận phải có `basis` và `note` cùng loại:

| basis / note.type | Khi nào | Ví dụ note |
|---|---|---|
| `illustration` | Có chi tiết dựng ra để minh họa cơ chế | "Thời lượng 90 giây là giả định để minh họa." |
| `assumption` | Dựa trên giả định chưa ai xác nhận | "Giả định go-live sau UAT 1 tuần." |
| `unconfirmed` | Suy ra từ nguồn, nguồn không nói thẳng | "Suy ra từ khoảng cách giữa các lượt trong log." |
| `proposal` | Giải pháp, việc đề xuất chưa chốt | "Giải pháp đề xuất, chưa triển khai." |
| `target` | Con số mục tiêu, chưa đạt | "160/160 là mục tiêu sau khi sửa." |

Note ngắn, nói điều gì là giả định/đề xuất, không xin lỗi, không giải thích dài.

## 4. Màu mang nghĩa cố định

ok = xanh (đúng, có, đạt) · bad = đỏ (thiếu, lỗi, vượt) · warn = vàng (bù, cảnh báo, đang chờ) · info = xanh dương (trung tính cần chú ý) · muted = mờ (không liên quan). Không dùng màu để trang trí. Màu thương hiệu chỉ ở khung (tiêu đề, thanh tiến độ).

## 5. Thuật ngữ

- Không có bộ thuật ngữ chung cố định. Mỗi lần làm, rút thuật ngữ từ chính nguồn, ưu tiên từ người nhận đang dùng.
- Người dùng gửi bảng thuật ngữ dự án thì dùng bảng đó.
- Không dịch: tên sản phẩm, tên API, tên trường dữ liệu, mã thiết bị.
- Trong một trang, một khái niệm chỉ một từ, một bản dịch.
- Thuật ngữ mới với người đọc: giải thích một lần ở bước đầu dùng tới, bằng nửa câu.

## 6. Đa ngôn ngữ

- Viết ngôn ngữ chính trước, chốt nội dung, rồi mới dịch. Mỗi ngôn ngữ phải tự nhiên, không dịch từng chữ.
- Tiếng Nhật: thể です/ます cho khách; câu ngắn; số và giờ giữ nguyên dạng.
- Số thập phân: VI dùng dấu phẩy (0,3), EN/JA dùng dấu chấm (0.3).
- Bản dịch tiếng Nhật và ngôn ngữ không phải tiếng mẹ đẻ của người soạn: luôn ghi vào "cần xác nhận" là nên có người bản ngữ đọc lại.

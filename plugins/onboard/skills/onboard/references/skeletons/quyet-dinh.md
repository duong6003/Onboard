# Khung xương: Quyết định (đề xuất phương án, CR có chi phí, trade-off kỹ thuật, xin duyệt kế hoạch, đàm phán phạm vi)

Người đọc cần: ra quyết định và tin rằng quyết định đó đúng. Trang phải **thuyết phục**, không chỉ thông báo.

## Lõi lập luận: không bị cắt, dù độ dài ngắn đến đâu

`length` ngắn chỉ rút gọn chữ và gộp bước; không được bỏ ý nào dưới đây. Thiếu ý nào thì đó là chỗ thiếu nội dung, không phải chỗ để lược.

1. **Cần duyệt gì, trước ngày nào**: con số cụ thể (người, công, tiền, thời gian) và hạn quyết định. Đặt ở bước 1.
2. **Vì sao phải làm bây giờ**: cái giá nếu không làm, có số và nguồn.
3. **Các phương án**: ít nhất 2, luôn gồm "giữ nguyên" và phương án người duyệt chắc chắn sẽ nghĩ tới.
4. **So sánh trên cùng tiêu chí**: dùng `matrix` (bảng phương án × tiêu chí) hoặc `compare` khi chỉ có 2 hướng.
5. **Khuyến nghị và lý do**: nhãn `proposal` nếu là đề xuất của người soạn/báo cáo.
6. **Rủi ro chính và điểm dừng**: mỗi rủi ro có cách xử lý hoặc điều kiện dừng.
7. **Việc cần quyết**: bước cuối, danh sách kèm owner (hoặc "chưa có owner") và hạn.

Bước 1 phải đủ để người bận đọc mỗi bước đó vẫn quyết được: tiêu đề là đề xuất, kèm con số cần duyệt và hạn. Các bước sau là bằng chứng.

## Câu hỏi phản biện của người duyệt (bắt buộc ở mức medium trở lên)

Trước khi lập storyboard, liệt kê 3–5 câu người duyệt sẽ hỏi ngay khi đọc. Ghi vào `brief.objections`: mỗi câu trỏ tới bước trả lời (`step`) hoặc ghi lý do chưa trả lời được (`gap`). check.py báo lỗi nếu thiếu.

Câu hỏi hay gặp:
- Không làm thì sao?
- Sao không chọn phương án X (phương án lớn hơn, rẻ hơn, theo hợp đồng…)?
- Con số này có chắc không? Trượt thì sao?
- Sau khi làm xong thì còn gì phải làm tiếp?
- Tốn bao nhiêu, ai chịu?

Một câu phản biện mà nguồn không trả lời được và **có thể đổi quyết định** là điều kiện chặn: hỏi người soạn trước khi dựng, kể cả tài liệu nội bộ.

## Ô bắt buộc

| Ô | Nếu thiếu |
|---|---|
| Điều cần quyết + người quyết + hạn | Chặn |
| Ít nhất 2 phương án | Tự thêm "giữ nguyên" và phương án người duyệt sẽ hỏi; số liệu không có thì ghi "chưa ước lượng", không tự ước |
| Chi phí / rủi ro từng phương án | Thiếu số: ghi "chưa ước lượng" trên trang và vào phản biện `gap` |
| Ràng buộc hợp đồng, chỉ đạo đã chốt | Hỏi nếu nguồn có dấu hiệu lệch (ví dụ đích hợp đồng khác phạm vi) |
| Khuyến nghị | Theo nguồn; không có thì đề xuất, nhãn `proposal` |

## Kế hoạch bước gợi ý (6–8 bước)

| Bước | Ý | Hình gợi ý |
|---|---|---|
| 1 | Cần duyệt gì, hạn | `stats` + chip điều kiện, `layout: center` |
| 2 | Vì sao bây giờ, cái giá nếu không làm | `stats`, `timeline` |
| 3 | Ràng buộc (hợp đồng, chỉ đạo, ngân sách) | `compare` |
| 4 | So sánh phương án | `matrix` có `recommend`, `layout: hero` |
| 5 | Sau khi làm xong còn gì | `timeline` |
| 6 | Công, lịch, năng lực | `bars`, `calc` |
| 7 | Rủi ro và điểm dừng | `checks` |
| 8 | Việc cần quyết | `list` có owner và hạn, `layout: center` |

Mức thường là `high`; `ultra` khi có chi phí, hợp đồng.

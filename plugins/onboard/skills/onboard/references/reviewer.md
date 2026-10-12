# Soát độc lập: đọc như người nhận

Mục đích: tìm những lỗi người viết không thấy vì đã biết đề bài. Người soát **không đọc `story.json` và brief**, chỉ đọc bản người đọc thấy:

```bash
python3 SKILL_DIR/scripts/reader_view.py story.json [--lang xx] > reader.md
```

Người soát được biết đúng hai điều: người nhận là ai, và họ đọc để làm gì (lấy từ dòng cài đặt). Không được biết nguồn, giả định, ý định của người viết.

Có subagent (ví dụ `onboard:onboard-reviewer` trong Claude Code): giao việc soát cho subagent, chỉ đưa đường dẫn `reader.md` và hai điều trên. Không có subagent: tự soát ở một lượt riêng sau khi build, chỉ mở `reader.md`.

## Năm câu phải trả lời

1. **Tóm lại trang nói gì** trong 3 câu. Không tóm được: trang thiếu mạch, ghi lại bước nào làm đứt mạch.
2. **Câu người nhận sẽ hỏi ngay**: liệt kê 3–5 câu. Câu nào trang chưa trả lời?
3. **Rò rỉ yêu cầu**: câu nào nói về tài liệu, người đọc, độ dài, đề bài thay vì nói về sự việc? (`writing-rules.md` §1)
4. **Luận điểm thiếu căn cứ**: con số, mốc, kết luận nào người đọc không thấy lấy từ đâu, hoặc điều chưa chắc mà không có nhãn?
5. **Từng bước**: tiêu đề có phải kết luận không; hình có chứng minh tiêu đề không; có thuật ngữ chưa giải thích với người nhận này không?

## Kết quả trả về

- **Kết luận**: `Đạt` hoặc `Cần sửa`.
- Tối đa 7 việc cần sửa, xếp theo mức ảnh hưởng tới người nhận, mỗi việc ghi bước và cách sửa ngắn.
- Không viết lại trang, không khen. Việc sửa do người viết làm, rồi chạy lại `check.py`.

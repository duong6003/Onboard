# onboard — skill dựng trang giải trình bấm từng bước

Dành cho người bảo trì skill. Claude đọc `SKILL.md`; file này chỉ để người đọc.

## Dùng

- `/onboard [low|medium|high|ultra] [mô tả]` hoặc nói "làm onboard / giải trình cho …", kèm tài liệu, log, ghi chú.
- Claude đề xuất mức, chấm độ đủ nội dung, hỏi khi thật sự cần, dựng trang HTML một file và báo lại nguồn, giả định, điều cần xác nhận.

## Phiên bản

- **1.3.1** (13/10/2026): sơ đồ trình tự không tràn khi tự gửi ở bên phải; bảng nhiệt rộng hơn, tiêu đề cột xuống dòng; thanh kéo trước/sau hiển thị đúng lớp khi hình có sơ đồ luồng.
- **1.3** (13/10/2026): trang để ra quyết định có lõi lập luận bắt buộc (cần duyệt gì, vì sao bây giờ, ≥ 2 phương án, so sánh, rủi ro và điểm dừng, việc cần quyết) và danh sách câu phản biện của người duyệt (`brief.objections`), check.py kiểm tra cả hai; loại hình `matrix` so sánh phương án, tự thành thẻ trên điện thoại; đánh giá lại mức ngay sau thẻ hỏi; bộ cài Lãnh đạo không còn cắt lý lẽ vì độ dài.
- **1.2.1** (13/10/2026): con số lớn tự co cỡ chữ để vừa thẻ; nhãn vạch giới hạn không tràn khi vạch sát mép; hình ở bố cục `hero` không cao quá nửa màn hình; check.py bắt được số bị tràn thẻ.
- **1.2** (13/10/2026): thẻ hỏi nhanh khi gọi `/onboard` (hình thức, người xem, phong cách); 3 hình thức từ cùng story (bấm từng bước có tự chạy, trang cuộn, tóm gọn 1 trang) và đường đi cho slide/video qua `snap.py`; 4 phong cách (gọn, tối, phác thảo, tạp chí); bố cục từng bước (split, hero, center); 6 loại hình mới (trình tự, trạng thái, bảng nhiệt, thanh kéo, mô phỏng, câu hỏi kiểm tra); lint rò rỉ yêu cầu bớt báo nhầm với cụm chỉ thời gian.
- **1.1** (13/10/2026): lưới ít cột không còn phóng to ô; sơ đồ luồng giữ cỡ chữ đọc được và cuộn ngang trong khung riêng trên màn hình hẹp; check.py cảnh báo luồng có làn từ 4 cột; quy tắc dùng người đọc do nguồn tự nêu để quyết định ranh giới chia sẻ; không mang lời dẫn và ví von của tài liệu nguồn sang trang.
- **1.0** (12/10/2026): bản đầu.

## Cấu trúc

| Đường dẫn | Nội dung |
|---|---|
| `SKILL.md` | Quy trình 8 bước |
| `references/levels.md` | 4 mức, tín hiệu đề xuất mức |
| `references/content-requirements.md` | Sự thật / diễn giải / đề xuất, điều kiện phải hỏi, phiếu thiếu thông tin |
| `references/audiences.md` | 5 núm người đọc, bộ cài sẵn, ranh giới chia sẻ |
| `references/writing-rules.md` | Rò rỉ yêu cầu, một bước một ý, nhãn trung thực, thuật ngữ, đa ngữ |
| `references/situations.md` | Danh mục tình huống → khung xương |
| `references/skeletons/*.md` | 6 khung xương: sự việc, giải thích, thay đổi, quyết định, trạng thái, hướng dẫn |
| `references/intake.md` | Thẻ hỏi nhanh khi gọi `/onboard` |
| `references/formats.md` | Hình thức đầu ra và cách xuất slide/video |
| `references/styles.md` | 4 phong cách, 3 bố cục từng bước |
| `references/visuals.md` | 16 loại hình và cách chọn |
| `references/story-schema.md` | Cấu trúc story.json |
| `references/report-back.md` | Phần báo lại cho người soạn |
| `references/lessons.md` | Bài học tích lũy từ các lần sửa |
| `assets/shell.html` | Engine trình bày (điều hướng, đa ngữ, dark mode, mobile, hình động) |
| `scripts/build.py` | story.json → HTML một file (không bao giờ đưa brief/sources ra trang) |
| `scripts/check.py` | Kiểm tra tĩnh + chụp từng bước mọi ngôn ngữ (cần playwright) |
| `scripts/snap.py` | Chụp hình từng bước + manifest chữ, dùng cho slide/tài liệu |
| `scripts/redact.py` | Che email, IP, token, đường dẫn trước khi gửi ra ngoài |
| `examples/test-sec-rca.story.json` | Ví dụ mẫu đầy đủ (RCA, 3 ngôn ngữ, mức high) |

## Cập nhật

1. Sửa quy tắc trong `references/`, thêm dòng vào `lessons.md` khi có bài học mới.
2. Chạy lại ví dụ mẫu: `python3 scripts/check.py examples/test-sec-rca.story.json --render /tmp/shots`, xem `sheet-*.png`.
3. Đóng gói lại thành `.skill` và cài đè (giữ nguyên tên `onboard`).

# Hình thức đầu ra

Mọi hình thức đi từ cùng một `story.json`. Viết story một lần, xuất được nhiều dạng.

| Hình thức | Cách làm | Hợp khi |
|---|---|---|
| Bấm từng bước | `format: "stepper"` (mặc định) | Trình bày trong họp, giải thích tuần tự |
| Bấm từng bước, tự chạy | `format: "stepper"`, `autoplay: true`; có nút Tự chạy / Tạm dừng | Màn hình sảnh, trình chiếu không người điều khiển; phương án thay video khi không có công cụ làm video |
| Trang cuộn kể chuyện | `format: "scroll"`; mỗi bước một khối, hình chạy khi cuộn tới | Gửi người nhận tự đọc, nội dung dài |
| Tóm gọn 1 trang | `format: "onepage"`; lưới thẻ, mỗi thẻ hình nhỏ + tiêu đề + nhãn; in được | Lãnh đạo, bản tổng quan, đính kèm in |
| Slide | Xem §Slide | Đính kèm, chiếu bằng phần mềm trình chiếu |
| Video / animation | Xem §Video | Giới thiệu ngắn, đăng nhóm |
| Mô phỏng tương tác | Pattern `calc` trong bất kỳ hình thức nào ở trên | Có công thức, ngưỡng, muốn người xem tự thử |
| Câu hỏi kiểm tra | Pattern `quiz`, thường là bước cuối | Onboard, đào tạo |

Với tóm gọn 1 trang: tiêu đề thẻ vẫn là kết luận; nhãn trung thực (`note`) luôn hiện; nên ≤ 9 bước.

## Slide

1. Chạy `python3 SKILL_DIR/scripts/snap.py story.json -o <workdir>/snaps` để có ảnh hình của từng bước (trạng thái cuối, nét gấp 2) và `manifest.json` (tiêu đề, chữ, nhãn theo ngôn ngữ).
2. Công cụ Artifact có loại Slides: đọc hướng dẫn của loại đó, mỗi bước thành một slide (tiêu đề = kết luận, ảnh từ snaps, nhãn trung thực ở chân slide).
3. Không có loại Slides, hoặc người soạn nói rõ PowerPoint: đọc skill `pptx`, dựng từ ảnh và `manifest.json`.
4. Hình tương tác (`calc`, `quiz`, `slider`) không chạy trên slide: thay bằng ảnh trạng thái mặc định và ghi vào báo lại.

## Video

1. Công cụ Artifact có loại cho animation / video (ví dụ Motion): đọc hướng dẫn của loại đó và làm theo quy trình riêng của nó; dùng story làm kịch bản: mỗi bước một cảnh, tiêu đề là câu chính, `body` là câu phụ, nhãn trung thực phải xuất hiện trên hình.
2. Không có: dựng `stepper` với `autoplay: true` và nói rõ đây là phương án thay thế.

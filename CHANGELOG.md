# Changelog

## 2.1.0 (13/10/2026)
- Đổi identity plugin và thư mục package thành `onboard`.
- Bổ sung kiểm tra dữ liệu render, redaction, schema lỗi và installer đa nền tảng.

## 2.0.0 (13/10/2026)
- Đóng gói thành plugin `onboard` trong marketplace `onboard-tools`; cài được cho Claude Code, claude.ai/Cowork (skill) và các agent đọc `SKILL.md` qua `install/install.py`.
- Skill mới `onboard-review` để soát trang có sẵn. Subagent `onboard-reviewer` (đọc như người nhận, không thấy brief) và `onboard-translator` (dịch song song từng ngôn ngữ). Hook tự kiểm `story*.json` sau khi ghi.
- Script mới: `doctor.py` (kiểm môi trường), `regress.py` (chạy lại story mẫu), `reader_view.py` (bản người đọc thấy), `hook_check.py`.
- `SKILL.md` có bảng môi trường và bước soát độc lập; thêm 2 story mẫu (trang quyết định, trình diễn loại hình).

## 1.3.1
- Sơ đồ trình tự không tràn khi tự gửi ở bên phải; bảng nhiệt rộng hơn; thanh kéo trước/sau hiển thị đúng lớp.

## 1.3
- Lõi lập luận bắt buộc và câu phản biện (`brief.objections`) cho trang để ra quyết định; loại hình `matrix`; đánh giá lại mức sau thẻ hỏi.

## 1.2.1
- Con số lớn tự co cỡ chữ; nhãn vạch giới hạn không tràn; hình `hero` không cao quá nửa màn hình.

## 1.2
- Thẻ hỏi nhanh; 3 hình thức (bấm từng bước có tự chạy, trang cuộn, tóm gọn 1 trang); đường đi cho slide/video; 4 phong cách; bố cục từng bước; 6 loại hình mới.

## 1.1
- Lưới ít cột không phóng to ô; sơ đồ luồng cuộn ngang trên màn hình hẹp; dùng người đọc do nguồn tự nêu để quyết định ranh giới chia sẻ.

## 1.0
- Bản đầu: quy trình, mức kiểm soát, 5 núm người đọc, quy tắc viết, engine trang bấm từng bước, build/check/redact.

---
name: onboard-translator
description: Dịch story.json của trang onboard sang một ngôn ngữ đích (ví dụ en, ja), giữ nguyên cấu trúc, mã, số liệu và thuật ngữ đã chốt. Dùng khi trang cần thêm ngôn ngữ; có thể chạy song song mỗi ngôn ngữ một subagent.
tools: Read, Write, Bash
---

Nhiệm vụ: thêm bản dịch cho đúng một ngôn ngữ đích vào mọi trường chữ hiển thị trong `story.json` được giao, ghi ra file mới `<tên>.<lang>.story.json`.

- Quy tắc: `${CLAUDE_PLUGIN_ROOT}/skills/onboard/references/writing-rules.md` §5 (thuật ngữ) và §6 (đa ngôn ngữ). Danh sách thuật ngữ đã chốt nếu được giao thì dùng đúng.
- Chuỗi đơn ngữ thành object theo mã ngôn ngữ, giữ bản gốc: `"Lượt chạy"` → `{ "vi": "Lượt chạy", "en": "Run" }`. Object đã có thì chỉ thêm khóa ngôn ngữ đích.
- Không dịch: tên sản phẩm, tên API, tên trường dữ liệu, mã thiết bị, mã campaign, giờ, số. Không dịch khóa cấu trúc (`pattern`, `status`, `id`…) và không đụng `brief`.
- Viết tự nhiên theo ngôn ngữ đích, không dịch từng chữ; tiếng Nhật dùng thể です/ます với khách; số thập phân EN/JA dùng dấu chấm.
- Thêm mã ngôn ngữ vào `langs`, rồi chạy `python "${CLAUDE_PLUGIN_ROOT}/skills/onboard/scripts/check.py" <file mới>` và sửa đến khi không còn lỗi thiếu bản dịch.
- Trả về: đường dẫn file mới và danh sách thuật ngữ đã dịch (gốc → đích) để người soạn duyệt.

---
name: onboard-review
description: Soát lại một trang onboard / giải trình đã dựng (story.json hoặc trang HTML do skill onboard tạo) bằng con mắt của người nhận, trước khi gửi. Dùng khi người dùng nhờ soát, review, kiểm tra lại, đọc thử trang giải trình, hoặc hỏi trang đã đủ thuyết phục, đã dễ hiểu chưa. Also use for "review this explainer page", "is this onboarding page clear".
---

# Soát lại trang onboard

Skill này dùng chung script và quy tắc với skill `onboard` nằm cạnh nó (thư mục `../onboard`; trong Claude Code plugin là `${CLAUDE_PLUGIN_ROOT}/skills/onboard`). Gọi thư mục đó là `ONBOARD_DIR`.

1. Tìm `story.json` của trang. Chỉ có file HTML: nói rõ là cần story để soát đầy đủ; nếu người dùng không có, đọc chữ trên trang và soát theo bước 3–4.
2. Hỏi (hoặc lấy từ câu lệnh) người nhận là ai và họ đọc để làm gì, nếu chưa rõ.
3. `python3 ONBOARD_DIR/scripts/reader_view.py story.json > reader.md`, rồi soát theo `ONBOARD_DIR/references/reviewer.md`. Có subagent `onboard-reviewer` thì giao cho subagent, chỉ đưa `reader.md`, người nhận và mục đích.
4. `python3 ONBOARD_DIR/scripts/check.py story.json --render <thư mục ảnh>` để bắt lỗi kỹ thuật (rò rỉ yêu cầu, thiếu bản dịch, tràn chữ, thiếu lõi lập luận với trang quyết định).
5. Trả lời: kết luận `Đạt` / `Cần sửa`, tối đa 7 việc theo mức ảnh hưởng, mỗi việc ghi bước và cách sửa. Không tự sửa trang trừ khi người dùng nhờ; nhờ sửa thì làm theo skill `onboard` bước 5–7.

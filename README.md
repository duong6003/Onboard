# Onboard: một nguồn, cài cho nhiều agent

Dựng trang giải trình / onboard bấm từng bước, đa ngữ, có hình động, cho khách hàng, lãnh đạo, BA, Dev, QC, vận hành và người mới. Skill tự đề xuất mức kiểm soát, hỏi nhanh định hướng, không bịa số liệu, gắn nhãn giả định và luôn báo lại cho người soạn.

## Thành phần

| Thành phần | Đường dẫn | Chạy ở đâu |
|---|---|---|
| Skill `onboard` (dựng trang) | `plugins/onboard/skills/onboard/` | Mọi agent đọc được `SKILL.md` |
| Skill `onboard-review` (soát trang có sẵn) | `plugins/onboard/skills/onboard-review/` | Mọi agent đọc được `SKILL.md` |
| Subagent `onboard-reviewer`, `onboard-translator` | `plugins/onboard/agents/` | Claude Code |
| Hook tự kiểm `story*.json` sau khi ghi | `plugins/onboard/hooks/hooks.json` | Claude Code |
| Bộ cài cho agent khác | `install/install.py` | Máy có Python 3.8+ |

Ở môi trường không có subagent hoặc hook, skill tự soát theo `references/reviewer.md` và tự chạy `check.py`, nên kết quả không đổi, chỉ chậm hơn.

## Cài đặt

| Agent | Cách cài |
|---|---|
| **Claude Code** | `/plugin marketplace add <git-url nội bộ hoặc đường dẫn thư mục repo>` rồi `/plugin install onboard@onboard-tools`. Lệnh có tiền tố tên plugin, ví dụ `/onboard:onboard`; Claude cũng tự gọi skill khi yêu cầu khớp mô tả |
| **claude.ai, Cowork** | Admin phân phối plugin qua cài đặt tổ chức; hoặc từng người tải `onboard.skill` lên phần Skills |
| **Codex, Cursor, Cline, Continue, Roo, Kilo Code, Qwen Code, Junie, Droid, Amp** | `python3 install/install.py --agent <tên>` (cấp người dùng) hoặc thêm `--project <thư mục dự án>`. Xem tên bằng `--list` |
| **Agent khác** (ví dụ Gemini CLI) | `python3 install/install.py --dest <thư mục skills của agent>`; agent không hỗ trợ skill thì thêm `--agents-md <dự án>/AGENTS.md` để agent biết đọc `SKILL.md` |

Đường dẫn skills mặc định của từng agent có thể đổi theo phiên bản agent; nếu agent không thấy skill, kiểm lại tài liệu của agent rồi dùng `--dest`.

Sau khi cài, chạy `python3 <thư mục skill>/onboard/scripts/doctor.py` để biết phần nào chạy được. Thiếu Playwright vẫn dùng được, chỉ bỏ qua bước kiểm hiển thị (cài: `pip install playwright pillow && python3 -m playwright install chromium`).

## Cập nhật và phát hành

1. Sửa trong `plugins/onboard/skills/onboard/` (quy tắc ở `references/`, engine ở `assets/shell.html`, script ở `scripts/`).
2. Chạy `python3 -m unittest discover -s tests -v`, `python3 plugins/onboard/skills/onboard/scripts/regress.py --no-render` và `claude plugin validate . --strict`. Có Playwright/Chromium thì chạy thêm kiểm hiển thị.
3. Tăng `version` trong `plugins/onboard/.claude-plugin/plugin.json` và `metadata.version` trong `SKILL.md`, ghi `CHANGELOG.md`, commit và tag.
4. Bài học mới từ người dùng: thêm một dòng vào `references/lessons.md` qua merge request.

## Đã kiểm

- `claude plugin validate --strict` (Claude Code 2.1.296): plugin và marketplace đều pass.
- Thêm marketplace từ thư mục và cài `onboard@onboard-tools`: thành công, plugin ở trạng thái enabled.
- `install.py` cài cho Codex và Cursor ở cấp dự án, thêm chỉ dẫn vào `AGENTS.md`: thành công.
- `tests/test_plugin.py`: kiểm tra các biên schema, redaction, hook, installer và identity plugin.
- `regress.py`: 3 story mẫu, 0 lỗi kiểm tra tĩnh; kiểm hiển thị cần Playwright/Chromium.

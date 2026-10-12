---
name: onboard
metadata:
  version: "2.1.0"
description: Tạo trang giải trình / onboard bấm qua từng bước, siêu dễ hiểu, có hình động, đa ngữ (VI/EN/JA) cho khách hàng, lãnh đạo, PM, BA, Dev, QC, vận hành hoặc người mới. Dùng skill này mỗi khi người dùng gõ /onboard, hoặc nhờ giải thích, giải trình, trình bày lại cho dễ hiểu, onboard người mới, viết lại để khách/QC/BA đọc là hiểu, làm bản song ngữ hay đa ngữ, giải thích sự cố/RCA, business rule, quy trình nghiệp vụ, luồng tích hợp, tính năng mới, release, go-live, đề xuất phương án, báo cáo tiến độ, hướng dẫn thao tác, kể cả khi họ không nói chữ onboard. Also use for English requests such as explain this simply, explainer or onboarding walkthrough, incident write-up, bilingual explanation, scrollytelling, one-page summary, slides, short video, simulator or quiz. Skill hỏi nhanh hình thức, người xem, phong cách bằng thẻ bấm chọn, tự đề xuất mức kiểm soát (low/medium/high/ultra), chấm độ đủ nội dung, không bịa số liệu, gắn nhãn mọi giả định và luôn báo lại cho người soạn.
---

# Onboard: trang giải trình bấm từng bước

Đầu ra mặc định là một trang HTML một file: mỗi bước một ý, một hình động, tối đa hai câu chữ; xem được trên điện thoại, dark mode, chuyển ngôn ngữ. Cùng nội dung xuất được thành trang bấm từng bước (có thể tự chạy), trang cuộn, tóm gọn 1 trang, slide hoặc video, kèm mô phỏng tương tác và câu hỏi kiểm tra. Người soạn nhận thêm phần **báo lại** trong chat: nguồn, giả định, điều cần xác nhận.

Hai thứ quyết định chất lượng, và cũng là hai lỗi hay gặp nhất:
- **Nội dung đúng và đủ**: không tự suy sự thật; thiếu thì nói rõ, không lấp bằng phỏng đoán.
- **Chữ phục vụ người đọc**: yêu cầu của người soạn ("cho người mới", "1 phút là hiểu") quyết định cách viết, không bao giờ xuất hiện trên trang.

`SKILL_DIR` dưới đây là thư mục chứa file này. Thư mục làm việc: `/home/claude/onboard-work/<id>/` (hoặc thư mục tạm bất kỳ). File giao: `/mnt/user-data/outputs/` nếu có, không thì thư mục hiện tại.

## Môi trường

Skill chạy trên nhiều agent. Lần đầu trong một môi trường mới, chạy `python3 SKILL_DIR/scripts/doctor.py` để biết phần nào chạy được.

| Môi trường | Thẻ hỏi nhanh | Giao trang | Soát độc lập | Ghi bài học |
|---|---|---|---|---|
| claude.ai, Cowork | Công cụ hỏi có nút bấm nếu có | Công cụ Artifact nếu có, không thì trình bày file | Tự soát một lượt riêng theo `references/reviewer.md` | Đưa vào cuối phần báo lại |
| Claude Code (cài dạng plugin) | Công cụ hỏi có lựa chọn nếu có, không thì liệt kê 1a/1b | File HTML trong thư mục dự án | Giao subagent `onboard-reviewer` của plugin | Sửa `references/lessons.md` trong repo plugin rồi commit |
| Agent khác (Codex, Cursor, Gemini CLI…) | Liệt kê 1a/1b bằng chữ | File HTML | Tự soát theo `references/reviewer.md` | Ghi `references/lessons.md` nếu thư mục ghi được |

Thiếu Playwright: vẫn build và kiểm tĩnh được; ghi "chưa kiểm hiển thị" vào báo lại.

## Quy trình

Làm đúng thứ tự. Mỗi bước đọc file tham chiếu tương ứng khi cần; không cần đọc hết một lúc.

### 0. Nạp bài học
Đọc `references/lessons.md`. Đây là các lần sửa trước đã thành quy tắc.

### 1. Hiểu yêu cầu, gom nguồn
- Cú pháp: `/onboard [low|medium|high|ultra] [mô tả]`, hoặc yêu cầu bằng lời. Không có mô tả và không có nội dung kèm theo → hỏi cần giải thích điều gì (điều kiện chặn), dừng.
- Gom nguồn theo thứ tự: file kèm và hội thoại → project/memory → connector nội bộ đang bật → web (chỉ kiến thức công khai). Chi tiết: `references/content-requirements.md` §2.
- Gửi ra ngoài: chạy `python3 SKILL_DIR/scripts/redact.py <nguồn> -o <bản-đã-che>` trên log/ghi chú trước khi trích (`--keep` cho mã khách đã biết, `--mask` cho mẫu riêng).

### 2. Phân loại và đề xuất mức
- Tình huống → khung xương: `references/situations.md`, rồi đọc file `references/skeletons/<khung>.md`.
- Người nhận thật, phạm vi chia sẻ (`internal`/`external`), 5 núm người đọc: `references/audiences.md`. Người dùng nói "coi X như Y" thì vặn núm, không đổi người nhận thật.
- Mức: `references/levels.md`. Người dùng đã chỉ định thì dùng đúng mức đó.
- Mở đầu câu trả lời bằng **một dòng** đề xuất mức kèm lý do (trừ khi người dùng đã chỉ định).

### 2b. Thẻ hỏi nhanh: người soạn muốn gì
Đọc `references/intake.md`. Hỏi một lượt bằng thẻ bấm chọn: hình thức, ai xem để làm gì, phong cách; mỗi câu đặt phương án đề xuất lên đầu. Có trả lời thì đánh giá lại mức ngay (người xem và mục đích vừa chọn là tín hiệu mới). Đi kèm dòng mức và một dòng "mình hiểu là". Nếu bước 3 phát hiện dữ liệu thiếu chạm điều kiện chặn, gộp phiếu thiếu thông tin vào cùng lượt này. Bỏ qua thẻ khi người soạn đã nói rõ, gõ `nhanh`, hoặc đang sửa trang cũ.

### 3. Chấm độ đủ (làm cùng lúc với 2b)
- Lấy danh sách ô bắt buộc của khung, chấm ✓ / ⚠ / ✗ (`content-requirements.md` §3).
- Trang để ra quyết định (khung Quyết định hoặc `goal: decide`): liệt kê 3–5 câu người duyệt sẽ hỏi, ghi vào `brief.objections`; câu nào nguồn không trả lời được mà có thể đổi quyết định là điều kiện chặn. Lõi lập luận không bị cắt theo độ dài (`skeletons/quyet-dinh.md`).
- Chạm một trong ba điều kiện chặn → gửi **phiếu thiếu thông tin** một lượt (tối đa 3 câu, mỗi câu: cần gì · vì sao · thiếu thì sao · mặc định), rồi dừng chờ trả lời. Không chạm → làm tiếp; ghi mọi ⚠ ✗ vào báo lại.

### 4. Storyboard
Lập bảng: bước · câu hỏi người đọc · tiêu đề (kết luận) · hình · nguồn · trạng thái.
- Mức high / ultra: gửi storyboard (kèm dòng cài đặt người đọc và danh sách thuật ngữ + bản dịch nếu đa ngữ), chờ duyệt. Ultra: sau khi duyệt storyboard, gửi bản nháp chữ ngôn ngữ chính để duyệt tiếp rồi mới dựng hình.
- Mức low / medium: không chờ; bảng rút gọn đưa vào báo lại.

### 5. Viết story.json
- Cấu trúc: `references/story-schema.md`. Hình: `references/visuals.md`. Quy tắc viết: `references/writing-rules.md` (đọc kỹ §1 về rò rỉ yêu cầu).
- Hình thức theo câu trả lời ở 2b: `references/formats.md`. Phong cách và bố cục: `references/styles.md`. Chọn `layout` cho từng bước theo nội dung, không để cả trang một kiểu; chọn hình đa dạng theo câu hỏi của từng bước, dùng lại cùng một hình qua các bước khi câu chuyện cần liền mạch.
- Mọi thông tin về người đọc, mức, mục đích chỉ nằm trong `brief`. Không câu nào trên trang nói về chính tài liệu hay người đọc.
- Tiêu đề mỗi bước là kết luận; đọc nối các tiêu đề phải ra cả câu chuyện.
- Bước nào không phải sự thật đã xác nhận: đặt `basis` + `note` cùng loại.
- Đa ngữ: viết xong ngôn ngữ chính, rà phép thử 2 câu, rồi mới dịch.
- Ví dụ mẫu đầy đủ: `examples/test-sec-rca.story.json`.

### 6. Build và tự kiểm
```bash
python3 SKILL_DIR/scripts/check.py story.json --render <workdir>/shots
python3 SKILL_DIR/scripts/build.py story.json -o <outdir>/<id>.html
```
- Sửa hết **lỗi**. Đọc từng **cảnh báo**: sửa, hoặc giữ có lý do (ghi vào báo lại nếu liên quan người đọc).
- Mở và xem `shots/sheet-desktop-<ngôn ngữ chính>.png` và `sheet-mobile-<ngôn ngữ chính>.png` (high/ultra: mọi ngôn ngữ). Tìm: chữ chồng hình, hình rỗng, bước không tự nói được ý. Script không bắt được những lỗi này.
- Rà lần cuối theo phép thử 2 câu (`writing-rules.md` §1); high/ultra rà từng câu.
- **Soát độc lập** (medium trở lên): làm theo `references/reviewer.md`. Người soát chỉ đọc `reader_view.py`, không đọc brief. Sửa các mục người soát nêu rồi chạy lại `check.py`.
- Không có playwright: chạy `check.py` không `--render`, ghi vào báo lại là chưa kiểm hiển thị.
- Slide hoặc video: chạy thêm `python3 SKILL_DIR/scripts/snap.py story.json -o <workdir>/snaps` để có ảnh từng bước và `manifest.json`, rồi làm theo `formats.md`.

### 7. Giao
- Trang (bấm từng bước, cuộn, 1 trang): có công cụ Artifact thì publish file HTML; không có thì đưa vào thư mục giao và trình bày bằng công cụ trình bày file.
- Slide, video: giao theo `formats.md` (loại Slides / Motion của công cụ Artifact nếu có; không có thì pptx hoặc trang tự chạy).
- Câu trả lời gồm: dòng mức (nếu chưa nói ở bước 2) · một câu nói trang là gì · **Báo lại** theo `references/report-back.md`. Không lặp lại nội dung trang trong chat.
- Không giao `story.json` trừ khi người dùng xin; giữ nó trong thư mục làm việc để sửa tiếp.

### 8. Sửa và học
- Người dùng yêu cầu sửa: sửa `story.json`, chạy lại bước 6, publish đè lên trang cũ (cùng link) nếu công cụ cho phép.
- Người dùng sửa theo kiểu có thể thành quy tắc ("quá nhiều chữ", "đang tự suy"): hỏi có ghi thành bài học không (`lessons.md`).

## Giới hạn của phiên bản này

- Word, PDF: chưa xuất trực tiếp; dùng skill tương ứng với ảnh và chữ từ `snap.py`. Trang 1 trang in được ra PDF từ trình duyệt.
- Hình tương tác (`calc`, `quiz`, `slider`) chỉ chạy trên trang HTML; trên slide/video là ảnh tĩnh.
- Tối đa 12 bước một trang; nhiều hơn thì đề xuất tách trang.
- Bản dịch máy (đặc biệt tiếng Nhật) luôn được ghi vào "cần xác nhận".

# Thư viện hình

Hình là phần chính của mỗi bước; chữ chỉ bổ sung điều hình không tự nói được. Chọn hình theo **câu hỏi của bước**, không theo sở thích. Cùng một câu chuyện nên dùng lại cùng một hình qua nhiều bước và để nó biến đổi (ví dụ cùng `grid` từ `build` → `sweep` → `focus` → `cursor`), người đọc không phải học hình mới.

Trạng thái dùng chung: `ok` · `bad` · `warn` · `info` · `muted` · `empty` (chấp nhận cả `miss`, `fail`, `catch`, `pending`… sẽ được quy về nhóm gần nhất).

## Chọn hình

| Câu hỏi của bước | Hình |
|---|---|
| Phạm vi, hiện tượng hàng loạt, ma trận đối tượng × thời gian / quyền / hạng mục | `grid` |
| Nhân quả theo thời gian, ai chuẩn bị cho cái gì, giai đoạn | `timeline` |
| Bao lâu, bao nhiêu, so với ngưỡng | `bars` |
| Ai làm gì, theo thứ tự nào, hệ thống nào gọi hệ thống nào | `flow` |
| Trước / sau, phương án A / B, đúng / nhầm | `compare` |
| Con số chính, hiện tại vs mục tiêu | `stats` |
| Việc cần làm, các bước tiếp theo | `list` |
| Giả thuyết → kết luận, điều kiện → đạt/không | `checks` |
| Ai gọi ai, theo thứ tự thời gian (API, tích hợp, quy trình nhiều bên) | `sequence` |
| Một đối tượng đi qua các trạng thái | `states` |
| Ma trận số liệu, mật độ, chỗ nóng | `heatmap` |
| Kéo để so trước / sau trên cùng một hình | `slider` |
| Người xem tự thử số liệu, công thức, ngưỡng | `calc` |
| Kiểm tra đã hiểu chưa | `quiz` |
| So nhiều phương án trên cùng tiêu chí | `matrix` |
| Không cái nào hợp | `custom` (SVG/HTML tĩnh tự vẽ) |

## grid

```json
{ "pattern": "grid", "rowCount": 10, "colCount": 16,
  "rows": ["tùy chọn: nhãn từng hàng"], "heads": ["06:00", "06:01"], "headSpan": 2,
  "cells": { "default": "ok", "rows": { "0": "warn" }, "cols": { "2": "bad" }, "list": [[3, 5, "bad"]] },
  "anim": "build | sweep | focus | cursor | static",
  "focus": { "cols": [2, 3, 13] },
  "cursor": { "from": 2, "during": "warn", "to": "ok", "label": "cursor" } }
```
- `build`: lưới hiện dần (giới thiệu phạm vi). `sweep`: lấp cột lần lượt (bình thường chạy thế nào). `focus`: làm mờ phần còn lại, khoanh cột bất thường (mặc định khoanh cột toàn `bad`). `cursor`: vạch quét qua, ô `bad` chuyển `during` rồi `to` (cách sửa / xử lý bù).
- Tối đa ~24 cột để đọc được trên điện thoại. Nhãn hàng dài sẽ bị cắt bằng dấu "…".
- Ít cột (ví dụ 3 × 4) thì engine giữ ô ở cỡ vừa, không phóng to. Nếu hàng là một khung có sức chứa cố định (16 chỗ), vẽ đủ sức chứa để người đọc thấy cả phần còn trống.

## timeline

```json
{ "pattern": "timeline", "topLabel": …, "bottomLabel": …, "offsetLabel": "+2 phút",
  "points":  [{ "label": "05:58:30", "status": "ok | skip | pending" }],
  "spans":   [{ "from": 0, "to": 2.9, "status": "bad", "label": … }],
  "targets": [{ "label": "06:00:30", "status": "ok | bad | empty" }],
  "links": [{ "from": 0, "to": 0 }],
  "reveal": "play | final", "showMiss": false,
  "skipLabel": "bỏ qua", "nowLabel": "bây giờ",
  "footnote": { "targets": [1, 2], "text": "không lượt nào gọi" } }
```
- Hàng trên là sự kiện, hàng dưới là hệ quả; mặc định điểm i nối mục tiêu i.
- `play`: vạch "bây giờ" chạy ngang, điểm `ok` bắn mũi tên xuống, điểm `skip` bị gạch. `spans` dài theo vạch (đơn vị = khoảng giữa 2 điểm).
- `showMiss: true`: hiện mũi tên đứt đỏ từ điểm bị bỏ và mục tiêu `bad`. Thường để `false` ở nhịp "kích hoạt", `true` với `reveal: final` ở nhịp "hậu quả".
- Tối đa 7 điểm. Bỏ `targets` nếu chỉ cần dòng sự kiện.

## bars

```json
{ "pattern": "bars", "max": 100, "limit": { "value": 30, "label": "giới hạn 30 giây" }, "together": false,
  "rows": [{ "label": "Tuần tự", "valueLabel": "100 giây", "value": 100, "blocks": 20,
             "status": "auto | ok | bad | warn", "anim": "blocks | grow | static", "dim": false, "at": 0.4 }] }
```
- `blocks`: chia thanh thành ô (mỗi ô một lần gọi/một đơn vị); `status: auto` tô đỏ phần vượt `limit`.
- Hàng chạy lần lượt; đặt cùng `at` (hoặc `together: true`) để các hàng chạy song song. `static` + `dim` để giữ hàng cũ làm mốc so sánh.

## flow

```json
{ "pattern": "flow", "lanes": ["Scheduler", "HiveStack", "DB"],
  "nodes": [{ "id": "a", "lane": 0, "col": 0, "text": "Mỗi 30 giây", "sub": "dòng phụ", "status": "info" }],
  "edges": [{ "from": "a", "to": "b", "label": "gọi VAST", "status": "ok" }],
  "highlight": ["b"], "order": ["a", "b", "c"] }
```
- `lanes` tùy chọn (bỏ = một làn). Mỗi cột giữ tối thiểu ~118px để chữ không bị ngắt giữa từ; màn hình hẹp hơn thì sơ đồ cuộn ngang trong khung riêng.
- Có làn và từ 4 cột trở lên: check.py cảnh báo vì người xem điện thoại phải cuộn. Ưu tiên ≤ 3 cột; nhánh điều kiện đơn giản (đạt → lưu, không đạt → dừng) thường rõ hơn khi viết bằng `checks`.
- Cạnh `status: bad` vẽ đứt nét. `highlight` làm nổi nút đang nói tới; dùng cùng flow qua nhiều bước, chỉ đổi `highlight` và `status`.

## compare

```json
{ "pattern": "compare",
  "left":  { "title": "Trước", "items": [{ "text": "…", "status": "same" }] },
  "right": { "title": "Sau",   "items": [{ "text": "…", "status": "changed | new | removed" }] } }
```

## stats

```json
{ "pattern": "stats", "items": [{ "label": "Hiện tại", "value": "130/160", "status": "bad", "note": "…" },
                                { "label": "Tỷ lệ", "value": { "from": 0, "to": 81.3, "decimals": 1, "suffix": "%" }, "status": "warn" }] }
```

## list

```json
{ "pattern": "list", "title": "Việc cần làm", "items": [{ "text": "…", "owner": "Dev", "due": "15/10" }] }
```
Không tự đặt `owner`, `due` khi nguồn không có.

## checks

```json
{ "pattern": "checks", "items": [{ "text": "HiveStack trả HTTP 200", "verdict": "Loại trừ", "status": "ok | key | warn" }] }
```
`key` = kết luận chính (tô đỏ). Cũng có thể đặt `checks` trực tiếp trong bước để hiện ở cột chữ.

## sequence

```json
{ "pattern": "sequence", "participants": [{ "id": "s", "label": "Scheduler" }, { "id": "h", "label": "HiveStack" }],
  "messages": [{ "from": "s", "to": "h", "label": "gọi VAST" }, { "from": "h", "to": "s", "label": "trả quảng cáo", "status": "ok" },
               { "from": "s", "to": "s", "label": "tự xử lý" }] }
```
Tối đa ~5 bên, nhãn ngắn. Hợp `layout: "hero"`.

## states

```json
{ "pattern": "states", "lanes": ["Xử lý", "Kết quả"],
  "states": [{ "id": "w", "label": "Chờ", "row": 0, "col": 0, "status": "info" }, { "id": "ok", "label": "Completed", "row": 1, "col": 1, "status": "ok" }],
  "transitions": [{ "from": "w", "to": "ok", "label": "thành công" }],
  "path": ["w", "ok"] }
```
`path` cho vạch sáng đi qua các trạng thái theo thứ tự; `current` để đánh dấu một trạng thái. Bố cục giống `flow` (≤ 3–4 cột).

## heatmap

```json
{ "pattern": "heatmap", "rows": ["MH 1", "MH 2"], "cols": ["06:00", "06:01"], "values": [[2, 0], [2, 0]],
  "min": 0, "max": 2, "scale": "good-high | good-low | neutral",
  "format": { "decimals": 0, "suffix": "" }, "highlight": { "cells": [[0, 1]] } }
```
Ô có số và màu theo giá trị. `good-high`: cao là tốt (xanh), thấp là xấu (đỏ). Tối đa ~12 cột.

## slider

```json
{ "pattern": "slider", "before": { "pattern": "grid", … }, "after": { "pattern": "grid", … },
  "beforeLabel": "Hiện tại 130/160", "afterLabel": "Mục tiêu 160/160", "start": 0.5 }
```
Hai hình cùng loại, cùng kích thước; người xem kéo để so. Nếu "sau" là mục tiêu hoặc đề xuất, bước phải có nhãn `target`/`proposal`.

## calc

```json
{ "pattern": "calc",
  "inputs": [{ "id": "n", "label": "Số màn hình", "min": 1, "max": 60, "value": 10, "step": 1, "unit": "", "decimals": 0 }],
  "outputs": [{ "label": "Một lượt mất", "expr": "ceil(n*2/w)*t", "unit": "giây", "decimals": 0,
                "status": [{ "if": "ceil(n*2/w)*t <= 30", "state": "ok" }, { "if": "ceil(n*2/w)*t > 30", "state": "bad" }] }],
  "bars": { "max": 120, "limit": { "value": 30, "label": "30 giây" }, "rows": [{ "label": "Một lượt", "valueExpr": "min(120, ceil(n*2/w)*t)" }] } }
```
- Biểu thức chỉ gồm số, `id` của input, `+ - * / %`, so sánh, `&& ||`, `min max round floor ceil abs`. check.py báo lỗi nếu sai cú pháp hoặc dùng tên lạ.
- Công thức phải lấy từ nguồn. Giá trị mặc định là giả định thì bước phải có nhãn `assumption`.

## quiz

```json
{ "pattern": "quiz", "questions": [{ "q": "Chọn đáp án đúng", "options": ["…", "…", "…"], "answer": 1, "explain": "…" }] }
```
Hỏi đúng ý chính của trang, không hỏi mẹo. Đặt câu hỏi ở tiêu đề bước, `layout: "center"`.

## matrix

```json
{ "pattern": "matrix", "cols": ["Giữ nguyên", "Phương án A", "Phương án B"], "recommend": 1,
  "rows": [{ "label": "Chi phí", "cells": [{ "text": "0" }, { "text": "21–34,5 PD", "status": "ok" }, { "text": "Chưa ước lượng", "status": "warn" }] }] }
```
- Cột là phương án, hàng là tiêu chí; ô có màu theo `status`. `recommend` đánh dấu cột đề xuất (bước nên có nhãn `proposal`).
- Trên điện thoại tự chuyển thành mỗi phương án một thẻ. Tối đa ~4 phương án × 6 tiêu chí.

## custom

```json
{ "pattern": "custom", "html": "<svg viewBox='0 0 640 300'>…</svg>" }
```
- Tĩnh, không script, không thuộc tính `on*` (check.py chặn). Dùng biến màu `var(--ok)`, `var(--bad)`, `var(--ink)`, `var(--muted)`, `var(--line)`, `var(--surface)` để tự theo dark mode.
- Ảnh màn hình người dùng gửi: nhúng `<img src='data:image/png;base64,…' style='max-width:100%'>`; trang phải dưới 16 MB.
- Chỉ dùng khi 8 hình trên thật sự không diễn đạt được; ghi lý do vào báo lại.

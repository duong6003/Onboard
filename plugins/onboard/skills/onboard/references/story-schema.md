# Cấu trúc story.json

Story là nguồn gốc duy nhất của trang. Sửa nội dung = sửa story rồi build lại; mọi ngôn ngữ cập nhật cùng lúc.

## Khung tổng

```json
{
  "version": 1,
  "id": "slug-ngan-khong-dau",
  "langs": ["vi", "en", "ja"],
  "defaultLang": "vi",
  "theme": "onboard",
  "format": "stepper | scroll | onepage",
  "style": "clean | dark | sketch | editorial",
  "autoplay": false,
  "brief": { … },
  "lint": { "allow": ["cụm hợp lệ trong ngữ cảnh"] },
  "meta": { "title": …, "subtitle": …, "footer": … },
  "steps": [ … ]
}
```

- `langs`: ngôn ngữ hiển thị; nút chuyển ngôn ngữ chỉ hiện khi ≥ 2. Hỗ trợ sẵn chữ giao diện cho vi, en, ja (ngôn ngữ khác dùng chữ giao diện tiếng Anh).
- `theme`: `"onboard"` (cam #D8501A, mặc định), `"neutral"`, hoặc `{ "brand": "#RRGGBB" }` theo thương hiệu khách. Chỉ đổi màu khung, không đổi màu ngữ nghĩa.
- `id`: dùng để nhớ ngôn ngữ người xem đã chọn.
- `format`, `autoplay`: xem `formats.md`. `style`: xem `styles.md`.

## Chữ đa ngôn ngữ

Mọi chữ hiển thị là chuỗi (một ngôn ngữ) hoặc object theo mã ngôn ngữ:
`{ "vi": "…", "en": "…", "ja": "…" }`. Story nhiều ngôn ngữ thì object phải đủ mọi ngôn ngữ (check.py báo lỗi nếu thiếu). Mã, giờ, số, tên riêng để chuỗi thường.

Chữ cho phép `<b>`, `<strong>`, `<em>`, `<i>`, `<code>`, `<br>`; mọi thẻ khác bị hiển thị dạng chữ.

## brief (không bao giờ ra HTML)

```json
"brief": {
  "recipient": "Khách hàng phía DOOH và QC",
  "sharing": "external",
  "level": "high",
  "situation": "Sự cố / RCA",
  "skeleton": "su-viec",
  "purpose": "Hiểu vì sao thiếu slot và đồng ý hướng sửa",
  "audience": { "context": "known", "depth": "flow", "goal": "decide", "tone": "formal", "length": "5min" },
  "customOrder": ["chỉ khi skeleton = custom"],
  "objections": [{ "q": "Không làm thì sao?", "step": 2 }, { "q": "Phương án X tốn bao nhiêu?", "gap": "Chưa có ước lượng" }]
}
```

`objections`: bắt buộc với khung Quyết định hoặc `goal: decide` ở mức medium trở lên (xem `skeletons/quyet-dinh.md`).

Bắt buộc: `recipient`, `sharing` (`internal` | `external`), `level` (`low` | `medium` | `high` | `ultra`), `skeleton`, `purpose`.

## meta

`title` (bắt buộc, cũng là `<title>`), `subtitle` (phạm vi, thời gian, môi trường), `footer` (tùy chọn, ví dụ "Số liệu tính đến 10/10/2026").

## steps[]

| Trường | Bắt buộc | Ý nghĩa |
|---|---|---|
| `title` | Có | Kết luận của bước. Có thể chứa `{count}` để hiện số chạy từ `count.from` tới `count.to` |
| `count` | | `{ "from": 96, "to": 130, "decimals": 0, "prefix": "", "suffix": "" }` |
| `body` | | Tối đa 2 câu |
| `chips` | | Tối đa 2: `{ "kind": "ok" \| "warn" \| "bad" \| "info", "text": … }` (bỏ `kind` = trung tính) |
| `checks` | | Bảng loại trừ trong cột chữ: `{ "text", "verdict", "status": "ok" \| "key" \| "warn" }` |
| `basis` | | `fact` (mặc định) · `illustration` · `assumption` · `unconfirmed` · `proposal` · `target` |
| `note` / `notes` | Khi `basis` khác `fact` | `{ "type": giống basis hoặc "source", "text": … }` hiện thành dòng nhãn |
| `sources` | Mức high/ultra với bước `fact` | Danh sách nguồn (không hiện trên trang, dùng cho báo lại và kiểm tra) |
| `layout` | | `split` (mặc định) · `hero` · `center` (xem `styles.md`) |
| `alt` | Nên có | Mô tả hình cho trình đọc màn hình |
| `visual` | | Một pattern, hoặc mảng pattern xếp dọc (xem `visuals.md`). Mỗi pattern có thể kèm `legend`, `caption` |

`legend`: `[{ "state": "ok", "text": …, "shape": "dot" | "ring" }]`. `caption`: một dòng chữ nhỏ dưới hình, nói kết luận hoặc đơn vị, không dẫn vào hình.

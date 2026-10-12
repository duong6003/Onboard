# Người đọc: 5 núm chỉnh và ranh giới chia sẻ

Vai trò (khách, QC, người mới…) không gắn cứng với cách trình bày. Người đọc được mô tả bằng 5 núm; vai trò chỉ là bộ cài sẵn. Người dùng vặn lại núm nào cũng được ("coi khách như người mới", "BA nhưng đọc để kiểm tra").

## 1. Năm núm

| Núm (`brief.audience`) | Giá trị | Ảnh hưởng |
|---|---|---|
| `context` độ quen bối cảnh | `new` · `known` · `expert` | `new`: thêm bước bối cảnh đầu trang, giải thích thuật ngữ khi dùng lần đầu. `expert`: bỏ bước bình thường, vào thẳng điểm khác |
| `depth` độ sâu kỹ thuật | `conclusion` · `flow` · `detail` | Mức chi tiết của hình: kết luận + số chính / luồng xử lý / dữ liệu, điều kiện, trường hợp biên |
| `goal` mục đích sau khi đọc | `understand` · `decide` · `verify` · `operate` · `prepare` | Bước cuối và phần nhấn mạnh: decide → phương án + cần quyết gì; verify → điều kiện, tiêu chí đạt; operate → thao tác; prepare → việc phải làm, hạn |
| `tone` giọng | `internal` · `formal` | internal: thẳng, ngắn. formal: lịch sự, không nêu cá nhân, không đổ lỗi |
| `length` thời lượng | `1min` · `5min` · `deep` | Số bước: 3–5 · 6–10 · tới 12 |

## 2. Bộ cài sẵn

| Vai trò | context | depth | goal | tone | length |
|---|---|---|---|---|---|
| Khách hàng | known | conclusion | decide | formal | 5min |
| Lãnh đạo | known | conclusion | decide | formal | 5min |
| PM | known | flow | prepare | internal | 5min |
| BA / Dev | known | detail | understand | internal | deep |
| QC | known | detail | verify | internal | deep |
| Vận hành / CS | known | flow | operate | internal | 5min |
| Người mới | new | flow | understand | internal | 5min |

Với `goal: decide`, `length` chỉ rút gọn chữ và gộp bước; lõi lập luận của khung Quyết định không bị cắt (xem `skeletons/quyet-dinh.md`). Ngắn cho lãnh đạo nghĩa là bước 1 đủ để quyết, không phải bỏ lý lẽ.

Kết hợp ví dụ:
- "Khách như người mới" = bộ Khách hàng, `context: new`. Thêm bước bối cảnh và thuật ngữ, vẫn trang trọng, vẫn kết thúc bằng điều cần quyết.
- "BA như QC" = bộ BA, `goal: verify`. Thêm điều kiện, trường hợp biên, tiêu chí đạt; vẫn giữ độ sâu dữ liệu.

## 3. Ranh giới chia sẻ: không vặn được

Cách **giải thích** chỉnh tự do. Cái gì được **hiện** thì theo người nhận thật (`brief.sharing`), không theo vai được gán.

`sharing: external` (khách, đối tác, cơ quan):
- Không hiện: log thô, tên người, ai làm sai, chi phí/giá nội bộ, tranh luận nội bộ, đường dẫn và host nội bộ, token, IP.
- Chạy `scripts/redact.py` trên nguồn trước khi trích. check.py báo lỗi nếu còn dữ liệu nhạy cảm.
- Nói về nguyên nhân bằng cơ chế ("scheduler bỏ qua lượt"), không bằng con người.

`sharing: internal`: được hiện chi tiết kỹ thuật và log cần thiết, vẫn không đưa thông tin cá nhân không liên quan.

## 4. Hiển thị cài đặt

Cài đặt là yêu cầu, không phải nội dung: không bao giờ xuất hiện trên trang. Chỉ hiện trong câu trả lời, một dòng:

`Người nhận: Khách · Bối cảnh: đã nắm · Kỹ thuật: kết luận · Mục đích: quyết định · Trang trọng · ~5 phút`

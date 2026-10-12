# Khung xương: Trạng thái (báo cáo tiến độ, kết quả UAT, rủi ro/vấn đề, SLA)

Người đọc cần: nắm tình hình và biết có gì cần mình can thiệp.

## Câu hỏi người đọc, theo thứ tự

1. Tổng thể đang tốt hay có vấn đề? (một câu + số chính)
2. Mục tiêu / mốc là gì, đang ở đâu?
3. Rủi ro, vấn đề nào cần chú ý, ai phụ trách?
4. Bước tiếp theo, cần ai hỗ trợ gì?

## Ô bắt buộc

| Ô | Nếu thiếu |
|---|---|
| Mục tiêu / mốc | Chặn |
| Tiến độ thực tế có số, tại thời điểm nào | Chặn; không ước lượng phần trăm |
| Rủi ro + người phụ trách | Thiếu người: ghi "chưa phân công" |
| Bước tiếp theo + hạn | Báo lại nếu thiếu hạn |

## Kế hoạch bước gợi ý (3–6 bước)

| Bước | Ý | Hình gợi ý |
|---|---|---|
| 1 | Tổng thể | `stats` |
| 2 | Tiến độ theo hạng mục / giai đoạn | `bars` hoặc `grid` (hạng mục × tuần) |
| 3 | Rủi ro, vấn đề | `checks` (status `warn`/`key`) |
| 4 | Bước tiếp theo | `list` có `owner`, `due` |

Luôn ghi "số liệu tính đến ngày …" trong `meta.subtitle`.

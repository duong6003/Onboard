# Khung xương: Sự việc (sự cố, RCA, báo tin xấu, lỗi UAT)

Người đọc cần: tin và yên tâm. Đọc xong phải trả lời được: chuyện gì xảy ra, vì sao, đã/ sẽ xử lý thế nào, mình cần làm gì.

## Câu hỏi người đọc, theo thứ tự

1. Bình thường hệ thống chạy thế nào? (bỏ nếu `context: expert`)
2. Chuyện gì đã xảy ra, phạm vi bao lớn?
3. Vì sao? (cơ chế, tách 3 nhịp nếu theo thời gian)
4. Đã loại trừ những khả năng nào, dựa trên bằng chứng gì?
5. Xử lý thế nào, phòng ngừa thế nào?
6. Trạng thái hiện tại và việc tiếp theo (ai, khi nào)?

## Ô bắt buộc

| Ô | Nếu thiếu |
|---|---|
| Hiện tượng + số liệu (kỳ vọng / thực tế / thiếu) | Chặn nếu gửi ra ngoài; không bịa |
| Phạm vi: thời gian, đối tượng, môi trường | Chặn |
| Cơ chế bình thường | Suy từ cấu hình/tài liệu, nhãn `unconfirmed` nếu không có nguồn thẳng |
| Nguyên nhân + trạng thái xác nhận | Chưa chốt: nhãn `unconfirmed`, đưa vào "cần xác nhận" |
| Bằng chứng loại trừ | Thiếu: bỏ bước loại trừ, ghi "chưa kiểm" ở báo lại |
| Cách xử lý | Tự đề xuất, nhãn `proposal` |
| Việc tiếp theo, người phụ trách, hạn | Thiếu người/hạn: ghi việc, bỏ trống người/hạn, báo lại |

## Kế hoạch bước gợi ý (6–10 bước)

| Bước | Ý | Hình gợi ý |
|---|---|---|
| 1 | Phạm vi: bao nhiêu đối tượng × bao nhiêu mốc | `grid` anim `build` |
| 2 | Bình thường chạy thế nào | `grid` `sweep` hoặc `flow` |
| 3–5 | Nhân quả theo 3 nhịp: bối cảnh → kích hoạt → hậu quả | `timeline` play → play có skip → `reveal: final` |
| 6 | Kết quả thực tế + loại trừ | `grid` `focus` + `checks` trong text, `count` ở tiêu đề |
| 7 | Nguyên nhân gốc | `bars` với `limit`, hoặc `flow` chỉ ra điểm nghẽn |
| 8–9 | Cách sửa (mỗi cách một bước) | `grid` `cursor`, `bars` song song, `compare` trước/sau |
| 10 | Kết luận + việc tiếp theo | `stats` + `list` |

Ví dụ hoàn chỉnh: `examples/test-sec-rca.story.json`.

## Lỗi hay gặp

- Kể nguyên nhân bằng con người ("dev quên…") thay vì cơ chế. Với khách luôn kể bằng cơ chế.
- Gộp hiện tượng và nguyên nhân vào một bước.
- Đưa số liệu suy ra (ví dụ thời lượng ước tính) như sự thật.

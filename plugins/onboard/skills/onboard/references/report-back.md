# Báo lại cho người soạn

Luôn có, ở mọi mức. Nằm trong câu trả lời ở chat, **không bao giờ nằm trên trang** (đó là yêu cầu, không phải nội dung).

## Năm mục

1. **Nguồn đã dùng**: sự thật trên trang lấy từ đâu (tên file, đoạn hội thoại, connector).
2. **Giả định đã tự đặt**: ở bước nào, trên trang đã gắn nhãn gì.
3. **Cần xác nhận trước khi gửi**: xếp theo ưu tiên, mỗi mục kèm lý do ngắn.
4. **Đã lược bỏ hoặc rút gọn**: bỏ gì, vì sao (ranh giới chia sẻ, giới hạn độ dài, thiếu nguồn).
5. **Cài đặt đã dùng**: một dòng người đọc (xem `audiences.md`) + mức + khung xương. Kèm khuyến nghị đổi mức nếu có.

## Độ dài theo mức

| Mức | Nội dung |
|---|---|
| low | Chỉ mục 2 và 3, vài dòng |
| medium | Đủ 5 mục; thêm bảng storyboard rút gọn (bước · ý · hình) vì không có bước duyệt |
| high | Đủ 5 mục; mục 1 ghi nguồn cho từng con số |
| ultra | Như high + checklist trước khi gửi (bản dịch đã người bản ngữ đọc, số liệu đã đối chiếu, đã che dữ liệu nhạy cảm, đã đúng người nhận) |

Thêm cuối cùng nếu có: **Đề xuất bài học** (xem `lessons.md`).

## Ví dụ (medium, RCA gửi khách)

> **Báo lại**
> - **Nguồn:** bảng kết quả DB, HTTP trace và log Serilog bạn gửi.
> - **Giả định:** lượt 05:58:30 chạy ~90 giây (bước 4), đã gắn nhãn "Minh họa".
> - **Cần xác nhận trước khi gửi khách:**
>   1. 5 giây/lần bị tốn ở đâu: trang đang ghi là "đang được tìm"; nếu dev đã tìm ra thì cập nhật bước 7.
>   2. Bản tiếng Nhật: nên có người quen thuật ngữ phía khách đọc lại.
> - **Đã lược:** chi tiết log nội bộ và tên người phụ trách, vì người nhận là khách.
> - **Cài đặt:** Khách · đã nắm · kết luận · quyết định · trang trọng · ~5 phút · mức medium · khung Sự việc. Nên chạy lại mức high trước khi gửi khách.

# Danh mục tình huống

Mỗi tình huống chỉ là một dòng: dùng khung xương nào, ô nào đặc biệt quan trọng, hình gợi ý. Thêm tình huống mới = thêm một dòng. Không thấy tình huống phù hợp: chọn khung gần nhất, ghi vào báo lại là "tình huống mới, đề xuất thêm vào danh mục".

| Nhóm | Tình huống | Khung xương | Ô quan trọng | Hình gợi ý |
|---|---|---|---|---|
| Khởi động / yêu cầu | Giới thiệu giải pháp | giai-thich | Vấn đề của khách, giá trị | flow, compare |
| | Hiện trạng → mong muốn (as-is / to-be) | thay-doi | Điểm đau hiện tại có số | compare, flow |
| | Phạm vi và ngoài phạm vi | quyet-dinh | Danh sách hạng mục, căn cứ hợp đồng | checks, compare |
| Phân tích / thiết kế | Business rule, công thức tính | giai-thich | Quy tắc gốc + ví dụ số | bars, grid, stats |
| | Quy trình nghiệp vụ (swimlane) | giai-thich | Vai trò, bước, điều kiện rẽ nhánh | flow có lanes |
| | Luồng tích hợp hệ thống (API, VAST, OpenRTB) | giai-thich | Thứ tự gọi, dữ liệu, thời điểm | flow có lanes, timeline |
| | Phân quyền RBAC | giai-thich | Vai trò × quyền | grid (hàng = vai trò, cột = quyền) |
| | Mô hình dữ liệu | giai-thich | Thực thể, quan hệ chính | flow |
| | Luồng màn hình | huong-dan | Màn hình, hành động | flow một làn |
| | Kiến trúc | giai-thich | Thành phần, luồng dữ liệu | flow có lanes |
| Phát triển | Handoff BA → Dev | giai-thich (`depth: detail`) | Quy tắc, trường hợp biên, tiêu chí nghiệm thu | flow, checks |
| | Quyết định kỹ thuật (trade-off) | quyet-dinh | Phương án, tiêu chí | compare, bars |
| | CR và tác động | quyet-dinh | Chi phí, thời gian, phạm vi | compare, bars |
| Kiểm thử / nghiệm thu | Kế hoạch test | huong-dan (`goal: verify`) | Phạm vi test, tiêu chí đạt | checks, grid |
| | Kết quả UAT | trang-thai | Số case đạt/lỗi, lỗi chặn | stats, grid, checks |
| | Tiêu chí nghiệm thu | huong-dan | Tiêu chí đo được | checks |
| Phát hành / triển khai | Release notes, tính năng mới | thay-doi | Trước/sau, ai bị ảnh hưởng | compare, list |
| | Go-live theo giai đoạn, rollback | thay-doi | Giai đoạn, mốc, phương án quay lui | timeline, list |
| | Đào tạo người dùng | huong-dan | Thao tác thật | flow, custom (ảnh) |
| Vận hành / hỗ trợ | Sự cố / RCA | su-viec | Số liệu, phạm vi, bằng chứng | grid, timeline, bars |
| | Runbook | huong-dan (`goal: operate`) | Dấu hiệu, thao tác, leo thang | flow, checks |
| | Hiệu năng, SLA | trang-thai | Số đo, ngưỡng | bars có limit, stats |
| | Bảo mật, pentest | trang-thai hoặc quyet-dinh | Phát hiện, mức độ, kế hoạch xử lý | checks, stats |
| Quản lý dự án | Báo cáo tiến độ | trang-thai | Mốc, % thực tế, rủi ro | stats, bars, checks |
| | Rủi ro, vấn đề (RAID) | trang-thai | Mức độ, người phụ trách | checks, list |
| | RACI, phân công | giai-thich | Việc × vai trò | grid |
| | Roadmap | thay-doi | Giai đoạn, mốc | timeline |
| | Retrospective | su-viec | Điều tốt, điều chưa tốt, hành động | checks, list |
| Phòng ban | Onboard thành viên mới | giai-thich (`context: new`) | Bối cảnh, hệ thống, ai làm gì | flow, grid, list |
| | Quy trình làm việc của phòng | giai-thich | Đầu vào, các bước, đầu ra | flow có lanes |
| | Chuẩn tài liệu, template | huong-dan | Quy tắc + ví dụ đúng/sai | compare |
| | Bàn giao khi đổi người | huong-dan | Việc đang dở, đầu mối, tài khoản | list, checks |
| Giao tiếp stakeholder | Báo tin xấu (trễ, lỗi, vượt chi phí) | su-viec | Tác động, phương án, cam kết mới | stats, timeline, list |
| | Xin quyết định | quyet-dinh | Điều cần quyết, hạn | compare, checks |
| | Biên bản họp, việc cần làm | trang-thai | Quyết định đã chốt, việc + người + hạn | checks, list |
| | Giải thích cho người không chuyên | giai-thich (`depth: conclusion`) | Ví dụ đời thường đúng bản chất | flow, compare |
| | Đàm phán phạm vi | quyet-dinh | Căn cứ hợp đồng, phương án | compare, checks |

## Khung xương tùy biến

Tình huống đặc biệt cần trình tự riêng (ví dụ "kết luận trước, bằng chứng sau"): đặt `brief.skeleton: "custom"` và ghi trình tự câu hỏi vào `brief.customOrder`. Vẫn áp dụng đủ quy tắc viết, nhãn trung thực và chấm độ đủ.

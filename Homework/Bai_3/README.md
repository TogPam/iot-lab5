# Bài 3 về nhà: Node-RED Dashboard cục bộ

Nhận dữ liệu MQTT bằng Node-RED và hiển thị CPU/RAM bằng Gauge, Chart cùng bảng dữ liệu sensor.

## Tệp của bài

- `flows.json`
- `settings.js`
- `chay.ps1`

## Cách chạy

Các lệnh dưới đây chạy từ thư mục gốc `C:\IOT\lab5`. Có thể chạy file PowerShell bằng đường dẫn tuyệt đối từ thư mục khác.

```powershell
powershell -ExecutionPolicy Bypass -File Ve_nha\Bai_3\chay.ps1
```

## Kết quả cần quan sát

Dashboard tại http://127.0.0.1:1880/dashboard/gateway có hai Gauge CPU/RAM, biểu đồ lịch sử và bảng hai cảm biến mô phỏng.

## Ghi chú

chay.ps1 khởi động cả hệ thống nếu chưa chạy, sau đó in địa chỉ dashboard. Flow trong thư mục này là bản để xem/import; flow chạy thực nằm ở node-red/flows.json và được sinh đồng thời bởi scripts/build_flow.py. Node-RED dùng tài khoản dashboard, chỉ có quyền đọc metrics/report. Khi import sang máy khác cần nhập tài khoản broker rồi Deploy. Môi trường chạy nằm chung ở node-red/ để tránh cài lặp thư viện.

Cài môi trường dùng chung: `scripts/setup.ps1`. Hướng dẫn tổng thể: [README gốc](../../README.md). Báo cáo: [Bao_cao_Lab_5.docx](../../Bao_cao/Bao_cao_Lab_5.docx).

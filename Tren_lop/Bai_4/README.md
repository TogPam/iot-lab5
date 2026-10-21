# Bài 4: Publish thông số CPU và RAM mỗi 5 giây

Đọc CPU/RAM thật bằng psutil, đóng gói JSON và gửi gateway/system/metrics định kỳ.

## Tệp của bài

- `metrics_publisher.py`
- `chay.ps1`

## Cách chạy

Các lệnh dưới đây chạy từ thư mục gốc `C:\IOT\lab5`. Có thể chạy file PowerShell bằng đường dẫn tuyệt đối từ thư mục khác.

```powershell
powershell -ExecutionPolicy Bypass -File Tren_lop\Bai_4\chay.ps1

.\.venv\Scripts\python.exe scripts\mqtt_cli.py sub -t gateway/system/metrics -v
```

## Kết quả cần quan sát

Một bản tin JSON mỗi 5 giây gồm cpu_percent, ram_percent, ram_used_bytes, ram_total_bytes, gateway_id và timestamp.

## Ghi chú

Cần broker bảo mật đang chạy. Hệ thống demo đã có một publisher; chỉ chạy thêm nếu muốn thử riêng. Chạy hữu hạn: python -m Tren_lop.Bai_4.metrics_publisher --count 3. Timestamp dùng UTC; đây là số đo thật của máy Windows, không phải số liệu cảm biến mô phỏng.

Cài môi trường dùng chung: `scripts/setup.ps1`. Hướng dẫn tổng thể: [README gốc](../../README.md). Báo cáo: [Bao_cao_Lab_5.docx](../../Bao_cao/Bao_cao_Lab_5.docx).

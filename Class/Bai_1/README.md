# Bài 1: Cài đặt và cấu hình Mosquitto Local Broker

Cài đặt broker MQTT cục bộ trên gateway và cấu hình địa chỉ lắng nghe.

## Tệp của bài

- `mosquitto.conf`
- `chay.ps1`

## Cách chạy

Các lệnh dưới đây chạy từ thư mục gốc `C:\IOT\lab5`. Có thể chạy file PowerShell bằng đường dẫn tuyệt đối từ thư mục khác.

```powershell
powershell -ExecutionPolicy Bypass -File scripts\stop.ps1

powershell -ExecutionPolicy Bypass -File Tren_lop\Bai_1\chay.ps1
```

## Kết quả cần quan sát

Broker mở cổng 1883 trên 127.0.0.1; sẵn sàng nhận kết nối MQTT trên máy này.

## Ghi chú

Chế độ anonymous chỉ dùng cho bài 1–2 trên loopback. Dừng hệ thống demo trước khi mở broker này để tránh trùng cổng. Kết thúc bằng Ctrl+C, rồi chạy scripts/start.ps1 để trở lại bản bảo mật. Trên Linux, dùng sudo apt install mosquitto mosquitto-clients và sudo systemctl status mosquitto.

Cài môi trường dùng chung: `scripts/setup.ps1`. Hướng dẫn tổng thể: [README gốc](../../README.md). Báo cáo: [Bao_cao_Lab_5.docx](../../Bao_cao/Bao_cao_Lab_5.docx).

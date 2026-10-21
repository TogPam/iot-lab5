# Bài 2: Kiểm tra MQTT Client bằng dòng lệnh

Dùng mosquitto_sub và mosquitto_pub để kiểm tra truyền nhận bản tin tại gateway/test.

## Tệp của bài

- `nhan.ps1`
- `gui.ps1`

## Cách chạy

Các lệnh dưới đây chạy từ thư mục gốc `C:\IOT\lab5`. Có thể chạy file PowerShell bằng đường dẫn tuyệt đối từ thư mục khác.

```powershell
powershell -ExecutionPolicy Bypass -File Tren_lop\Bai_2\nhan.ps1

powershell -ExecutionPolicy Bypass -File Tren_lop\Bai_2\gui.ps1
```

## Kết quả cần quan sát

Terminal subscriber hiển thị gateway/test Hello Local MQTT.

## Ghi chú

Chạy broker anonymous của bài 1 trước. Mở hai terminal, chạy nhan.ps1 trước rồi gui.ps1. Kết thúc subscriber bằng Ctrl+C. Nếu dùng broker bảo mật đang chạy, xem lệnh scripts/mqtt_cli.py trong README gốc.

Cài môi trường dùng chung: `scripts/setup.ps1`. Hướng dẫn tổng thể: [README gốc](../../README.md). Báo cáo: [Bao_cao_Lab_5.docx](../../Bao_cao/Bao_cao_Lab_5.docx).

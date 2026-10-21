# Bài 3: Cài Paho-MQTT và kiểm tra kết nối Python

Tạo môi trường ảo Python, cài Paho-MQTT và xác minh callback kết nối broker thành công.

## Tệp của bài

- `check_connection.py`
- `chay.ps1`

## Cách chạy

Các lệnh dưới đây chạy từ thư mục gốc `C:\IOT\lab5`. Có thể chạy file PowerShell bằng đường dẫn tuyệt đối từ thư mục khác.

```powershell
powershell -ExecutionPolicy Bypass -File scripts\start.ps1

powershell -ExecutionPolicy Bypass -File Tren_lop\Bai_3\chay.ps1
```

## Kết quả cần quan sát

CONNECTED 127.0.0.1:1883 và Ket noi MQTT thanh cong.

## Ghi chú

Chỉ chạy start.ps1 nếu hệ thống chưa chạy. Paho dùng CallbackAPIVersion.VERSION2; Session ở gateway/common.py chờ CONNACK trước khi xác nhận thành công. Truyền --anonymous khi thử broker bài 1. Cài thư viện: .venv/Scripts/python.exe -m pip install -r requirements.txt.

Cài môi trường dùng chung: `scripts/setup.ps1`. Hướng dẫn tổng thể: [README gốc](../../README.md). Báo cáo: [Bao_cao_Lab_5.docx](../../Bao_cao/Bao_cao_Lab_5.docx).

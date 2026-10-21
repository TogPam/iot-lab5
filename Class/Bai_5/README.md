# Bài 5: Subscribe lắng nghe lệnh điều khiển

Đăng ký wildcard gateway/command/# và in các lệnh nhận được trong callback on_message.

## Tệp của bài

- `command_subscriber.py`
- `chay.ps1`
- `gui_lenh.ps1`

## Cách chạy

Các lệnh dưới đây chạy từ thư mục gốc `C:\IOT\lab5`. Có thể chạy file PowerShell bằng đường dẫn tuyệt đối từ thư mục khác.

```powershell
powershell -ExecutionPolicy Bypass -File Tren_lop\Bai_5\chay.ps1

powershell -ExecutionPolicy Bypass -File Tren_lop\Bai_5\gui_lenh.ps1
```

## Kết quả cần quan sát

Subscriber in COMMAND, thời gian, topic gateway/command/led và nội dung LED_ON.

## Ghi chú

Mở hai terminal: chạy subscriber trước rồi gửi lệnh bằng tài khoản operator. Bản demo cũng ghi lệnh vào logs/commands.log. Chưa có thiết bị chấp hành thật để bật/tắt LED; bài này kiểm tra nhận và in lệnh.

Cài môi trường dùng chung: `scripts/setup.ps1`. Hướng dẫn tổng thể: [README gốc](../../README.md). Báo cáo: [Bao_cao_Lab_5.docx](../../Bao_cao/Bao_cao_Lab_5.docx).

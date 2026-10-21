# Bài 1 về nhà: Gateway tổng hợp dữ liệu cảm biến

Subscribe sensor/+/data, gom bản tin của nhiều node và publish một báo cáo JSON mỗi 10 giây.

## Tệp của bài

- `aggregator.py`
- `sensor_simulator.py`
- `chay.ps1`
- `sensor_node1.ps1`
- `sensor_node2.ps1`

## Cách chạy

Các lệnh dưới đây chạy từ thư mục gốc `C:\IOT\lab5`. Có thể chạy file PowerShell bằng đường dẫn tuyệt đối từ thư mục khác.

```powershell
powershell -ExecutionPolicy Bypass -File Ve_nha\Bai_1\chay.ps1

powershell -ExecutionPolicy Bypass -File Ve_nha\Bai_1\sensor_node1.ps1

powershell -ExecutionPolicy Bypass -File Ve_nha\Bai_1\sensor_node2.ps1

.\.venv\Scripts\python.exe scripts\mqtt_cli.py sub -t gateway/aggregated_report -v
```

## Kết quả cần quan sát

Báo cáo có window_start, timestamp, node_count, message_count và nodes; mỗi node giữ JSON hợp lệ mới nhất trong cửa sổ 10 giây.

## Ghi chú

Mỗi lệnh chạy trong terminal riêng, dùng broker bảo mật. Hệ thống demo đã chạy aggregator và hai sensor. Dữ liệu sensor được mô phỏng, có simulated=true. JSON lỗi bị bỏ qua; bộ đệm được bảo vệ bằng khóa luồng. Cửa sổ không có dữ liệu gửi node_count=0; publish lỗi sẽ khôi phục bộ đệm.

Cài môi trường dùng chung: `scripts/setup.ps1`. Hướng dẫn tổng thể: [README gốc](../../README.md). Báo cáo: [Bao_cao_Lab_5.docx](../../Bao_cao/Bao_cao_Lab_5.docx).

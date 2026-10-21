"""Organize exercise sources and entry points without breaking existing commands."""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXERCISES = [
    {
        "folder": "Tren_lop/Bai_1", "title": "Bài 1: Cài đặt và cấu hình Mosquitto Local Broker",
        "objective": "Cài đặt broker MQTT cục bộ trên gateway và cấu hình địa chỉ lắng nghe.",
        "files": ["mosquitto.conf", "chay.ps1"],
        "commands": ["powershell -ExecutionPolicy Bypass -File scripts\\stop.ps1",
                     "powershell -ExecutionPolicy Bypass -File Tren_lop\\Bai_1\\chay.ps1"],
        "expected": "Broker mở cổng 1883 trên 127.0.0.1; sẵn sàng nhận kết nối MQTT trên máy này.",
        "notes": "Chế độ anonymous chỉ dùng cho bài 1–2 trên loopback. Dừng hệ thống demo trước khi mở broker này để tránh trùng cổng. Kết thúc bằng Ctrl+C, rồi chạy scripts/start.ps1 để trở lại bản bảo mật. Trên Linux, dùng sudo apt install mosquitto mosquitto-clients và sudo systemctl status mosquitto.",
        "test_prefixes": ["Bai 1-2:"],
    },
    {
        "folder": "Tren_lop/Bai_2", "title": "Bài 2: Kiểm tra MQTT Client bằng dòng lệnh",
        "objective": "Dùng mosquitto_sub và mosquitto_pub để kiểm tra truyền nhận bản tin tại gateway/test.",
        "files": ["nhan.ps1", "gui.ps1"],
        "commands": ["powershell -ExecutionPolicy Bypass -File Tren_lop\\Bai_2\\nhan.ps1",
                     "powershell -ExecutionPolicy Bypass -File Tren_lop\\Bai_2\\gui.ps1"],
        "expected": "Terminal subscriber hiển thị gateway/test Hello Local MQTT.",
        "notes": "Chạy broker anonymous của bài 1 trước. Mở hai terminal, chạy nhan.ps1 trước rồi gui.ps1. Kết thúc subscriber bằng Ctrl+C. Nếu dùng broker bảo mật đang chạy, xem lệnh scripts/mqtt_cli.py trong README gốc.",
        "test_prefixes": ["Bai 2:"],
    },
    {
        "folder": "Tren_lop/Bai_3", "title": "Bài 3: Cài Paho-MQTT và kiểm tra kết nối Python",
        "objective": "Tạo môi trường ảo Python, cài Paho-MQTT và xác minh callback kết nối broker thành công.",
        "files": ["check_connection.py", "chay.ps1"],
        "commands": ["powershell -ExecutionPolicy Bypass -File scripts\\start.ps1",
                     "powershell -ExecutionPolicy Bypass -File Tren_lop\\Bai_3\\chay.ps1"],
        "expected": "CONNECTED 127.0.0.1:1883 và Ket noi MQTT thanh cong.",
        "notes": "Chỉ chạy start.ps1 nếu hệ thống chưa chạy. Paho dùng CallbackAPIVersion.VERSION2; Session ở gateway/common.py chờ CONNACK trước khi xác nhận thành công. Truyền --anonymous khi thử broker bài 1. Cài thư viện: .venv/Scripts/python.exe -m pip install -r requirements.txt.",
        "test_prefixes": ["Bai 3:"],
    },
    {
        "folder": "Tren_lop/Bai_4", "title": "Bài 4: Publish thông số CPU và RAM mỗi 5 giây",
        "objective": "Đọc CPU/RAM thật bằng psutil, đóng gói JSON và gửi gateway/system/metrics định kỳ.",
        "files": ["metrics_publisher.py", "chay.ps1"],
        "commands": ["powershell -ExecutionPolicy Bypass -File Tren_lop\\Bai_4\\chay.ps1",
                     ".\\.venv\\Scripts\\python.exe scripts\\mqtt_cli.py sub -t gateway/system/metrics -v"],
        "expected": "Một bản tin JSON mỗi 5 giây gồm cpu_percent, ram_percent, ram_used_bytes, ram_total_bytes, gateway_id và timestamp.",
        "notes": "Cần broker bảo mật đang chạy. Hệ thống demo đã có một publisher; chỉ chạy thêm nếu muốn thử riêng. Chạy hữu hạn: python -m Tren_lop.Bai_4.metrics_publisher --count 3. Timestamp dùng UTC; đây là số đo thật của máy Windows, không phải số liệu cảm biến mô phỏng.",
        "test_prefixes": ["Bai 4:"],
    },
    {
        "folder": "Tren_lop/Bai_5", "title": "Bài 5: Subscribe lắng nghe lệnh điều khiển",
        "objective": "Đăng ký wildcard gateway/command/# và in các lệnh nhận được trong callback on_message.",
        "files": ["command_subscriber.py", "chay.ps1", "gui_lenh.ps1"],
        "commands": ["powershell -ExecutionPolicy Bypass -File Tren_lop\\Bai_5\\chay.ps1",
                     "powershell -ExecutionPolicy Bypass -File Tren_lop\\Bai_5\\gui_lenh.ps1"],
        "expected": "Subscriber in COMMAND, thời gian, topic gateway/command/led và nội dung LED_ON.",
        "notes": "Mở hai terminal: chạy subscriber trước rồi gửi lệnh bằng tài khoản operator. Bản demo cũng ghi lệnh vào logs/commands.log. Chưa có thiết bị chấp hành thật để bật/tắt LED; bài này kiểm tra nhận và in lệnh.",
        "test_prefixes": ["Bai 5:"],
    },
    {
        "folder": "Ve_nha/Bai_1", "title": "Bài 1 về nhà: Gateway tổng hợp dữ liệu cảm biến",
        "objective": "Subscribe sensor/+/data, gom bản tin của nhiều node và publish một báo cáo JSON mỗi 10 giây.",
        "files": ["aggregator.py", "sensor_simulator.py", "chay.ps1", "sensor_node1.ps1", "sensor_node2.ps1"],
        "commands": ["powershell -ExecutionPolicy Bypass -File Ve_nha\\Bai_1\\chay.ps1",
                     "powershell -ExecutionPolicy Bypass -File Ve_nha\\Bai_1\\sensor_node1.ps1",
                     "powershell -ExecutionPolicy Bypass -File Ve_nha\\Bai_1\\sensor_node2.ps1",
                     ".\\.venv\\Scripts\\python.exe scripts\\mqtt_cli.py sub -t gateway/aggregated_report -v"],
        "expected": "Báo cáo có window_start, timestamp, node_count, message_count và nodes; mỗi node giữ JSON hợp lệ mới nhất trong cửa sổ 10 giây.",
        "notes": "Mỗi lệnh chạy trong terminal riêng, dùng broker bảo mật. Hệ thống demo đã chạy aggregator và hai sensor. Dữ liệu sensor được mô phỏng, có simulated=true. JSON lỗi bị bỏ qua; bộ đệm được bảo vệ bằng khóa luồng. Cửa sổ không có dữ liệu gửi node_count=0; publish lỗi sẽ khôi phục bộ đệm.",
        "test_prefixes": ["Ve nha 1:"],
    },
    {
        "folder": "Ve_nha/Bai_2", "title": "Bài 2 về nhà: Bảo mật xác thực và phân quyền broker",
        "objective": "Tắt truy cập anonymous, tạo tài khoản bằng mosquitto_passwd và kiểm chứng từ chối đăng nhập hoặc thao tác không hợp lệ.",
        "files": ["cau_hinh_bao_mat.py", "acl", "mosquitto-secure.conf.example", "kiem_tra.ps1"],
        "commands": ["powershell -ExecutionPolicy Bypass -File Ve_nha\\Bai_2\\kiem_tra.ps1"],
        "expected": "Anonymous và mật khẩu sai bị từ chối; node1 không gửi được lệnh; dashboard chỉ đọc dữ liệu.",
        "notes": "Tài khoản thực nằm ở config/credentials.json, mật khẩu băm ở config/passwords; không sao chép bí mật vào thư mục bài nộp. File .example dùng đường dẫn tương đối từ thư mục gốc lab. Muốn tạo lại cấu hình: dừng demo, chạy python -m Ve_nha.Bai_2.cau_hinh_bao_mat rồi khởi động lại. Giữ nguyên mật khẩu nếu tài khoản đã có. mosquitto_passwd -U chuyển tệp tạm chứa mật khẩu sang hash có salt.",
        "test_prefixes": ["Ve nha 2:"],
    },
    {
        "folder": "Ve_nha/Bai_3", "title": "Bài 3 về nhà: Node-RED Dashboard cục bộ",
        "objective": "Nhận dữ liệu MQTT bằng Node-RED và hiển thị CPU/RAM bằng Gauge, Chart cùng bảng dữ liệu sensor.",
        "files": ["flows.json", "settings.js", "chay.ps1"],
        "commands": ["powershell -ExecutionPolicy Bypass -File Ve_nha\\Bai_3\\chay.ps1"],
        "expected": "Dashboard tại http://127.0.0.1:1880/dashboard/gateway có hai Gauge CPU/RAM, biểu đồ lịch sử và bảng hai cảm biến mô phỏng.",
        "notes": "chay.ps1 khởi động cả hệ thống nếu chưa chạy, sau đó in địa chỉ dashboard. Flow trong thư mục này là bản để xem/import; flow chạy thực nằm ở node-red/flows.json và được sinh đồng thời bởi scripts/build_flow.py. Node-RED dùng tài khoản dashboard, chỉ có quyền đọc metrics/report. Khi import sang máy khác cần nhập tài khoản broker rồi Deploy. Môi trường chạy nằm chung ở node-red/ để tránh cài lặp thư viện.",
        "test_prefixes": [],
    },
]


def write_ps1(path, commands):
    header = "$ErrorActionPreference = 'Stop'\nSet-Location (Split-Path (Split-Path $PSScriptRoot -Parent) -Parent)\n"
    path.write_text(header + "\n".join(commands) + "\n", encoding="utf-8-sig")


def main():
    for group in ("Tren_lop", "Ve_nha"):
        (ROOT / group).mkdir(exist_ok=True)
        (ROOT / group / "__init__.py").touch()
    moves = {
        "gateway/check_connection.py": "Tren_lop/Bai_3/check_connection.py",
        "gateway/metrics_publisher.py": "Tren_lop/Bai_4/metrics_publisher.py",
        "gateway/command_subscriber.py": "Tren_lop/Bai_5/command_subscriber.py",
        "gateway/aggregator.py": "Ve_nha/Bai_1/aggregator.py",
        "gateway/sensor_simulator.py": "Ve_nha/Bai_1/sensor_simulator.py",
        "scripts/prepare.py": "Ve_nha/Bai_2/cau_hinh_bao_mat.py",
    }
    for source, destination in moves.items():
        old, new = ROOT / source, ROOT / destination
        new.parent.mkdir(parents=True, exist_ok=True)
        module = destination.removesuffix(".py").replace("/", ".")
        if not new.exists():
            content = old.read_text(encoding="utf-8").replace("from .common import", "from gateway.common import")
            if source == "scripts/prepare.py":
                content = content.replace(".parents[1]", ".parents[2]")
                content = content.replace('config = ROOT / "config"',
                                          'config = ROOT / "config"\n    shutil.copyfile(ROOT / "Ve_nha/Bai_2/acl", config / "acl")')
            new.write_text(content, encoding="utf-8")
        exports = "Aggregator, main" if source == "gateway/aggregator.py" else "main"
        prelude = '"""Compatibility entry point; exercise source: ' + destination + '."""\n'
        if source == "scripts/prepare.py":
            prelude += "import sys\nfrom pathlib import Path\nsys.path.insert(0, str(Path(__file__).resolve().parents[1]))\n"
        old.write_text(prelude + f"from {module} import {exports}\n\nif __name__ == '__main__':\n    main()\n", encoding="utf-8")
    for item in EXERCISES:
        folder = ROOT / item["folder"]
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "__init__.py").touch()
        files = "\n".join(f"- `{name}`" for name in item["files"])
        commands = "\n\n".join(item["commands"])
        (folder / "README.md").write_text(
            f"# {item['title']}\n\n{item['objective']}\n\n## Tệp của bài\n\n{files}\n\n"
            f"## Cách chạy\n\nCác lệnh dưới đây chạy từ thư mục gốc `C:\\IOT\\lab5`. "
            "Có thể chạy file PowerShell bằng đường dẫn tuyệt đối từ thư mục khác.\n\n"
            f"```powershell\n{commands}\n```\n\n## Kết quả cần quan sát\n\n{item['expected']}\n\n"
            f"## Ghi chú\n\n{item['notes']}\n\n"
            "Cài môi trường dùng chung: `scripts/setup.ps1`. Hướng dẫn tổng thể: [README gốc](../../README.md). "
            "Báo cáo: [Bao_cao_Lab_5.docx](../../Bao_cao/Bao_cao_Lab_5.docx).\n", encoding="utf-8")
    if not (ROOT / "Tren_lop/Bai_1/mosquitto.conf").exists():
        shutil.copyfile(ROOT / "config/mosquitto-local.conf", ROOT / "Tren_lop/Bai_1/mosquitto.conf")
    if not (ROOT / "Ve_nha/Bai_2/acl").exists():
        shutil.copyfile(ROOT / "config/acl", ROOT / "Ve_nha/Bai_2/acl")
    (ROOT / "Ve_nha/Bai_2/mosquitto-secure.conf.example").write_text(
        "# Run mosquitto with working directory set to the lab root.\n"
        "listener 1883 127.0.0.1\nallow_anonymous false\npassword_file config/passwords\n"
        "acl_file config/acl\npersistence false\nlog_dest stdout\nlog_type all\n", encoding="utf-8")
    shutil.copyfile(ROOT / "node-red/flows.json", ROOT / "Ve_nha/Bai_3/flows.json")
    shutil.copyfile(ROOT / "node-red/settings.js", ROOT / "Ve_nha/Bai_3/settings.js")
    write_ps1(ROOT / "Tren_lop/Bai_1/chay.ps1", [
        "& .\\tools\\mosquitto\\mosquitto.exe -c Tren_lop\\Bai_1\\mosquitto.conf -v",
        "if ($LASTEXITCODE -ne 0) { throw 'Broker failed. Stop the demo first if port 1883 is occupied.' }"])
    write_ps1(ROOT / "Tren_lop/Bai_2/nhan.ps1", ["& .\\tools\\mosquitto\\mosquitto_sub.exe -h 127.0.0.1 -t gateway/test -v"])
    write_ps1(ROOT / "Tren_lop/Bai_2/gui.ps1", ["& .\\tools\\mosquitto\\mosquitto_pub.exe -h 127.0.0.1 -t gateway/test -m 'Hello Local MQTT'"])
    for folder, module in (("Tren_lop/Bai_3", "check_connection"), ("Tren_lop/Bai_4", "metrics_publisher"),
                           ("Tren_lop/Bai_5", "command_subscriber"), ("Ve_nha/Bai_1", "aggregator")):
        write_ps1(ROOT / folder / "chay.ps1", [
            f"& .\\.venv\\Scripts\\python.exe -m {folder.replace('/', '.')}.{module} @args",
            "if ($LASTEXITCODE -ne 0) { throw 'Exercise failed; check broker connection and arguments.' }"])
    write_ps1(ROOT / "Tren_lop/Bai_5/gui_lenh.ps1", [
        "& .\\.venv\\Scripts\\python.exe scripts\\mqtt_cli.py pub -t gateway/command/led -m LED_ON"])
    for node in ("node1", "node2"):
        write_ps1(ROOT / f"Ve_nha/Bai_1/sensor_{node}.ps1", [
            f"& .\\.venv\\Scripts\\python.exe -m Ve_nha.Bai_1.sensor_simulator --node {node} @args"])
    write_ps1(ROOT / "Ve_nha/Bai_2/kiem_tra.ps1", [
        "# Includes authentication and ACL checks on isolated test brokers.",
        "& .\\.venv\\Scripts\\python.exe tests\\integration.py",
        "if ($LASTEXITCODE -ne 0) { throw 'MQTT verification failed; see reports/test-results.json' }"])
    write_ps1(ROOT / "Ve_nha/Bai_3/chay.ps1", [
        "$listening = Get-NetTCPConnection -State Listen -LocalPort 1880 -ErrorAction SilentlyContinue",
        "if (-not $listening) {",
        "    & .\\.venv\\Scripts\\python.exe scripts\\manage.py start",
        "    if ($LASTEXITCODE -ne 0) { throw 'Dashboard startup failed; see logs/' }",
        "}",
        "Write-Host 'Dashboard: http://127.0.0.1:1880/dashboard/gateway'",
        "Write-Host 'Node-RED editor: http://127.0.0.1:1880/'"])
    (ROOT / "scripts/exercises.json").write_text(json.dumps(EXERCISES, indent=2, ensure_ascii=False), encoding="utf-8")
    (ROOT / "Bao_cao").mkdir(exist_ok=True)
    print("Organized 5 classroom exercises and 3 homework exercises.")


if __name__ == "__main__":
    main()

"""Build the importable Node-RED flow without embedding any password."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
nodes = []


def add(id, type, **options):
    node = {"id": id, "type": type, **options}
    nodes.append(node)
    return node


add("lab5", "tab", label="Lab 5 - Local MQTT Gateway", disabled=False, info="CPU/RAM: 5s; sensor aggregation: 10s")
add("mqtt-local", "mqtt-broker", name="Mosquitto authenticated local", broker="127.0.0.1", port="1883",
    clientid="lab5-dashboard", autoConnect=True, usetls=False, protocolVersion="4", keepalive="30",
    cleansession=True, autoUnsubscribe=True)
add("base", "ui-base", name="Lab 5 Gateway", path="/dashboard", appIcon="mdi-router-wireless",
    includeClientData=True, acceptClientConfig=[], showPathInSidebar=False,
    headerContent="page", navigationStyle="default", titleBarStyle="default", showReconnectNotification=True)
add("theme", "ui-theme", name="Gateway",
    colors={"surface": "#ffffff", "primary": "#087f8c", "bgPage": "#f1f5f9", "groupBg": "#ffffff", "groupOutline": "#dbe4ed"},
    sizes={"density": "default", "pagePadding": "20px", "groupGap": "16px", "groupBorderRadius": "8px", "widgetGap": "12px"})
add("page", "ui-page", name="Gateway Monitor", ui="base", path="/gateway", icon="router-wireless",
    layout="grid", theme="theme", order=1, visible=True, disabled=False,
    breakpoints=[{"name": "Default", "px": 0, "cols": 3}, {"name": "Tablet", "px": 576, "cols": 6},
                 {"name": "Desktop", "px": 1024, "cols": 12}])
add("system", "ui-group", name="CPU / RAM thuc te - cap nhat moi 5 giay", page="page", width=12,
    height=1, order=1, showTitle=True, visible=True, disabled=False, groupType="default")
add("sensors", "ui-group", name="Sensor mo phong - tong hop moi 10 giay", page="page", width=12,
    height=1, order=2, showTitle=True, visible=True, disabled=False, groupType="default")
add("mqtt-metrics", "mqtt in", z="lab5", name="System metrics", topic="gateway/system/metrics", qos="1",
    datatype="json", broker="mqtt-local", nl=False, rap=True, rh=0, inputs=0, x=140, y=100, wires=[["split-metrics"]])
add("split-metrics", "function", z="lab5", name="CPU / RAM", outputs=2, x=370, y=100,
    func="const p = msg.payload;\nif (!p || !Number.isFinite(p.cpu_percent) || !Number.isFinite(p.ram_percent)) return null;\nreturn [{payload:p.cpu_percent,topic:'CPU'}, {payload:p.ram_percent,topic:'RAM'}];",
    wires=[["cpu", "chart"], ["ram", "chart"]])
for index, metric in enumerate(("CPU", "RAM")):
    add(metric.lower(), "ui-gauge", z="lab5", name=metric, group="system", order=index + 1,
        width=6, height=3, gtype="gauge-half", gstyle="needle", title=f"{metric} usage", units="%",
        value="payload", valueType="msg", min=0, max=100,
        segments=[{"color": "#16a34a", "from": 0}, {"color": "#f59e0b", "from": 70}, {"color": "#dc2626", "from": 90}],
        sizeThickness=16, sizeGap=4, sizeKeyThickness=8, styleRounded=True, styleGlow=False,
        x=620, y=80 + index * 70, wires=[[]])
add("chart", "ui-chart", z="lab5", name="CPU and RAM history", group="system", label="CPU / RAM history (%)",
    order=3, width=12, height=5, chartType="line", category="topic", categoryType="msg",
    xAxisProperty="", xAxisPropertyType="timestamp", xAxisType="time", xAxisFormat="{HH}:{mm}:{ss}",
    xAxisFormatType="custom", yAxisProperty="payload", yAxisPropertyType="msg", ymin="0", ymax="100",
    action="append", showLegend=True, pointRadius=2, pointShape="circle", interpolation="linear",
    removeOlder=10, removeOlderUnit="60", removeOlderPoints="120", colors=["#087f8c", "#e38627"],
    textColorDefault=True, gridColorDefault=True, x=630, y=220, wires=[[]])
add("mqtt-report", "mqtt in", z="lab5", name="Aggregated report", topic="gateway/aggregated_report", qos="1",
    datatype="json", broker="mqtt-local", nl=False, rap=True, rh=0, inputs=0, x=150, y=320, wires=[["report-summary"]])
add("report-summary", "function", z="lab5", name="Report summary", outputs=2, x=390, y=320,
    func="const p=msg.payload; if (!p || !p.nodes) return null;\nreturn [{payload:`${p.node_count} nodes | ${p.message_count} messages | ${p.timestamp}`}, {payload:Object.entries(p.nodes).map(([node,v])=>({node,...v.data,received_at:v.received_at}))}];",
    wires=[["report-text"], ["sensor-table"]])
add("report-text", "ui-text", z="lab5", group="sensors", order=1, width=12, height=1,
    name="Window summary", label="Latest report", value="payload", valueType="msg", format="{{msg.payload}}",
    layout="row-spread", wrapText=True, x=650, y=300, wires=[])
add("sensor-table", "ui-table", z="lab5", group="sensors", order=2, width=12, height=3,
    name="Latest sensor values", label="Simulated sensor data", maxrows=0, autocols=True, showSearch=False,
    selectionType="none", columns=[], x=660, y=370, wires=[[]])
# Unique IDs prevent Node-RED treating literal values such as headerContent='page'
# as a reference to a config node with the same ID.
ids = {node["id"]: "lab5-" + node["id"] for node in nodes}
for node in nodes:
    node["id"] = ids[node["id"]]
    for key in ("z", "ui", "theme", "page", "group", "broker"):
        if node.get(key) in ids:
            node[key] = ids[node[key]]
    if "wires" in node:
        node["wires"] = [[ids[target] for target in output] for output in node["wires"]]
(ROOT / "node-red" / "flows.json").write_text(json.dumps(nodes, indent=2), encoding="utf-8")
exercise_flow = ROOT / "Ve_nha/Bai_3/flows.json"
if exercise_flow.parent.exists():
    exercise_flow.write_text(json.dumps(nodes, indent=2), encoding="utf-8")
print(f"Built Node-RED flow: {len(nodes)} nodes")

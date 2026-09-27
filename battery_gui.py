import sys
import wmi
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox

print("程序正在启动...")

def get_battery_health():
    try:
        c = wmi.WMI(namespace="root\\wmi")
        design = c.BatteryStaticData()[0].DesignedCapacity
        full = c.BatteryFullChargedCapacity()[0].FullChargedCapacity
        cycle = c.BatteryCycleCount()[0].CycleCount
        health = (full / design) * 100
        return health, design, full, cycle
    except Exception as e:
        return None, None, None, str(e)

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("电池健康检测工具")
window.resize(350, 250)

layout = QVBoxLayout()

label = QLabel("点击下方按钮，检测电池健康状况")
label.setStyleSheet("font-size: 14px; color: #333; margin-bottom: 15px;")

result_label = QLabel("健康度: --%")
result_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #2b7a2b;")

info_label = QLabel("设计容量: --\n满充容量: --\n循环次数: --")

def on_click():
    health, design, full, cycle = get_battery_health()
    if health is not None:
        result_label.setText(f"健康度: {health:.2f}%")
        info_label.setText(f"设计容量: {design} mWh\n满充容量: {full} mWh\n循环次数: {cycle}")
    else:
        QMessageBox.critical(window, "错误", f"读取失败！\n原因: {design}")
        result_label.setText("读取失败")
        info_label.setText("请以管理员身份运行")

btn = QPushButton("开始检测")
btn.setStyleSheet("font-size: 16px; padding: 10px; background-color: #0078d4; color: white; border-radius: 5px;")
btn.clicked.connect(on_click)

layout.addWidget(label)
layout.addWidget(result_label)
layout.addWidget(info_label)
layout.addWidget(btn)

window.setLayout(layout)
window.show()
sys.exit(app.exec())
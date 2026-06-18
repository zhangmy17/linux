import time
import wmi

# ANSI颜色定义
BLUE = "\033[34m"
YELLOW = "\033[33m"
ORANGE = "\033[38;5;208m"
RED = "\033[31m"
WHITE = "\033[0m"

# WMI读取主板温控温度（系统自带，无需额外软件）
def get_cpu_temperature():
    try:
        c = wmi.WMI(namespace="root\\wmi")
        temp_data = c.MSAcpi_ThermalZoneTemperature()[0]
        temp_c = int(temp_data.CurrentTemperature / 10 - 273.15)
        return temp_c
    except Exception as e:
        print(f"读取硬件失败，使用模拟温度，错误：{e}")
        return 40

def draw_dinosaur(temp):
    print("\n" * 70)
    if temp < 45:
        f_color, flame, tip = BLUE, "≋ ≋ ≋ ≋ ≋ ≋ ≋ ≋ ≋ ≋", "💧 凉爽待机，CPU低负载"
    elif 45 <= temp <= 65:
        f_color, flame, tip = YELLOW, "≋ ≋ ≋ ≋ ≋ ≋ ≋ ≋ ≋ ≋", "☀️ 负载正常，运行平稳"
    elif 66 <= temp <= 80:
        f_color, flame, tip = ORANGE, "≋ ≋ ≋ ≋ ≋ ≋ ≋ ≋ ≋ ≋", "🔥 负载偏高，建议减负"
    else:
        f_color, flame, tip = RED, "≋ ≋ ≋ ≋ ≋ ≋ ≋ ≋ ≋ ≋", "⚠️ 高温警告！立刻降负载！"

    print("┌─────────────────────────────────────────────────────┐")
    print(f"│                                                     │")
    print(f"│        /\\_/\\                                        │")
    print(f"│       |  • _\\                                       │")
    print(f"│       |  _\\{f_color}{flame}{WHITE}                      │")
    print(f"│       |  |                                          │")
    print(f"│                                                     │")
    print(f"│  CPU实时温度：{temp}℃  | 状态：{tip}    │")
    print("└─────────────────────────────────────────────────────┘")
    print("按 Ctrl + C 退出监控程序")

if __name__ == "__main__":
    try:
        while True:
            t = get_cpu_temperature()
            draw_dinosaur(t)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n监控程序已安全关闭")
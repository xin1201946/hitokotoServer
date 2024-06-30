import platform
import psutil
import os
from datetime import timedelta
import socket
import ctypes


def get_system_info():
    boot_time_timestamp = psutil.boot_time()
    uptime_seconds = int(psutil.time.time() - boot_time_timestamp)
    uptime_string = str(timedelta(seconds=uptime_seconds)).split('.')[0]
    processor_name=platform.processor().split(',')[0]
    user32 = ctypes.windll.user32
    gdi32 = ctypes.windll.gdi32
    dc = user32.GetDC(None)
    width = gdi32.GetDeviceCaps(dc, 118)  # 原始分辨率的宽度
    height = gdi32.GetDeviceCaps(dc, 117)  # 原始分辨率的高度

    info = {
        "User": f"{os.getlogin()}@{platform.node()}",
        "OS": f"{platform.system()} {platform.release()} ({platform.version()}) {platform.machine()}",
        "Host": f"{platform.node()}",
        "Kernel": platform.version(),
        "Uptime": uptime_string,
        "Shell": os.environ.get("SHELL", "Unknown"),
        "Display": f"{width}*{height}",
        "DE": "Fluent",
        "WM": "Desktop Window Manager",
        "WM Theme": "Custom - Blue (System: Light, Apps: Light)",
        "Icons": "CanFeng Design",
        "Font": "Microsoft YaHei UI (12pt)",
        "Terminal": "WEB Terminal By Canf",
        "Terminal Font": "CaskaydiaMono Nerd Font (12pt)",
        "CPU": f"{processor_name} @ {psutil.cpu_freq().max} MHz",
        "Memory": f"{round(psutil.virtual_memory().used / (1024 ** 3), 2)} GiB / {round(psutil.virtual_memory().total / (1024 ** 3), 2)} GiB ({psutil.virtual_memory().percent}%)",
        "Swap": f"{round(psutil.swap_memory().used / (1024 ** 3), 2)} GiB / {round(psutil.swap_memory().total / (1024 ** 3), 2)} GiB ({psutil.swap_memory().percent}%)",
        "Local IP": f"{socket.gethostbyname(socket.gethostname())}",
        "Battery": get_battery_status(),
        "Locale": "zh-CN"
    }
    return info


def get_battery_status():
    battery = psutil.sensors_battery()
    if battery:
        return f"{battery.percent}% [{'AC Connected' if battery.power_plugged else 'Discharging'}]"
    else:
        return "No Battery"


def print_system_info(info, shellname=''):
    global logo_lines
    if shellname != '':
        info['Shell'] = shellname
    logo_lines = [
        "%%%%%%%%%%%@%%%%%%%%%%%%%%%%%%%%%%%",
        "%%%%%%%%%@%#%@%%%%%%%%@@@%%%%%%%%%%",
        "%%%%%%%%%@*+*%@%%%%%@@%#%@%%%%%%%%%",
        "%%%%%%%%@#+=-+#@@%%@%*+=%@%%%%%%%%%",
        "%%%%%%%@%++:.-++****++-+@%%%%%%%%%%",
        "**%%%%@@++=:.:*++*++*+:*@%%%%%%%%%%",
        "**%%%%%*=+=  .*#*###**-+%%%@@@@**@%",
        "#%@%%%*+*+*--=++**#**##+#@%%%%#*#%%",
        "*#%%%%*+=++****#######*+#@%###*%%%%",
        "%%#*%%#++=++=+*+-=+#*=-+%%%%%%#%%%%",
        "%@%##++=+++**+*==*#%#+*#%%#%%%%%%%%",
        "@%#+=+++++*++=+***++***##%##**%%%@%",
        "*+=====+-:*++**#%#*+#%%+#%+:--+%%%%",
        "===-::::..-=+***#*#%%%+==++---=#%#%",
        "-..::::::::::=+=-=*#%%*=+***===+#%%",
        "==:-===-..::.:-=-=**###****++**#%%%",
        "=--++++=-:-: ::++ =*+**+=+####%%%%%",
    ]

    info_lines = [
        f"{'User:'.ljust(20)}{info['User']}",
        f"{'OS:'.ljust(20)}{info['OS']}",
        f"{'Host:'.ljust(20)}{info['Host']}",
        f"{'Kernel:'.ljust(20)}{info['Kernel']}",
        f"{'Uptime:'.ljust(20)}{info['Uptime']}",
        f"{'Shell:'.ljust(20)}{info['Shell']}",
        f"{'Display:'.ljust(20)}{info['Display']}",
        f"{'DE:'.ljust(20)}{info['DE']}",
        f"{'WM:'.ljust(20)}{info['WM']}",
        f"{'WM Theme:'.ljust(20)}{info['WM Theme']}",
        f"{'Icons:'.ljust(20)}{info['Icons']}",
        f"{'Font:'.ljust(20)}{info['Font']}",
        f"{'Terminal:'.ljust(20)}{info['Terminal']}",
        f"{'Terminal Font:'.ljust(20)}{info['Terminal Font']}",
        f"{'CPU:'.ljust(20)}{info['CPU']}",
        f"{'Memory:'.ljust(20)}{info['Memory']}",
        f"{'Swap:'.ljust(20)}{info['Swap']}",
        f"{'Local IP:'.ljust(20)}{info['Local IP']}",
        f"{'Battery:'.ljust(20)}{info['Battery']}",
        f"{'Locale:'.ljust(20)}{info['Locale']}",
    ]

    # Combine logo and info side by side
    combined_lines = []
    max_lines = max(len(logo_lines), len(info_lines))
    for i in range(max_lines):
        logo_part = logo_lines[i] if i < len(logo_lines) else " " * len(logo_lines[0])
        info_part = info_lines[i] if i < len(info_lines) else ""
        combined_lines.append(f"{logo_part}  {info_part}")

    result = []
    for line in combined_lines:
        result.append(line)
    return result


if __name__ == "__main__":
    system_info = get_system_info()
    print(print_system_info(system_info))

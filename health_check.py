import os
import psutil
import subprocess
from datetime import datetime
from notifypy import Notify

os.environ["DISPLAY"] = ":0"
os.environ["DBUS_SESSION_BUS_ADDRESS"] = f"unix:path=/run/user/{os.getuid()}/bus"

notification = Notify()

def send_desktop_alert(title, message):
    """Triggers a native Ubuntu desktop notification."""
    notification.application_name = "Server Health Monitor"
    notification.title = title
    notification.message = message
    notification.send()

def run_health_check():
    print("==========================================")
    print(" LINUX SERVER HEALTH REPORT & MONITOR")
    print(f" Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("==========================================")

    # 1. CPU & RAM Threshold Check (Lowered to > 1.0% so you can see the alert popup right away!)
    cpu_usage = psutil.cpu_percent(interval=1)
    print(f"[CPU] Usage: {cpu_usage}%")
    if cpu_usage > 1.0:
        send_desktop_alert("⚠️ High CPU Warning", f"Usage is at {cpu_usage}%")

    mem = psutil.virtual_memory()
    print(f"[RAM] Usage: {mem.percent}%")
    if mem.percent > 1.0:
        send_desktop_alert("⚠️ High RAM Warning", f"Usage is at {mem.percent}%")

    # 2. Disk Space Check
    print("\n[DISK PARTITIONS]")
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            print(f"  - {partition.mountpoint}: {usage.percent}% Used")
        except PermissionError:
            continue

    # 3. Security Log Check
    print("\n[SECURITY]")
    try:
        cmd = "grep -i 'failed' /var/log/auth.log | wc -l"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        failed_attempts = int(result.stdout.strip())
        print(f"  - Failed Login Attempts in auth.log: {failed_attempts}")
    except Exception:
        print("  - Could not fetch login logs.")
    
    print("==========================================")
    print(" Health check completed successfully.")

if __name__ == "__main__":
    run_health_check()

import psutil
import platform
import csv
import os
import logging
import time
from datetime import datetime

from config import (
    CPU_THRESHOLD,
    MEMORY_THRESHOLD,
    DISK_THRESHOLD,
    MONITOR_INTERVAL,
    CSV_FILE,
    LOG_FILE
)


def create_directories():
    os.makedirs("data", exist_ok=True)
    os.makedirs("logs", exist_ok=True)


def setup_logging():
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def get_system_info():
    print("\n==============================================")
    print("           SYSTEM INFORMATION")
    print("==============================================")
    print(f"Operating System : {platform.system()}")
    print(f"OS Version       : {platform.release()}")
    print(f"Machine          : {platform.machine()}")
    print(f"Processor        : {platform.processor()}")
    print(f"Computer Name    : {platform.node()}")
    print("==============================================")


def get_cpu_usage():
    return psutil.cpu_percent(interval=1)


def get_memory_usage():
    memory = psutil.virtual_memory()
    return {
        "percent": memory.percent,
        "total": round(memory.total / (1024 ** 3), 2),
        "available": round(memory.available / (1024 ** 3), 2)
    }


def get_disk_usage():
    disk_path = os.path.abspath(os.sep)
    disk = psutil.disk_usage(disk_path)
    return {
        "percent": disk.percent,
        "total": round(disk.total / (1024 ** 3), 2),
        "free": round(disk.free / (1024 ** 3), 2)
    }


def get_network_usage():
    network = psutil.net_io_counters()
    return {
        "sent_mb": round(network.bytes_sent / (1024 ** 2), 2),
        "received_mb": round(network.bytes_recv / (1024 ** 2), 2)
    }


def get_process_count():
    return len(psutil.pids())


def get_system_uptime():
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.now() - boot_time
    return str(uptime).split(".")[0]


def get_status(value, threshold):
    return "WARNING" if value >= threshold else "NORMAL"


def check_alerts(cpu, memory, disk):
    alerts = []
    if cpu >= CPU_THRESHOLD:
        alerts.append(f"High CPU usage detected: {cpu}%")
    if memory >= MEMORY_THRESHOLD:
        alerts.append(f"High memory usage detected: {memory}%")
    if disk >= DISK_THRESHOLD:
        alerts.append(f"High disk usage detected: {disk}%")
    return alerts


def display_alerts(alerts):
    if alerts:
        print("\nALERTS:")
        for alert in alerts:
            print(f"  [WARNING] {alert}")
            logging.warning(alert)
    else:
        print("\nSystem Status : HEALTHY")


def initialize_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                "Timestamp", "CPU Usage (%)", "Memory Usage (%)",
                "Disk Usage (%)", "Network Sent (MB)",
                "Network Received (MB)", "Running Processes"
            ])


def save_to_csv(timestamp, cpu, memory, disk, network, process_count):
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            timestamp, cpu, memory, disk,
            network["sent_mb"], network["received_mb"], process_count
        ])


def display_metrics(timestamp, cpu, memory, disk, network, process_count, uptime):
    print("\n==============================================")
    print("              SYSTEM MONITOR")
    print("==============================================")
    print(f"Time              : {timestamp}")
    print("----------------------------------------------")
    print(f"CPU Usage         : {cpu}% [{get_status(cpu, CPU_THRESHOLD)}]")
    print(f"Memory Usage      : {memory['percent']}% [{get_status(memory['percent'], MEMORY_THRESHOLD)}]")
    print(f"Memory Total      : {memory['total']} GB")
    print(f"Memory Available  : {memory['available']} GB")
    print("----------------------------------------------")
    print(f"Disk Usage        : {disk['percent']}% [{get_status(disk['percent'], DISK_THRESHOLD)}]")
    print(f"Disk Total        : {disk['total']} GB")
    print(f"Disk Free         : {disk['free']} GB")
    print("----------------------------------------------")
    print(f"Network Sent      : {network['sent_mb']} MB")
    print(f"Network Received  : {network['received_mb']} MB")
    print(f"Running Processes : {process_count}")
    print(f"System Uptime     : {uptime}")
    print("==============================================")


def monitor_system():
    print("\nSystem monitoring started.")
    print(f"Monitoring interval: {MONITOR_INTERVAL} seconds")
    print("Press Ctrl+C to stop monitoring.\n")
    logging.info("System monitoring started.")

    try:
        while True:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cpu = get_cpu_usage()
            memory = get_memory_usage()
            disk = get_disk_usage()
            network = get_network_usage()
            process_count = get_process_count()
            uptime = get_system_uptime()

            display_metrics(timestamp, cpu, memory, disk, network, process_count, uptime)

            alerts = check_alerts(cpu, memory["percent"], disk["percent"])
            display_alerts(alerts)

            save_to_csv(
                timestamp, cpu, memory["percent"], disk["percent"],
                network, process_count
            )

            logging.info(
                f"CPU={cpu}% | Memory={memory['percent']}% | Disk={disk['percent']}%"
            )
            time.sleep(MONITOR_INTERVAL)

    except KeyboardInterrupt:
        print("\n\nMonitoring stopped by user.")
        logging.info("System monitoring stopped by user.")
    except Exception as error:
        print(f"\nUnexpected error: {error}")
        logging.exception("Unexpected monitoring error.")


def main():
    create_directories()
    setup_logging()
    initialize_csv()
    get_system_info()
    monitor_system()


if __name__ == "__main__":
    main()

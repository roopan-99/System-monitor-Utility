# System Monitoring Utility

A Python-based cross-platform system monitoring utility for monitoring system
resource utilization and identifying potential performance issues.

## Features

- Real-time CPU utilization monitoring
- Memory usage monitoring
- Disk utilization monitoring
- Network sent and received statistics
- Running process count
- System uptime tracking
- Configurable CPU, memory, and disk thresholds
- Automatic warning generation
- CSV-based monitoring history
- Application logging
- Continuous monitoring
- Windows and Linux support
- Modular and reusable Python functions

## Technologies Used

- Python
- psutil
- CSV
- Python Logging
- OS / Platform / Datetime

## Installation

Install the required dependency:

```bash
pip install -r requirements.txt
```

## Run

```bash
python system_monitor.py
```

Press `Ctrl + C` to safely stop monitoring.

## Default Thresholds

| Resource | Warning Threshold |
|---|---:|
| CPU | 80% |
| Memory | 80% |
| Disk | 85% |

The thresholds and monitoring interval can be changed in `config.py`.

## Output

Monitoring history is saved to:

`data/system_metrics.csv`

Application logs and warning messages are saved to:

`logs/system_monitor.log`

## Use Case

This project demonstrates basic concepts used in system monitoring, IT support,
and production support environments. It helps identify high resource utilization
and provides initial information for troubleshooting system performance issues.

## Future Enhancements

- Process-level CPU and memory monitoring
- Email alerts
- Monitoring dashboard
- Historical trend visualization
- Database integration
- Remote server monitoring

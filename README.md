# embedded-toolkit

[![CI](https://github.com/Qandel-Embedded/embedded-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/Qandel-Embedded/embedded-toolkit/actions)
[![PyPI](https://img.shields.io/badge/pypi-embedded--toolkit-blue)](https://pypi.org/project/embedded-toolkit)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A plug-and-play Python toolkit for embedded systems engineers.  
Works on Raspberry Pi, desktop, and any Python 3.9+ environment.

## Install

```bash
pip install embedded-toolkit
```

## What's Inside

| Module | What it does |
|--------|-------------|
| `KalmanFilter` | 1-D Kalman filter — sensor noise reduction |
| `MovingAverage` | Ring-buffer moving average |
| `PIDController` | Anti-windup PID with output clamping |
| `crc8 / crc16_modbus / crc32` | CRC checksums for serial protocols |
| `FrameEncoder / FrameDecoder` | HDLC-style byte framing for UART |

## Quick Examples

```python
from embedded_toolkit import KalmanFilter, PIDController, crc16_modbus

# Denoise a temperature sensor
kf = KalmanFilter(process_noise=0.01, measurement_noise=0.5)
clean = kf.update(noisy_reading)

# PID heater control
pid = PIDController(kp=1.2, ki=0.4, kd=0.05, output_limits=(0, 100))
pwm = pid(setpoint=75.0, measured=current_temp)

# Validate a Modbus frame
frame = bytes([0x01, 0x03, 0x00, 0x00, 0x00, 0x02])
crc   = crc16_modbus(frame)
```

## Run Tests

```bash
git clone https://github.com/Qandel-Embedded/embedded-toolkit
cd embedded-toolkit
pip install -e . pytest pyserial
pytest tests/ -v
```

---
Made by **[Ahmed Qandel](https://ahmedqandel.com)** — Embedded Systems & IoT Engineer  
Available for freelance contracts via Upwork.

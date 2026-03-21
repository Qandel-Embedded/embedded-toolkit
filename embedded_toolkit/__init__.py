"""embedded-toolkit — Utilities for embedded systems development."""
from .filters   import KalmanFilter, MovingAverage
from .pid       import PIDController
from .crc       import crc8, crc16_modbus, crc32
from .framing   import FrameEncoder, FrameDecoder

__version__ = "1.0.0"
__all__ = [
    "KalmanFilter", "MovingAverage",
    "PIDController",
    "crc8", "crc16_modbus", "crc32",
    "FrameEncoder", "FrameDecoder",
]

"""Digital filters for sensor data processing."""
import numpy as np
from collections import deque


class KalmanFilter:
    """Lightweight 1-D Kalman filter suitable for MCU/Pi deployments.

    Args:
        process_noise (float): Q — model uncertainty (lower = trust model more).
        measurement_noise (float): R — sensor uncertainty (lower = trust sensor more).

    Example::

        kf = KalmanFilter(process_noise=0.01, measurement_noise=0.5)
        for raw in sensor_readings:
            filtered = kf.update(raw)
    """

    def __init__(self, process_noise: float = 0.1, measurement_noise: float = 1.0,
                 initial_state: float = 0.0):
        self._q  = process_noise
        self._r  = measurement_noise
        self._x  = initial_state   # state estimate
        self._p  = 1.0             # error covariance

    def update(self, measurement: float) -> float:
        """Feed one measurement, return filtered estimate."""
        # Predict
        p_pred = self._p + self._q
        # Update
        k      = p_pred / (p_pred + self._r)
        self._x = self._x + k * (measurement - self._x)
        self._p = (1 - k) * p_pred
        return self._x

    @property
    def state(self) -> float:
        return self._x


class MovingAverage:
    """Efficient ring-buffer moving average filter.

    Example::

        mav = MovingAverage(window=8)
        smoothed = mav.update(raw_adc_value)
    """

    def __init__(self, window: int = 8):
        self._buf = deque(maxlen=window)

    def update(self, value: float) -> float:
        self._buf.append(value)
        return sum(self._buf) / len(self._buf)

    def reset(self):
        self._buf.clear()

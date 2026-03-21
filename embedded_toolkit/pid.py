"""PID controller with anti-windup and output clamping."""
import time


class PIDController:
    """Discrete PID controller with integral anti-windup.

    Args:
        kp, ki, kd: PID gains
        output_limits: (min, max) tuple for output clamping
        sample_time: None = auto (uses real elapsed time)

    Example::

        pid = PIDController(kp=1.2, ki=0.5, kd=0.1, output_limits=(0, 100))
        while True:
            output = pid(setpoint=75.0, measured=read_temperature())
            set_heater_pwm(output)
            time.sleep(0.1)
    """

    def __init__(self, kp: float, ki: float, kd: float,
                 output_limits: tuple = (-100.0, 100.0),
                 sample_time: float = None):
        self.kp, self.ki, self.kd = kp, ki, kd
        self._lo, self._hi = output_limits
        self._sample_time  = sample_time
        self._integral     = 0.0
        self._prev_error   = 0.0
        self._prev_time    = time.monotonic()

    def __call__(self, setpoint: float, measured: float) -> float:
        return self.compute(setpoint, measured)

    def compute(self, setpoint: float, measured: float) -> float:
        now = time.monotonic()
        dt  = self._sample_time or max(now - self._prev_time, 1e-6)
        err = setpoint - measured

        # Integral with anti-windup clamping
        self._integral += self.ki * err * dt
        self._integral  = max(self._lo, min(self._hi, self._integral))

        derivative = self.kd * (err - self._prev_error) / dt
        output     = self.kp * err + self._integral + derivative
        output     = max(self._lo, min(self._hi, output))

        self._prev_error = err
        self._prev_time  = now
        return output

    def reset(self):
        """Reset integral and derivative history."""
        self._integral   = 0.0
        self._prev_error = 0.0
        self._prev_time  = time.monotonic()

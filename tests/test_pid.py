from embedded_toolkit import PIDController
import time


def test_pid_reduces_error():
    pid = PIDController(kp=1.0, ki=0.0, kd=0.0, output_limits=(-200, 200))
    out = pid.compute(setpoint=100.0, measured=0.0)
    assert out > 0


def test_pid_output_clamped():
    pid = PIDController(kp=999.0, ki=0.0, kd=0.0, output_limits=(-100, 100))
    out = pid.compute(100.0, 0.0)
    assert out == 100.0


def test_pid_reset_clears_integral():
    pid = PIDController(kp=0.0, ki=10.0, kd=0.0, output_limits=(-1000, 1000))
    for _ in range(5): pid.compute(10.0, 0.0)
    pid.reset()
    out = pid.compute(0.0, 0.0)
    assert abs(out) < 0.1

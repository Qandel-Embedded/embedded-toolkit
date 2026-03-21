from embedded_toolkit import KalmanFilter, MovingAverage


def test_kalman_steady_state():
    kf = KalmanFilter(process_noise=0.01, measurement_noise=0.1)
    for _ in range(50):
        out = kf.update(10.0)
    assert abs(out - 10.0) < 0.01


def test_kalman_tracks_step():
    kf = KalmanFilter()
    for _ in range(20): kf.update(0.0)
    for _ in range(20): out = kf.update(5.0)
    assert out > 4.0


def test_moving_average_window():
    ma = MovingAverage(window=4)
    for v in [0, 0, 0, 4]:
        out = ma.update(v)
    assert out == 1.0


def test_moving_average_reset():
    ma = MovingAverage(4)
    for v in [10, 10, 10, 10]: ma.update(v)
    ma.reset()
    assert ma.update(0) == 0.0

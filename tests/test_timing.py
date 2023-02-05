import time
from datetime import timedelta

import pytest

from ancv.timing import Stopwatch


def test_stopwatch_disallows_same_segments() -> None:
    stopwatch = Stopwatch()
    with pytest.raises(ValueError):
        stopwatch("segment1")
        stopwatch("segment1")


def sleep(seconds: float) -> None:
    """Sleep for the given number of seconds.

    This is a replacement for the built-in `time.sleep()` function which will send
    control back to the OS, introducing an uncertainty depending on the OS.
    To keep our tests fast, we want to sleep for brief periods, but that will yield a
    large relative error from the approx. constant OS thread sleep uncertainties.
    """
    now = time.time()
    while time.time() <= (now + seconds):
        time.sleep(0.001)


@pytest.mark.flaky(reruns=3)
def test_stopwatch_basics() -> None:
    stopwatch = Stopwatch()
    stopwatch("segment1")
    sleep(0.1)
    stopwatch("segment2")
    sleep(0.1)
    stopwatch("segment3")
    sleep(0.2)
    stopwatch.stop()
    sleep(0.1)
    stopwatch("segment4")
    sleep(0.5)
    stopwatch.stop()

    expected_timings = {
        "segment1": timedelta(seconds=0.1),
        "segment2": timedelta(seconds=0.1),
        "segment3": timedelta(seconds=0.2),
        "segment4": timedelta(seconds=0.5),
    }
    for real, expected in zip(stopwatch.timings.values(), expected_timings.values()):
        # https://stackoverflow.com/a/1133888/11477374 :
        os_thread_sleep_uncertainty_microseconds = 25_000
        assert (
            pytest.approx(
                real.microseconds, abs=os_thread_sleep_uncertainty_microseconds
            )
            == expected.microseconds
        )

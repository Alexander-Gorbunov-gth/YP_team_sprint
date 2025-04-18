import time
import functools


def bench_timer(func):

    @functools.wraps(func)
    def wrapper(instance, *args, **kwargs):
        start_time = time.time()
        func(instance, *args, **kwargs)
        end_time = time.time()
        return end_time-start_time

    return wrapper


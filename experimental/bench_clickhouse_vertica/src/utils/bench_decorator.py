import time
import functools

import vertica_python

from src.core.config import settings


def bench_clickhouse(func):

    @functools.wraps(func)
    def wrapper(instance, *args, **kwargs):
        total_time = 0
        for id in range(settings.col_requests):
            start_time = time.time()
            func(instance, id, *args, **kwargs)
            end_time = time.time()
            total_time += end_time-start_time

        return total_time

    return wrapper


def bench_vertica(func):

    @functools.wraps(func)
    def wrapper(instance, *args, **kwargs):
        with vertica_python.connect(**settings.vertica_dict) as conn:
            cur = conn.cursor()
            total_time = 0
            for id in range(settings.col_requests):
                start_time = time.time()
                func(instance, id, cur, *args, **kwargs)
                end_time = time.time()
                total_time += end_time-start_time
            conn.commit()
            cur.close()

        return total_time

    return wrapper

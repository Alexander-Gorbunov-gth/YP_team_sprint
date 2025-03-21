import time

from backoff import expo, on_exception
from redis import Redis
from redis.exceptions import ConnectionError

from tests.functional.settings import test_settings


@on_exception(expo, ConnectionError, max_tries=15, max_time=150)
def main():
    redis_client = Redis(
        host=test_settings.redis_host, port=test_settings.redis_port
    )
    redis_client.ping()


if __name__ == "__main__":
    main()

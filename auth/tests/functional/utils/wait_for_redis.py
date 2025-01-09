from backoff import on_exception, expo
from redis import Redis
from redis.exceptions import ConnectionError

from tests.functional.settings import test_settings


@on_exception(expo, ConnectionError, max_tries=15, max_time=150)
def main():
    # time.sleep(10000)
    redis_client = Redis(
        host=test_settings.redis.redis_host, port=test_settings.redis.redis_port
    )
    redis_client.ping()


if __name__ == "__main__":
    main()

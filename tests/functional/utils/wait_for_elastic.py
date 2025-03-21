from backoff import expo, on_exception
from elasticsearch import Elasticsearch, exceptions

from tests.functional.settings import test_settings


@on_exception(
    expo,
    (exceptions.ApiError, exceptions.TransportError),
    max_tries=15,
    max_time=150,
)
def main():
    es_client = Elasticsearch(
        hosts=test_settings.es_url_to_connect,
        verify_certs=False,
        ssl_show_warn=False,
    )
    es_client.ping()


if __name__ == "__main__":
    main()

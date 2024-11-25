import time

from elasticsearch import Elasticsearch

from tests.functional.settings import test_settings

if __name__ == '__main__':
    es_client = Elasticsearch(hosts=test_settings.get_elastic_url(), verify_certs=False, ssl_show_warn=False)
    while True:
        if es_client.ping():
            break
        time.sleep(1)
import clickhouse_connect
from kafka import KafkaConsumer

import json
from logger import logger

from settings import settings
from src.queries import queries
from src.schemas.base_user_event import BaseUserEvent
from src.helpers.backoff_func_wrapper import backoff


class ClickHouse:
    def __init__(self):
        self.client = clickhouse_connect.get_client(
            **settings.clickhouse_settings.get_init_conf()
        )

    def create_tables(self):
        self.client.command(queries.get("create_user_events_table"))

    def _get_table_columns(self, table: str) -> dict:
        result = self.client.query(
            f"SELECT name, type FROM system.columns WHERE table = '{table}'"+
            f"AND database = '{settings.clickhouse_settings.database}' ORDER BY position"
        )
        return {row[0]: row[1] for row in result.result_rows}

    @backoff(0.1, 2, 10, logger)
    def load_data(self, table: str, data: list[BaseUserEvent]):
        columns = self._get_table_columns(table)
        normal_data = []

        for event in data:
            event_dict = event.model_dump()
            payload = event_dict.pop("payload")
            merged_data = {**event_dict, **payload}

            row = []
            for key, value in columns.items():
                if merged_data.get(key):
                    res = merged_data.get(key)
                else:
                    if value == "Array(Nullable(String))":
                        res = []
                    else:
                        res = None
                row.append(res)
            normal_data.append(row)

        self.client.insert(table, normal_data, columns)


class Kafka:
    def __init__(self):
        self.consumer = KafkaConsumer(
            **settings.kafka_settings.get_init_conf()
        )
        self.consumer.subscribe([settings.kafka_settings.topic_name])


if __name__ == "__main__":
    ch = ClickHouse()
    ch.create_tables()
    kafka = Kafka()
    batch = []

    try:
        for msg in kafka.consumer:
            data = json.loads(json.loads(msg.value))
            data = BaseUserEvent(**data)

            batch.append(data)

            if len(batch) >= settings.batch_size:
                ch.load_data("user_events", batch)
                batch = []

    finally:
        ch.load_data("user_events", batch)

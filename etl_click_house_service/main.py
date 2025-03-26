import clickhouse_connect
from typing import Any, Generator, List, Tuple
from pydantic import BaseModel

from src.queries import queries
from src.schemas.base_user_event import BaseUserEvent, ClickPayload, VideoProgressPayload
from logging import Logger


class ClickHouse:
    def __init__(self):
        self.client = clickhouse_connect.get_client(
            host='ofsok90ydh.germanywestcentral.azure.clickhouse.cloud',
            user='default',
            password='cjh72mrPIGd.f',
            secure=True
        )

    def create_tables(self):
        self.client.command(queries.get("create_user_events_table"))

    def _get_table_columns(self, table: str) -> dict:
        result = self.client.query(
            f"SELECT name, type FROM system.columns WHERE table = '{table}' AND database = 'default' ORDER BY position"
        )
        return {row[0]: row[1] for row in result.result_rows}

    def load_data(self, table: str, data: List[BaseUserEvent]):
        columns = self._get_table_columns(table)
        print(columns)
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

        print(normal_data)
        self.client.insert(table, normal_data, columns)


class Kafka:
    def __init__(self):
        ...

    def extract_data(self):
        ...


if __name__ == '__main__':
    import faker
    fake = faker.Faker()
    ch = ClickHouse()
    ch.create_tables()

    event = BaseUserEvent(
        user_id=fake.uuid4(),
        ip_address=fake.ipv4(),
        user_agent="asdasd/web",
        event_type="click",
        timestamp=fake.date_time(),
        # payload=ClickPayload(
        #     item_id="item_123",
        #     item_type="button"
        # )
        payload=VideoProgressPayload(
            video_id="item_123",
            watched_seconds=123
        )
    )
    ch.load_data(
        "user_events",
        [event]
    )

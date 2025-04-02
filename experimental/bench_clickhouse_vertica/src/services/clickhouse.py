import clickhouse_connect

from src.core.config import settings
from src.services import BaseService
from src.utils.bench_decorator import bench_clickhouse
from src.utils.sql_tools import (
    DatabaseType, SQLRequests,
    SQLTools
)


class ClickHouse(BaseService):
    def __init__(self):
        self.sql_tools = SQLTools(DatabaseType.CLICKHOUSE)
        self.client = clickhouse_connect.get_client(
            **settings.clickhouse_dict
        )
        self._create_test_table()

    def _create_test_table(self) -> None:
        self.client.query(
            self.sql_tools.get_sql_request(SQLRequests.CREATE_TABLE)
        )

    @bench_clickhouse
    def _bench_insert(self, id: int) -> int:
        self.client.command(
            self.sql_tools.get_sql_request(SQLRequests.INSERT)
            .format(id=id, name=f"name_{id}")
        )

    @bench_clickhouse
    def _bench_select(self, id: int) -> int:
        self.client.query(
            self.sql_tools.get_sql_request(SQLRequests.SELECT)
            .format(id=id)
        )

    @bench_clickhouse
    def _bench_update(self, id: int) -> int:
        self.client.command(
            self.sql_tools.get_sql_request(SQLRequests.UPDATE)
            .format(name=f"updated_name_{id}", id=id)
        )

    @bench_clickhouse
    def _bench_delete(self, id: int) -> int:
        self.client.command(
            self.sql_tools.get_sql_request(SQLRequests.DELETE)
            .format(id=id)
        )

import vertica_python
import vertica_python.vertica
import vertica_python.vertica.cursor

from src.core.config import settings
from src.services import BaseService
from src.utils.bench_decorator import bench_vertica
from src.utils.sql_tools import (
    DatabaseType, SQLRequests,
    SQLTools
)


class Vertica(BaseService):
    def __init__(self):
        self.sql_tools = SQLTools(DatabaseType.VERTICA)
        self._create_test_table()

    def _create_test_table(self) -> None:
        with vertica_python.connect(**settings.vertica_dict) as conn:
            cur = conn.cursor()
            cur.execute(
                self.sql_tools.get_sql_request(SQLRequests.CREATE_TABLE)
            )
            cur.close()

    @bench_vertica
    def _bench_insert(
        self,
        id: int,
        cur: vertica_python.vertica.cursor.Cursor
    ) -> int:
        cur.execute(
            self.sql_tools.get_sql_request(SQLRequests.INSERT),
            (id, f"name_{id}")
        )

    @bench_vertica
    def _bench_select(
        self,
        id: int,
        cur: vertica_python.vertica.cursor.Cursor
    ) -> int:
        cur.execute(
            self.sql_tools.get_sql_request(SQLRequests.SELECT),
            (id,)
        )
        cur.fetchall()

    @bench_vertica
    def _bench_update(
        self,
        id: int,
        cur: vertica_python.vertica.cursor.Cursor
    ) -> int:
        cur.execute(
            self.sql_tools.get_sql_request(SQLRequests.UPDATE),
            (f"updated_name_{id}", id)
        )

    @bench_vertica
    def _bench_delete(
        self,
        id: int,
        cur: vertica_python.vertica.cursor.Cursor
    ) -> int:
        cur.execute(
            self.sql_tools.get_sql_request(SQLRequests.DELETE),
            (id,)
        )

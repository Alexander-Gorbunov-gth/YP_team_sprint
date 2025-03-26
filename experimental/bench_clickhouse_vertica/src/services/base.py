from abc import abstractmethod

from src.core.config import settings
from src.utils.sql_tools import SQLRequests


class BaseService:
    def __init__(self):
        self._create_test_table()

    @abstractmethod
    def _create_test_table(self) -> None:
        pass

    @abstractmethod
    def _bench_insert(self) -> int:
        pass

    @abstractmethod
    def _bench_select(self) -> int:
        pass

    @abstractmethod
    def _bench_update(self) -> int:
        pass

    @abstractmethod
    def _bench_delete(self) -> int:
        pass

    def bench(self) -> dict:
        return {
            SQLRequests.INSERT: self._bench_insert()/settings.col_requests,
            SQLRequests.SELECT: self._bench_select()/settings.col_requests,
            SQLRequests.UPDATE: self._bench_update()/settings.col_requests,
            SQLRequests.DELETE: self._bench_delete()/settings.col_requests
        }

from abc import abstractmethod

from src.utils.enums import RequestType


class BaseService:
    def __init__(self):
        pass

    @abstractmethod
    def _bench_insert_one(self) -> int:
        pass

    @abstractmethod
    def _bench_insert_many(self) -> int:
        pass

    @abstractmethod
    def _bench_select_one(self) -> int:
        pass

    @abstractmethod
    def _bench_select_many(self) -> int:
        pass

    @abstractmethod
    def _bench_update_one(self) -> int:
        pass

    @abstractmethod
    def _bench_update_many(self) -> int:
        pass

    @abstractmethod
    def _bench_delete_one(self) -> int:
        pass

    @abstractmethod
    def _bench_delete_many(self) -> int:
        pass

    def bench(self) -> dict:
        return {
            RequestType.INSERT_ONE: self._bench_insert_one(),
            RequestType.INSERT_MANY: self._bench_insert_many(),
            RequestType.SELECT_ONE: self._bench_select_one(),
            RequestType.SELECT_MANY: self._bench_select_many(),
            RequestType.UPDATE_ONE: self._bench_update_one(),
            RequestType.UPDATE_MANY: self._bench_update_many(),
            RequestType.DELETE_ONE: self._bench_delete_one(),
            RequestType.DELETE_MANY: self._bench_delete_many()
        }

import pymongo

from src.services import BaseService
from src.core.config import settings
from src.utils.bench_decorator import bench_timer


class MongoDB(BaseService):
    def __init__(self):
        self.client = pymongo.MongoClient(
            host=settings.mongodb_host,
            port=settings.mongodb_port
        )
        self.db = self.client[settings.mongodb_db]
        self.table = self.db["test"]
        super().__init__()

    @bench_timer
    def _bench_insert_one(self) -> int:
        print("MongoDB insert_one")
        for row in range(settings.col_requests):
            self.table.insert_one({
                "row": row,
                "test_type": "insert_one"
            })

    @bench_timer
    def _bench_insert_many(self) -> int:
        print("MongoDB insert_many")
        data = [{
            "row": row,
            "test_type": "insert_many"
        } for row in range(settings.col_requests)]
        self.table.insert_many(data)

    @bench_timer
    def _bench_select_one(self) -> int:
        print("MongoDB select_one")
        for row in range(settings.col_requests):
            self.table.find_one({
                "row": row,
                "test_type": "insert_one"
            })

    @bench_timer
    def _bench_select_many(self) -> int:
        print("MongoDB select_many")
        list(self.table.find({
            "test_type": "insert_many"
        }))

    @bench_timer
    def _bench_update_one(self) -> int:
        print("MongoDB update_one")
        for row in range(settings.col_requests):
            self.table.update_one(
                {"row": row, "test_type": "insert_one"},
                {"$set": {"test_type": "update_one"}}
            )

    @bench_timer
    def _bench_update_many(self) -> int:
        print("MongoDB update_many")
        self.table.update_many(
            {"test_type": "insert_many"},
            {"$set": {"test_type": "update_many"}}
        )

    @bench_timer
    def _bench_delete_one(self) -> int:
        print("MongoDB delete_one")
        for row in range(settings.col_requests):
            self.table.delete_one({
                "row": row,
                "test_type": "update_one"
            })

    @bench_timer
    def _bench_delete_many(self) -> int:
        print("MongoDB delete_many")
        self.table.delete_many({
            "test_type": "update_many"
        })

import psycopg2
from psycopg2.extras import execute_batch

from src.services import BaseService
from src.core.config import settings
from src.utils.bench_decorator import bench_timer


class Postgres(BaseService):
    def __init__(self):
        self.conn = psycopg2.connect(
            host=settings.postgres_host,
            port=settings.postgres_port,
            dbname=settings.postgres_db,
            user=settings.postgres_username,
            password=settings.postgres_password
        )
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS test (
                id SERIAL PRIMARY KEY,
                row INTEGER,
                test_type VARCHAR
            )
        """)
        super().__init__()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    @bench_timer
    def _bench_insert_one(self) -> int:
        print("Postgres insert_one")
        for row in range(settings.col_requests):
            self.cursor.execute(
                "INSERT INTO test (row, test_type) VALUES (%s, %s)",
                (row, "insert_one")
            )

    @bench_timer
    def _bench_insert_many(self) -> int:
        print("Postgres insert_many")
        data = [(row, "insert_many") for row in range(settings.col_requests)]
        execute_batch(
            self.cursor,
            "INSERT INTO test (row, test_type) VALUES (%s, %s)",
            data,
            page_size=500
        )

    @bench_timer
    def _bench_select_one(self) -> int:
        print("Postgres select_one")
        for row in range(settings.col_requests):
            self.cursor.execute(
                "SELECT * FROM test WHERE row = %s AND test_type = %s LIMIT 1",
                (row, "insert_one")
            )
            self.cursor.fetchone()

    @bench_timer
    def _bench_select_many(self) -> int:
        print("Postgres select_many")
        self.cursor.execute(
            "SELECT * FROM test WHERE test_type = %s",
            ("insert_many",)
        )
        self.cursor.fetchall()

    @bench_timer
    def _bench_update_one(self) -> int:
        print("Postgres update_one")
        for row in range(settings.col_requests):
            self.cursor.execute(
                "UPDATE test SET test_type = %s WHERE row = %s AND test_type = %s",
                ("update_one", row, "insert_one")
            )

    @bench_timer
    def _bench_update_many(self) -> int:
        print("Postgres update_many")
        self.cursor.execute(
            "UPDATE test SET test_type = %s WHERE test_type = %s",
            ("update_many", "insert_many")
        )

    @bench_timer
    def _bench_delete_one(self) -> int:
        print("Postgres delete_one")
        for row in range(settings.col_requests):
            self.cursor.execute(
                "DELETE FROM test WHERE row = %s AND test_type = %s",
                (row, "update_one")
            )

    @bench_timer
    def _bench_delete_many(self) -> int:
        print("Postgres delete_many")
        self.cursor.execute(
            "DELETE FROM test WHERE test_type = %s",
            ("update_many",)
        )

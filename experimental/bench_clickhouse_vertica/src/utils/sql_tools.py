import enum


class DatabaseType(enum.Enum):
    CLICKHOUSE = "clickhouse"
    VERTICA = "vertica"


class SQLRequests(enum.Enum):
    CREATE_TABLE = "create_table"
    INSERT = "insert"
    SELECT = "select"
    UPDATE = "update"
    DELETE = "delete"


class SQLTools:
    def __init__(self, database_type: DatabaseType):
        self.database_type = database_type

    def get_sql_request(self, file_name: SQLRequests) -> str:
        with open(
            f"./src/sql/{self.database_type.value}/{file_name.value}.sql", "r"
        ) as sql_request:
            return sql_request.read()

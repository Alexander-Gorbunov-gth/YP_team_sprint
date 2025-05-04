import enum


class DatabaseType(enum.Enum):
    POSTGRES = "postgres"
    MONGODB = "mongodb"


class RequestType(enum.Enum):
    INSERT_ONE = "insert_one"
    INSERT_MANY = "insert_many"
    SELECT_ONE = "select_one"
    SELECT_MANY = "select_many"
    UPDATE_ONE = "update_one"
    UPDATE_MANY = "update_many"
    DELETE_ONE = "delete_one"
    DELETE_MANY = "delete_many"

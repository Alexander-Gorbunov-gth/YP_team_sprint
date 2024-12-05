from sqlmodel import SQLModel, create_engine

from src.core.config import settings
from src.models.users import *
from src.models.permissions import *
from src.models.sessions import *

sync_engine = create_engine(
    "postgresql://postgres:password@auth_postgres:5432/auth",
    echo=True
)


def develop_db_worker():
    SQLModel.metadata.drop_all(sync_engine)
    SQLModel.metadata.create_all(sync_engine)

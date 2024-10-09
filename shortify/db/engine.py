from sqlalchemy import Engine
from sqlmodel import SQLModel
from sqlmodel import create_engine as _create_sqlalchemy_engine


def create_engine(conn_str: str, *args, **kwargs) -> Engine:
    engine = _create_sqlalchemy_engine(conn_str, *args, **kwargs)
    SQLModel.metadata.create_all(engine)
    return engine

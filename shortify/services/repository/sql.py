import typing

from sqlalchemy import Engine
from sqlmodel import select, Session

from . import abc
from shortify.db import models


class GenericRepository(abc.GenericRepository[abc.TSQLModel]):
    def __init__(self, engine: Engine, model_type: typing.Type[abc.TSQLModel]):
        self._engine = engine
        self._model_type = model_type

    def get_all(self, session: Session) -> typing.Sequence[abc.TSQLModel]:
        stmt = select(self._model_type)
        return session.exec(stmt).all()

    def get_by_field(
        self,
        session: Session,
        key: str,
        value: typing.Any,
        # eager_load: typing.Optional[typing.Sequence[str]] = None
    ) -> typing.Optional[abc.TSQLModel]:
        stmt = select(self._model_type).where(getattr(self._model_type, key) == value)

        # if eager_load:
        # stmt = stmt.options(selectinload(*eager_load)) # type: ignore

        return session.exec(stmt).first()

    def create(self, session: Session, model: abc.TSQLModel) -> abc.TSQLModel:
        session.add(model)
        session.commit()
        session.refresh(model)
        return model


class SQLUserRepository(abc.UserRepository, GenericRepository[models.User]):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, models.User)


class SQLShortlinkRepository(GenericRepository[models.Shortlink]):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, models.Shortlink)


class SQLAuthTokenRepository(GenericRepository[models.AuthToken]):
    def __init__(self, engine: Engine) -> None:
        super().__init__(engine, models.AuthToken)

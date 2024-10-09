from abc import (
    ABC,
    abstractmethod,
)
import typing

from sqlmodel import SQLModel, Session

from shortify.db import models


TSQLModel = typing.TypeVar("TSQLModel", bound=SQLModel)


class GenericRepository(ABC, typing.Generic[TSQLModel]):
    @abstractmethod
    def get_all(self, session: Session) -> typing.Sequence[TSQLModel]: ...

    @abstractmethod
    def get_by_field(
        self,
        session: Session,
        key: str,
        value: typing.Any,
        eager_load: typing.Optional[typing.Sequence[str]] = None,
    ) -> typing.Optional[TSQLModel]: ...

    @abstractmethod
    def create(self, session: Session, model: TSQLModel) -> TSQLModel: ...


class UserRepository(GenericRepository[models.User]): ...


class ShortlinkRepository(GenericRepository[models.Shortlink]): ...


class AuthTokenRepository(GenericRepository[models.AuthToken]): ...

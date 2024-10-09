from abc import (
    ABC,
    abstractmethod,
)
import typing

from shortify.db import models
from .schemas import (
    ShortlinkCreateInput,
    AuthTokenCreateInput,
    UserResponse,
)


class UserService(ABC):
    @abstractmethod
    def create(self) -> models.User: ...


class ShortlinkService(ABC):
    @abstractmethod
    def get_all(self) -> typing.Sequence[models.Shortlink]: ...

    @abstractmethod
    def create(self, auth_token: str, input: ShortlinkCreateInput) -> UserResponse: ...

    @abstractmethod
    def get_by_name(self, name: str) -> typing.Optional[models.Shortlink]: ...


class AuthTokenService(ABC):
    @abstractmethod
    def create(self, input: AuthTokenCreateInput) -> models.AuthToken: ...

    @abstractmethod
    def get_user_by_token(self, auth_token: str) -> typing.Optional[models.User]: ...

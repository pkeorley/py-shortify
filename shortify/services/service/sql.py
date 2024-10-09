from contextlib import contextmanager
import typing

from sqlalchemy import Engine
from sqlmodel import Session

from shortify import crypto
from . import (
    abc,
    schemas,
)
from shortify.db import models
from shortify.services.repository import abc as _abc_repo
from shortify.services.service import abc as _abc_service


@contextmanager
def create_session(engine: Engine):
    session = Session(engine, expire_on_commit=False)
    try:
        yield session
    finally:
        session.close()


class SQLUserService(abc.UserService):
    def __init__(
        self,
        engine: Engine,
        user_repository: _abc_repo.UserRepository,
        auth_token_service: _abc_service.AuthTokenService,
    ):
        self._engine = engine
        self._user_repository = user_repository
        self._auth_token_service = auth_token_service

    def create(self) -> schemas.UserResponse:
        with create_session(self._engine) as session:
            user = self._user_repository.create(session, model=models.User())

            input = schemas.AuthTokenCreateInput(user=user.id)
            auth_token = self._auth_token_service.create(input=input)

            user = self._user_repository.get_by_field(
                session, key="id", value=auth_token.user_id
            )
            assert user is not None

            return schemas.UserResponse(id=user.id, auth_token=input.token)


class SQLShortlinkService(abc.ShortlinkService):
    def __init__(
        self,
        engine: Engine,
        shortlink_repository: _abc_repo.ShortlinkRepository,
        user_repository: _abc_repo.UserRepository,
        auth_token_service: abc.AuthTokenService,
    ):
        self._engine = engine
        self._shortlink_repository = shortlink_repository
        self._user_repository = user_repository
        self._auth_token_service = auth_token_service

    def get_all(self) -> typing.Sequence[models.Shortlink]:
        with create_session(self._engine) as session:
            return self._shortlink_repository.get_all(session)

    def get_by_name(self, name: str) -> typing.Optional[models.Shortlink]:
        with create_session(self._engine) as session:
            return self._shortlink_repository.get_by_field(
                session=session, key="name", value=name
            )

    def create(
        self, auth_token: str, input: schemas.ShortlinkCreateInput
    ) -> schemas.Response:
        user_model = self._auth_token_service.get_user_by_token(auth_token)

        with create_session(self._engine) as session:
            if user_model is None:
                raise PermissionError("Invalid auth token")

            shortlink_model = self._shortlink_repository.create(
                session,
                model=models.Shortlink(
                    name=input.name,
                    url=input.url,
                    user_id=user_model.id,
                ),
            )
            return schemas.Response(
                id=shortlink_model.id,
            )


class SQLAuthTokenService(abc.AuthTokenService):
    def __init__(
        self,
        engine: Engine,
        auth_token_repository: _abc_repo.AuthTokenRepository,
        user_repository: _abc_repo.UserRepository,
    ) -> None:
        self._engine = engine
        self._auth_token_repository = auth_token_repository
        self._user_repository = user_repository

    def create(self, input: abc.AuthTokenCreateInput) -> models.AuthToken:
        with create_session(self._engine) as session:
            return self._auth_token_repository.create(
                session,
                model=models.AuthToken(
                    token=crypto.sha256(input.token),
                    user_id=input.user,
                ),
            )

    def get_user_by_token(self, auth_token: str) -> typing.Optional[models.User]:
        with create_session(self._engine) as session:
            auth_token_model = self._auth_token_repository.get_by_field(
                session, key="token", value=crypto.sha256(auth_token)
            )

            if auth_token_model:
                return self._user_repository.get_by_field(
                    session, key="id", value=auth_token_model.user_id
                )

            return None

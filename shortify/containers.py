from dependency_injector import containers, providers

from shortify.services.repository import sql as _sql_repos
from shortify.services.service import sql as _sql_services

from .db.engine import create_engine


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "shortify.endpoints.v1.users",
            "shortify.endpoints.v1.shortlinks",
            "shortify.endpoints.v1.shorten",
        ]
    )

    config = providers.Configuration()

    engine = providers.Callable(
        create_engine,
        conn_str=config.db.conn_str,
        echo=True,
    )

    user_repository = providers.Singleton(
        _sql_repos.SQLUserRepository,
        engine=engine,
    )

    shortlink_repository = providers.Singleton(
        _sql_repos.SQLShortlinkRepository,
        engine=engine,
    )

    auth_token_repository = providers.Singleton(
        _sql_repos.SQLAuthTokenRepository,
        engine=engine,
    )

    auth_token_service = providers.Singleton(
        _sql_services.SQLAuthTokenService,
        engine=engine,
        auth_token_repository=auth_token_repository,
        user_repository=user_repository,
    )

    user_service = providers.Singleton(
        _sql_services.SQLUserService,
        engine=engine,
        user_repository=user_repository,
        auth_token_service=auth_token_service,
    )

    shortlink_service = providers.Singleton(
        _sql_services.SQLShortlinkService,
        engine=engine,
        shortlink_repository=shortlink_repository,
        user_repository=user_repository,
        auth_token_service=auth_token_service,
    )

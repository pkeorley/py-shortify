from fastapi import FastAPI

from .endpoints import (
    v1,
)
from .containers import Container


def create_app() -> FastAPI:
    container = Container()
    container.config.from_yaml("config.yaml")

    app = FastAPI()
    app.container = container  # type: ignore
    app.include_router(v1.get_router())

    return app


app = create_app()

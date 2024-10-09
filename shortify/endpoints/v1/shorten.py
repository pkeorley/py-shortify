from fastapi import APIRouter, Depends, HTTPException
from dependency_injector.wiring import inject, Provide

from . import common
from shortify.containers import Container
from shortify.services.service import schemas
from shortify.services.service import abc as _abc_service


router = APIRouter(prefix="/shorten")


@router.post("", status_code=201)
@inject
def create_shortlink(
    input: schemas.ShortlinkCreateInput,
    credentials: common.CredentialsHeader,
    shortlinks_service: _abc_service.ShortlinkService = Depends(
        Provide[Container.shortlink_service]
    ),
):
    auth_token = credentials.credentials

    try:
        return shortlinks_service.create(
            auth_token=auth_token,
            input=input,
        )
    except ValueError:
        return HTTPException(
            status_code=409,
            detail=f"Shortlink with name {input.name!r} already exists",
        )


def get_router() -> APIRouter:
    return router

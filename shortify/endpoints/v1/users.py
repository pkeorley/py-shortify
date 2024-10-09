from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide

from . import common
from shortify.containers import Container
from shortify.services.service import abc as _abc_service


router = APIRouter(prefix="/users")


@router.get("", status_code=200)
@inject
def retrieve_the_current_user(
    credentials: common.CredentialsHeader,
    auth_token_service: _abc_service.AuthTokenService = Depends(
        Provide[Container.auth_token_service],
    ),
):
    auth_token = credentials.credentials
    return auth_token_service.get_user_by_token(auth_token)


@router.post("", status_code=201)
@inject
def create_user(
    user_service: _abc_service.UserService = Depends(
        Provide[Container.user_service],
    ),
):
    return user_service.create()


def get_router() -> APIRouter:
    return router

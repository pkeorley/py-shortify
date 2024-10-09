from fastapi import APIRouter, Depends, HTTPException, status
from dependency_injector.wiring import inject, Provide

from shortify.containers import Container
from shortify.services.service import abc as _abc_service


router = APIRouter(prefix="/shortlinks")


@router.get("/{name}", status_code=200)
@inject
def receive_shortlink(
    name: str,
    shortlinks_service: _abc_service.ShortlinkService = Depends(
        Provide[Container.shortlink_service]
    ),
):
    shortlink_model = shortlinks_service.get_by_name(name)

    if shortlink_model is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No shortlink found with name {name!r}",
        )

    return shortlink_model


@router.get("", status_code=200)
@inject
def receive_a_list_of_shortened_links(
    shortlink_service: _abc_service.ShortlinkService = Depends(
        Provide[Container.shortlink_service],
    ),
):
    return shortlink_service.get_all()


def get_router() -> APIRouter:
    return router

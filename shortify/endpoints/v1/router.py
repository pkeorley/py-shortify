from fastapi import APIRouter

from . import (
    users,
    shorten,
    shortlinks,
)


router = APIRouter(prefix="/api/v1")
router.include_router(users.get_router())
router.include_router(shorten.get_router())
router.include_router(shortlinks.get_router())


def get_router() -> APIRouter:
    return router

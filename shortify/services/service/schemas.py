import uuid
import secrets

from pydantic import BaseModel, Field


class ShortlinkCreateInput(BaseModel):
    name: str

    url: str


class AuthTokenCreateInput(BaseModel):
    token: str = Field(default_factory=lambda: secrets.token_urlsafe(32))

    user: uuid.UUID


class Response(BaseModel):
    id: uuid.UUID


class UserResponse(Response):
    auth_token: str

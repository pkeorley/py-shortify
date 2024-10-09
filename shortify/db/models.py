import typing
import uuid
from sqlmodel import Field, SQLModel, Relationship


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    shortlinks: typing.List["Shortlink"] = Relationship(back_populates="user")

    auth_tokens: typing.List["AuthToken"] = Relationship(back_populates="user")


class Shortlink(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    name: str

    url: str

    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)

    user: User = Relationship(back_populates="shortlinks")


class AuthToken(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    token: str

    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)

    user: User = Relationship(back_populates="auth_tokens")

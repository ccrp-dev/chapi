from typing import Self

from fastapi import Request
from pydantic import BaseModel, Field

from chapi import __version__

from .link import Link


class LandingPage(BaseModel):
    title: str = ''
    description: str = ''
    links: list[Link] = Field(default_factory=list)

    @classmethod
    def from_request(cls, request: Request) -> Self:
        links = [
            Link.root_link(request),
            Link.self_link(request),
        ]

        return cls(
            title=request.app.title,
            description=request.app.description,
            links=links,
        )


class VersionInfo(BaseModel):
    version: str
    links: list[Link] = Field(default_factory=list)

    @classmethod
    async def from_request(cls, request: Request) -> Self:
        return cls(
            version=__version__,
        )

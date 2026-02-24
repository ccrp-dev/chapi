from __future__ import annotations

from fastapi import APIRouter, Request

from chapi.api.models.root import LandingPage, VersionInfo
from chapi.api.tags import Tags

router: APIRouter = APIRouter()


@router.get(
    '/',
    tags=[Tags.ROOT],
)
async def get_landing_page(request: Request) -> LandingPage:
    return LandingPage.from_request(request)


@router.get(
    '/version',
    tags=[Tags.ROOT],
)
async def get_version(request: Request) -> VersionInfo:
    return await VersionInfo.from_request(request)

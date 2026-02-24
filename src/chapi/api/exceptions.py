from __future__ import annotations

from collections.abc import Sequence
from typing import Any, NoReturn

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class APIError(Exception):
    http_status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR

    def serialize(self) -> dict[str, Any]:
        return {
            'error_type': self.__class__.__name__,
            'status': self.http_status_code,
            'detail': str(self),
        }

    def to_json(self) -> JSONResponse:
        return JSONResponse(
            status_code=self.http_status_code,
            content=self.serialize(),
        )


async def api_error_handler(request: Request, exc: APIError) -> JSONResponse:
    if exc.http_status_code >= 500:
        request.app.state.logger.exception('Server Error')
    return exc.to_json()


class NotFoundError(APIError):
    http_status_code: int = status.HTTP_404_NOT_FOUND


class ValidationError(APIError):
    http_status_code: int = status.HTTP_422_UNPROCESSABLE_CONTENT
    errors: Sequence[dict[str, Any]] | None = None

    def __init__(
        self,
        *args,
        errors: Sequence[dict[str, Any]] | None = None,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.errors = errors

    def serialize(self) -> dict[str, Any]:
        content = super().serialize()
        content['errors'] = self.errors
        return content


async def request_validation_error_handler(
    request: Request,
    exc: RequestValidationError,
) -> NoReturn:
    errors = exc.errors()
    raise ValidationError(
        f'request validation failed: {len(errors)} errors',
        errors=errors,
    )

from collections.abc import Iterator

import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient

from chapi.api.app import get_app
from chapi.api.settings import Settings


@pytest.fixture
def test_settings(
    test_database: str,
) -> Settings:
    return Settings(
        PGDATABASE=test_database,
        db_migrate_on_app_startup=False,
    )


@pytest.fixture
def test_app(test_settings) -> FastAPI:
    return get_app(settings=test_settings)


@pytest.fixture
def test_client(test_app) -> Iterator[TestClient]:
    with TestClient(test_app) as client:
        yield client

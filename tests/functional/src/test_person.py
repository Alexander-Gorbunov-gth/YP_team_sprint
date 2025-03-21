from http import HTTPStatus

import aiohttp
import pytest

from tests.functional.settings import test_settings

from ..fixtures.es_data import PERSON_NAME, PERSON_UUID


@pytest.mark.asyncio
async def test_get_person_list(
    add_persons, http_client: aiohttp.ClientSession
):
    async with http_client.get(
        f"{test_settings.service_url}/api/v1/persons/"
    ) as response:
        assert response.status == HTTPStatus.OK


@pytest.mark.asyncio
async def test_get_person(add_person, http_client):
    url = test_settings.service_url + "/api/v1/persons/" + PERSON_UUID
    async with http_client.get(url) as response:
        assert response.status == HTTPStatus.OK
        result = await response.json()
        assert result.get("full_name") == PERSON_NAME

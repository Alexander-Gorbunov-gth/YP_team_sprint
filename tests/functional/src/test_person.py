import pytest
import aiohttp

from tests.functional.settings import test_settings



@pytest.mark.asyncio
async def test_get_genre_list(
    app_persons,
    http_client: aiohttp.ClientSession
):
    async with http_client.get(
        f"{test_settings.service_url}/api/v1/persons/"
    ) as response:
        assert response.status == 200


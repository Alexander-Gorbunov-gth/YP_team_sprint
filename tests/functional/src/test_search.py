import pytest

from tests.functional.settings import test_settings


@pytest.mark.asyncio
async def test_search(add_films, http_client):
    url = test_settings.service_url + '/api/v1/films'
    query_data = {'search': 'The Star'}
    async with http_client.get(url, params=query_data) as response:
        body = await response.json()
        status = response.status
    assert status == 200
    assert len(body) == 50

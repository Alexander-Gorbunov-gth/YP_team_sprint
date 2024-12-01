import pytest

from ..settings import test_settings

from ..fixtures.es_data import FILM_NAME, FILM_UUID

@pytest.mark.asyncio
async def test_film_list(add_films, http_client):
    url = test_settings.service_url + '/api/v1/films/'
    async with http_client.get(url) as response:
        response_data = await response.json()
        status = response.status
    assert status == 200
    assert len(response_data) == 50

    params = {}
    params['page'] = 2
    async with http_client.get(url, params=params) as response:
        second_page_response = await response.json()
        status = response.status

    assert status == 200
    assert len(second_page_response) == 10

    params = {}
    params['page_size'] = 20
    async with http_client.get(url, params=params) as response:
        page_size_response = await response.json()
        status = response.status

    assert status == 200
    assert len(page_size_response) == 20


@pytest.mark.asyncio
async def test_get_film(add_film, http_client):
    url = test_settings.service_url + '/api/v1/films/' + FILM_UUID
    async with http_client.get(url) as response:
        assert response.status == 200
        result = await response.json()
        assert result.get("title") == FILM_NAME
import pytest

from src.core.config import settings
from src.domain.exceptions import ShortUrlNotFound
from src.services.short_url import ShortUrlService
from tests.unit.repositories import FakeShortUrlRepository


@pytest.fixture
def fake_short_url_repository() -> FakeShortUrlRepository:
    return FakeShortUrlRepository()


@pytest.fixture
def short_url_service(fake_short_url_repository) -> ShortUrlService:
    return ShortUrlService(short_url_repository=fake_short_url_repository)


@pytest.fixture
def original_url():
    return "https://example.com"


@pytest.mark.asyncio
async def test_create_short_url(short_url_service, original_url):
    short_url = str(await short_url_service.create_short_url(original_url))
    short_url_copy = str(
        await short_url_service.create_short_url(original_url)
    )
    short_url_code = short_url.replace(settings.service.domain, "")

    assert settings.service.domain in short_url
    assert len(short_url_code) == settings.service.short_code_length
    assert short_url == short_url_copy


@pytest.mark.asyncio
async def test_get_original_url(short_url_service, original_url):
    short_url = str(await short_url_service.create_short_url(original_url))
    short_url_code = short_url.replace(settings.service.domain, "")
    original_url_request = await short_url_service.get_original_url(
        short_url_code
    )

    assert original_url_request == original_url


@pytest.mark.asyncio
async def test_delete_expired_urls(short_url_service, original_url):
    short_url = await short_url_service.create_short_url(original_url)
    await short_url_service.delete_expired_urls()
    
    with pytest.raises(ShortUrlNotFound):
        await short_url_service.get_original_url(
            str(short_url)
        )

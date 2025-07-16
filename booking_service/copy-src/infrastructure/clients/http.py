from httpx import AsyncClient

httpx_client: AsyncClient | None = None


def get_httpx_client() -> AsyncClient:
    return httpx_client

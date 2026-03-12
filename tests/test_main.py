from httpx import AsyncClient, ASGITransport
from main import app


async def test_root_endpoint_returns_hello_world() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/")
        assert response.status_code == 200
        assert "<h1>Hello</h1>" in response.text

import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch
from io import BytesIO
from pdf_service.app.main import app
from pdf_service.app.dependencies import get_current_user

class FakeUser:
    id = "12345"
    name = "TestName"
    surname = "TestSurname"
    date_of_birth = "2023-02-15"

@pytest.mark.asyncio
async def test_download_pdf_success():
    app.dependency_overrides[get_current_user] = lambda: FakeUser()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        with patch("pdf_service.app.services.PDFService.generate_pdf") as mocked_pdf:
            mock_buffer = BytesIO(b"fake pdf content")
            mocked_pdf.return_value = mock_buffer

            response = await ac.get("api/pdf/download", headers={"Authorization": "Bearer valid-token"})

            assert response.status_code == 200
            assert response.headers["content-type"] == "application/pdf"
            assert "attachment; filename=profile_12345.pdf" in response.headers["content-disposition"]
            assert response.content == b"fake pdf content"

    app.dependency_overrides = {}


@pytest.mark.asyncio
async def test_download_pdf_no_token():
    app.dependency_overrides = {}

    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("api/pdf/download")

        assert response.status_code == 401
        assert response.json()["detail"] == "Missing or invalid Authorization header"


@pytest.mark.asyncio
async def test_download_pdf_invalid_token():
    app.dependency_overrides = {}

    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        headers = {"Authorization": "Bearer this-is-not-a-valid-token"}
        response = await ac.get("api/pdf/download", headers=headers)

        assert response.status_code == 401
        assert "detail" in response.json()
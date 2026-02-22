import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, AsyncMock
from auth_service.app.main import app


@pytest.mark.asyncio
async def test_login_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        with patch("auth_service.app.services.AuthService.authenticate", new_callable=AsyncMock) as mocked_auth:
            mocked_auth.return_value = "fake-token"

            response = await ac.post("api/auth/login", json={
                "email": "test@example.com",
                "password": "password123"
            })

            assert response.status_code == 200
            assert response.json()["access_token"] == "fake-token"


@pytest.mark.asyncio
async def test_login_invalid_credentials():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        path = "auth_service.app.services.AuthService.authenticate"
        with patch(path, new_callable=AsyncMock) as mocked_auth:
            mocked_auth.side_effect = ValueError("Incorrect email or password")

            response = await ac.post("api/auth/login", json={
                "email": "wrong@example.com",
                "password": "wrongpassword"
            })

            assert response.status_code == 401
            assert response.json() == {
                "detail":
                    {
                        "error": "Auth Error",
                        "message": "Incorrect email or password"
                    }
            }


@pytest.mark.asyncio
async def test_login_invalid_email_format():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("api/auth/login", json={
            "email": "not-an-email",
            "password": "password123"
        })

        assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_missing_fields():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("api/auth/login", json={
            "email": "test@example.com"
        })

        assert response.status_code == 422


@pytest.mark.asyncio
async def test_signup_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        path = "auth_service.app.services.AuthService.create_account"
        mock_user = {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "name": "Ivan",
            "surname": "Ivanov",
            "email": "ivan@example.com",
            "date_of_birth": "2000-01-01"
        }

        with patch(path, new_callable=AsyncMock) as mocked_signup:
            mocked_signup.return_value = mock_user

            response = await ac.post("api/auth/signup", json={
                "name": "Ivan",
                "surname": "Ivanov",
                "email": "ivan@example.com",
                "date_of_birth": "2000-01-01",
                "password": "strongpassword123"
            })

            assert response.status_code == 201
            assert response.json()["email"] == "ivan@example.com"
            assert "password" not in response.json()


@pytest.mark.asyncio
async def test_signup_email_already_exists():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        path = "auth_service.app.services.AuthService.create_account"
        with patch(path, new_callable=AsyncMock) as mocked_signup:
            mocked_signup.side_effect = ValueError("Email must be unique")

            response = await ac.post("api/auth/signup", json={
                "name": "Ivan",
                "surname": "Ivanov",
                "email": "existing@example.com",
                "date_of_birth": "2000-01-01",
                "password": "password123"
            })

            assert response.status_code == 400
            assert response.json() == {
                'detail':
                    {
                        'error': 'Registration Error',
                        'message': 'Email must be unique'
                    }
            }


@pytest.mark.asyncio
async def test_signup_invalid_date_format():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("api/auth/signup", json={
            "name": "Ivan",
            "surname": "Ivanov",
            "email": "ivan@example.com",
            "date_of_birth": "not-a-date",
            "password": "password123"
        })

        assert response.status_code == 422

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import HTTPException
from datetime import timedelta
from app.services.auth import AuthService
from app.schemas.auth import LoginDto
from app.services.user import UserService
from app.core.security import create_access_token, create_refresh_token


@pytest.mark.asyncio
async def test_login_success():
    # Arrange
    mock_user_service = AsyncMock(spec=UserService)
    mock_session = AsyncMock()
    service = AuthService(user_service=mock_user_service, db_session=mock_session)

    # Crear un mock para el usuario
    user_data = MagicMock()
    user_data.id = "user_1"
    user_data.email = "test@example.com"
    user_data.name = "Test User"
    user_data.password = "$2b$12$M5J4qAxC50WDjEQmPLjPWeUwZpGuAfeZoxdEo8LKvBl57/XjbCXVy"

    mock_user_service.find_by_email.return_value = user_data
    with patch("app.core.security.verify_password", return_value=True):
        with patch("app.core.security.create_access_token", return_value="access_token"):
            with patch("app.core.security.create_refresh_token", return_value="refresh_token"):
                # Act
                dto = LoginDto(email="test@example.com", password="123")
                result = await service.login(dto)

    # Assert
    assert result["user"]["id"] == "user_1"
    mock_user_service.find_by_email.assert_called_once_with("test@example.com")



@pytest.mark.asyncio
async def test_login_invalid_credentials():
    # Arrange
    mock_user_service = AsyncMock(spec=UserService)
    mock_session = AsyncMock()
    service = AuthService(user_service=mock_user_service, db_session=mock_session)

    mock_user_service.find_by_email.return_value = None
    with patch("app.core.security.verify_password", return_value=False):
        # Act & Assert
        dto = LoginDto(email="test@example.com", password="password")
        with pytest.raises(HTTPException) as exc_info:
            await service.login(dto)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid credentials or user not found"
    mock_user_service.find_by_email.assert_called_once_with("test@example.com")

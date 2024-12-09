import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.models.user import User
from app.schemas.user import CreateUserDto
from app.services.user import UserService

@pytest.mark.asyncio
async def test_create_user_user_does_not_exist():
    # Arrange
    mock_session = AsyncMock()
    mock_session.execute.return_value.scalar_one_or_none = AsyncMock(return_value=None)
    mock_session.add = AsyncMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()
    user_service = UserService(db_session=mock_session)
    dto = CreateUserDto(email="test@example.com", name="Test User", password="password123")

    # Act
    result = await user_service.create_user(dto)

    # Assert
    assert result["email"] == "test@example.com"
    assert "password" not in result
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()

@pytest.mark.asyncio
async def test_create_user_user_already_exists():
    # Arrange
    mock_session = AsyncMock()
    mock_session.execute.return_value.scalar_one_or_none = AsyncMock(return_value=User(email="test@example.com"))
    user_service = UserService(db_session=mock_session)
    dto = CreateUserDto(email="test@example.com", name="Test User", password="password123")

    # Act & Assert
    with pytest.raises(HTTPException) as excinfo:
        await user_service.create_user(dto)
    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "User already exists"

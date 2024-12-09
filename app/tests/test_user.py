from unittest.mock import AsyncMock, MagicMock
import pytest
from fastapi import HTTPException
from app.services.user import UserService
from app.models.user import User
from app.schemas.user import CreateUserDto
from app.core.exceptions import UserNotFoundException
from app.models.favorite import Favorite

@pytest.mark.asyncio
async def test_create_user_user_does_not_exist():
    # Arrange
    mock_session = AsyncMock()

    # Simular el resultado de `execute` como un objeto con `scalar_one_or_none` que devuelve None
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_session.execute.return_value = mock_result

    user_service = UserService(db_session=mock_session)
    dto = CreateUserDto(email="test@example.com", name="Test User", password="password123")

    # Act
    result = await user_service.create_user(dto)

    # Assert
    assert result["email"] == "test@example.com"
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

@pytest.mark.asyncio
async def test_find_by_email_user_exists():
    # Arrange
    mock_session = AsyncMock()
    mock_user = User(id="123", email="test@example.com", name="Test User")
    execute_mock = MagicMock()
    execute_mock.scalar_one_or_none.return_value = mock_user
    mock_session.execute.return_value = execute_mock

    user_service = UserService(db_session=mock_session)

    # Act
    user = await user_service.find_by_email("test@example.com")

    # Assert
    assert user.email == "test@example.com"
    assert user.id == "123"
    assert user.name == "Test User"

@pytest.mark.asyncio
async def test_find_by_email_user_not_found():
    # Arrange
    mock_session = AsyncMock()
    execute_mock = MagicMock()
    execute_mock.scalar_one_or_none.return_value = None
    mock_session.execute.return_value = execute_mock

    user_service = UserService(db_session=mock_session)

    # Act & Assert
    with pytest.raises(UserNotFoundException) as excinfo:
        await user_service.find_by_email("notfound@example.com")
    assert "User not found" in str(excinfo.value)

@pytest.mark.asyncio
async def test_find_by_id_user_exists():
    # Arrange
    mock_session = AsyncMock()
    mock_user = User(id="123", email="test@example.com", name="Test User")
    execute_mock = MagicMock()
    execute_mock.scalar_one_or_none.return_value = mock_user
    mock_session.execute.return_value = execute_mock

    user_service = UserService(db_session=mock_session)

    # Act
    user = await user_service.find_by_id("123")

    # Assert
    assert user.email == "test@example.com"
    assert user.id == "123"
    assert user.name == "Test User"

@pytest.mark.asyncio
async def test_find_by_id_user_not_found():
    # Arrange
    mock_session = AsyncMock()
    execute_mock = MagicMock()
    execute_mock.scalar_one_or_none.return_value = None
    mock_session.execute.return_value = execute_mock

    user_service = UserService(db_session=mock_session)

    # Act & Assert
    with pytest.raises(UserNotFoundException) as excinfo:
        await user_service.find_by_id("456")
    assert "User not found" in str(excinfo.value)

@pytest.mark.asyncio
async def test_add_favorite_success():
    # Arrange
    mock_session = AsyncMock()
    mock_user = User(id="123", email="test@example.com", name="Test User")
    execute_mock_user = MagicMock()
    execute_mock_user.scalar_one_or_none.return_value = mock_user

    execute_mock_favorite = MagicMock()
    execute_mock_favorite.scalar_one_or_none.return_value = None

    execute_mock_user_favorites = MagicMock()
    execute_mock_user_favorites.scalars().all.return_value = []

    mock_session.execute.side_effect = [execute_mock_user, execute_mock_favorite, execute_mock_user_favorites]
    mock_session.add = AsyncMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    user_service = UserService(db_session=mock_session)
    user_dict = {"username": "test@example.com"}
    match_id = "21"

    # Act
    response = await user_service.add_favorite(user_dict, match_id)

    # Assert
    print(response)
    assert response["id"] == "123"
    assert response["favorites"] == []
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()

@pytest.mark.asyncio
async def test_add_favorite_already_exists():
    # Arrange
    mock_session = AsyncMock()
    mock_user = User(id="123", email="test@example.com", name="Test User")
    execute_mock_user = MagicMock()
    execute_mock_user.scalar_one_or_none.return_value = mock_user

    execute_mock_favorite = MagicMock()
    execute_mock_favorite.scalar_one_or_none.return_value = Favorite(matchId="match_456")

    mock_session.execute.side_effect = [execute_mock_user, execute_mock_favorite]

    user_service = UserService(db_session=mock_session)
    user_dict = {"username": "test@example.com"}
    match_id = "match_456"

    # Act & Assert
    with pytest.raises(HTTPException) as excinfo:
        await user_service.add_favorite(user_dict, match_id)
    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Favorite already exists"

@pytest.mark.asyncio
async def test_remove_favorite_success():
    # Arrange
    mock_session = AsyncMock()
    mock_user = User(id="123", email="test@example.com", name="Test User")
    mock_favorite = Favorite(userId="123", matchId="match_456")

    execute_mock_user = MagicMock()
    execute_mock_user.scalar_one_or_none.return_value = mock_user

    execute_mock_favorite = MagicMock()
    execute_mock_favorite.scalar_one_or_none.return_value = mock_favorite

    execute_mock_user_favorites = MagicMock()
    execute_mock_user_favorites.scalars().all.return_value = []

    mock_session.execute.side_effect = [execute_mock_user, execute_mock_favorite, execute_mock_user_favorites]
    mock_session.delete = AsyncMock()
    mock_session.commit = AsyncMock()

    user_service = UserService(db_session=mock_session)
    user_dict = {"username": "test@example.com"}
    match_id = "match_456"

    # Act
    response = await user_service.remove_favorite(user_dict, match_id)

    # Assert
    assert response["id"] == "123"
    assert response["favorites"] == []
    mock_session.delete.assert_called_once()
    mock_session.commit.assert_called_once()

@pytest.mark.asyncio
async def test_remove_favorite_not_found():
    # Arrange
    mock_session = AsyncMock()
    mock_user = User(id="123", email="test@example.com", name="Test User")

    execute_mock_user = MagicMock()
    execute_mock_user.scalar_one_or_none.return_value = mock_user

    execute_mock_favorite = MagicMock()
    execute_mock_favorite.scalar_one_or_none.return_value = None

    mock_session.execute.side_effect = [execute_mock_user, execute_mock_favorite]

    user_service = UserService(db_session=mock_session)
    user_dict = {"username": "test@example.com"}
    match_id = "match_456"

    # Act & Assert
    with pytest.raises(HTTPException) as excinfo:
        await user_service.remove_favorite(user_dict, match_id)
    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Favorite not found"

import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.services.user import UserService
from app.models.user import User
from app.models.favorite import Favorite
from app.schemas.user import CreateUserDto
from app.core.exceptions import UserNotFoundException

# Fixtures comunes para los tests
@pytest.fixture
def mock_db_session():
    return AsyncMock(spec=AsyncSession)

@pytest.fixture
def user_service(mock_db_session):
    return UserService(mock_db_session)

@pytest.fixture
def test_user():
    return User(id="123", email="test@example.com", name="Test User", password="hashed_password")

@pytest.fixture
def test_favorite():
    return Favorite(id="456", userId="123", matchId="match_123")

# Test del método create_user
@pytest.mark.asyncio
async def test_create_user_success(user_service, mock_db_session):
    # Mockear un resultado vacío para que el usuario no exista
    mock_db_session.execute.return_value.scalar_one_or_none.return_value = None

    # Crear DTO para el usuario
    dto = CreateUserDto(email="test@example.com", name="Test User", password="securepassword")

    # Mockear el commit y refresh
    mock_db_session.commit = AsyncMock()
    mock_db_session.refresh = AsyncMock()

    result = await user_service.create_user(dto)

    assert result["email"] == "test@example.com"
    assert result["name"] == "Test User"
    assert "hashed_password" not in result  # Asegurarse de que no se filtra la contraseña

@pytest.mark.asyncio
async def test_create_user_already_exists(user_service, mock_db_session, test_user):
    # Mockear un resultado indicando que el usuario ya existe
    mock_db_session.execute.return_value.scalar_one_or_none.return_value = test_user

    dto = CreateUserDto(email="test@example.com", name="Test User", password="securepassword")

    with pytest.raises(HTTPException) as exc_info:
        await user_service.create_user(dto)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "User already exists"

# Test del método find_by_email
@pytest.mark.asyncio
async def test_find_by_email_success(user_service, mock_db_session, test_user):
    # Mockear un resultado indicando que se encontró el usuario
    mock_db_session.execute.return_value.scalar_one_or_none.return_value = test_user

    result = await user_service.find_by_email("test@example.com")

    assert result == test_user

@pytest.mark.asyncio
async def test_find_by_email_not_found(user_service, mock_db_session):
    # Mockear un resultado vacío indicando que no se encontró el usuario
    mock_db_session.execute.return_value.scalar_one_or_none.return_value = None

    with pytest.raises(UserNotFoundException):
        await user_service.find_by_email("notfound@example.com")

# Test del método add_favorite
@pytest.mark.asyncio
async def test_add_favorite_success(user_service, mock_db_session, test_user, test_favorite):
    # Mockear que el usuario existe y no tiene el favorito
    mock_db_session.execute.side_effect = [
        MagicMock(scalar_one_or_none=AsyncMock(return_value=test_user)),  # Usuario encontrado
        MagicMock(scalar_one_or_none=AsyncMock(return_value=None)),  # Favorito no existe
        MagicMock(scalars=AsyncMock(return_value=[test_favorite]))  # Lista de favoritos actualizada
    ]

    user_data = {"username": "test@example.com"}
    result = await user_service.add_favorite(user_data, "match_123")

    assert result["email"] == "test@example.com"
    assert "match_123" in result["favorites"]

@pytest.mark.asyncio
async def test_add_favorite_already_exists(user_service, mock_db_session, test_user, test_favorite):
    # Mockear que el favorito ya existe
    mock_db_session.execute.side_effect = [
        MagicMock(scalar_one_or_none=AsyncMock(return_value=test_user)),  # Usuario encontrado
        MagicMock(scalar_one_or_none=AsyncMock(return_value=test_favorite)),  # Favorito encontrado
    ]

    user_data = {"username": "test@example.com"}
    with pytest.raises(HTTPException) as exc_info:
        await user_service.add_favorite(user_data, "match_123")

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Favorite already exists"

# Test del método remove_favorite
@pytest.mark.asyncio
async def test_remove_favorite_success(user_service, mock_db_session, test_user, test_favorite):
    # Mockear que el usuario y el favorito existen
    mock_db_session.execute.side_effect = [
        MagicMock(scalar_one_or_none=AsyncMock(return_value=test_user)),  # Usuario encontrado
        MagicMock(scalar_one_or_none=AsyncMock(return_value=test_favorite)),  # Favorito encontrado
        MagicMock(scalars=AsyncMock(return_value=[])),  # Lista de favoritos vacía tras eliminar
    ]

    user_data = {"username": "test@example.com"}
    result = await user_service.remove_favorite(user_data, "match_123")

    assert result["email"] == "test@example.com"
    assert result["favorites"] == []

@pytest.mark.asyncio
async def test_remove_favorite_not_found(user_service, mock_db_session, test_user):
    # Mockear que el favorito no existe
    mock_db_session.execute.side_effect = [
        MagicMock(scalar_one_or_none=AsyncMock(return_value=test_user)),  # Usuario encontrado
        MagicMock(scalar_one_or_none=AsyncMock(return_value=None)),  # Favorito no encontrado
    ]

    user_data = {"username": "test@example.com"}
    with pytest.raises(HTTPException) as exc_info:
        await user_service.remove_favorite(user_data, "match_123")

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Favorite not found"

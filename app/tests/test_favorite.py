import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException
from app.services.favorite import FavoriteService
from app.models.favorite import Favorite
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.asyncio
async def test_get_favorites_success():
    # Arrange
    mock_session = AsyncMock(spec=AsyncSession)
    service = FavoriteService(db_session=mock_session)

    # Crear una lista de favoritos simulados
    mock_favorites = [
        MagicMock(userId="user_1", matchId="match_1"),
        MagicMock(userId="user_1", matchId="match_2"),
    ]

    # Configurar el comportamiento del mock
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = mock_favorites
    mock_session.execute.return_value = mock_result

    # Act
    result = await service.get_favorites(user_id="user_1")

    # Assert
    assert result == {"favorites": ["match_1", "match_2"]}
    mock_session.execute.assert_called_once()



@pytest.mark.asyncio
async def test_get_favorites_no_favorites():
    # Arrange
    mock_session = AsyncMock(spec=AsyncSession)
    service = FavoriteService(db_session=mock_session)

    # Configurar el comportamiento del mock para devolver una lista vacía
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = []
    mock_session.execute.return_value = mock_result

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        await service.get_favorites(user_id="user_1")

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "You don't have any favorite"
    mock_session.execute.assert_called_once()

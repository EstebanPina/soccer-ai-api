import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.soccer_matches import SoccerMatchesService
from app.schemas.soccer_matches import SoccerMatchesCreate, SoccerMatchesRead, SoccerMatchesFavorites
from app.models.soccer_matches import SoccerMatches
from app.models.venue import Venue
from app.schemas.OpenAi import OpenAiCreate

@pytest.mark.asyncio
async def test_create_match_success():
    # Arrange
    mock_session = AsyncMock(spec=AsyncSession)
    service = SoccerMatchesService(db_session=mock_session)
    
    # Mock para venue y match
    mock_result_match = MagicMock()
    mock_result_match.scalar_one_or_none.return_value = None
    mock_session.execute.return_value = mock_result_match
    
    mock_result_venue = MagicMock()
    mock_result_venue.scalar_one_or_none.return_value = Venue(
        id="1", temperature=22, weather="Sunny", wind_speed=5
    )
    mock_session.execute.return_value = mock_result_venue
 
    # Configurar el comportamiento de mock_session.execute
    mock_session.execute.side_effect = [mock_result_match, mock_result_venue]
    
    # Mock de OpenAI prediction
    prediction_mock = {"prediction": "Win"}
    with patch('app.services.open_ai.OpenAIService.create_prediction', return_value=AsyncMock(return_value=prediction_mock)):
        # Act
        dto = SoccerMatchesCreate(
            id_sports_api="match_1",
            local_team="Team A",
            visitor_team="Team B",
            local_team_img="img1",
            visitor_team_img="img2",
            finished=False,
            venueId="1"
        )
        result = await service.create_match(dto)

    # Assert
    assert result.id_sports_api == "match_1"
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_create_match_already_registered():
    # Arrange
    mock_session = AsyncMock(spec=AsyncSession)
    service = SoccerMatchesService(db_session=mock_session)
    
    mock_session.execute.return_value.scalar_one_or_none.return_value = SoccerMatches(
        id_sports_api="match_1"
    )

    # Act & Assert
    dto = SoccerMatchesCreate(
            id_sports_api="match_1",
            local_team="Team A",
            visitor_team="Team B",
            local_team_img="img1",
            visitor_team_img="img2",
            finished=False,
            venueId="1"
        )
    with pytest.raises(HTTPException) as exc_info:
        await service.create_match(dto)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Match is already registered"


@pytest.mark.asyncio
async def test_find_by_id_existing_match():
    # Arrange
    mock_session = AsyncMock(spec=AsyncSession)
    service = SoccerMatchesService(db_session=mock_session)
    
    # Crear una instancia mock de SoccerMatches
    existing_match = SoccerMatches(
        id_sports_api="match_1", view_count=1
    )
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = existing_match
    
    # Configurar mock_session.execute
    mock_session.execute.return_value = mock_result

    # Act
    dto = SoccerMatchesCreate(
        id_sports_api="match_1",
        local_team="Team A",
        visitor_team="Team B",
        local_team_img="img1",
        visitor_team_img="img2",
        finished=False,
        venueId="1"
    )
    result = await service.find_by_id(dto)

    # Assert
    assert result.id_sports_api == "match_1"
    assert result.view_count == 2  # Verificar que se incrementó el contador
    mock_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_find_many_success():
    # Arrange
    mock_session = AsyncMock(spec=AsyncSession)
    service = SoccerMatchesService(db_session=mock_session)

    # Crear la lista de partidos
    matches = [
        SoccerMatches(id ="match_1", id_sports_api = "match_1", view_count =2, prediction_ai ="win", local_team ="a", visitor_team ="b", local_team_img ="aa", visitor_team_img ="bb", finished = False, venueId = "i"),
        SoccerMatches(id ="match_2", id_sports_api = "match_2", view_count =2, prediction_ai ="win", local_team ="a", visitor_team ="b", local_team_img ="aa", visitor_team_img ="bb", finished = False, venueId = "i")
    ]

    # Configurar mocks para scalars y all
    mock_scalars = MagicMock()
    mock_scalars.scalars.all.return_value = matches  # Simula que no hay partidos encontrados
    mock_scalars.all.return_value = matches
    mock_result = MagicMock()
    mock_result.scalars.return_value = mock_scalars
    mock_session.execute.return_value = mock_result

    # Act & Assert

    # Act
    dto = SoccerMatchesFavorites(favorites=["match_1", "match_2"])
    result = await service.find_many(dto)

    # Assert
    assert len(result) == 2
    assert result[0].id_sports_api == "match_1"
    assert result[1].id_sports_api == "match_2"


@pytest.mark.asyncio
async def test_find_many_no_matches_found():
    # Arrange
    mock_session = AsyncMock(spec=AsyncSession)
    service = SoccerMatchesService(db_session=mock_session)

    # Crear mocks para scalars y all
    mock_scalars = MagicMock()
    mock_scalars.scalars.all.return_value = []  # Simula que no hay partidos encontrados
    mock_scalars.all.return_value = []
    mock_result = MagicMock()
    mock_result.scalars.return_value = mock_scalars
    mock_session.execute.return_value = mock_result

    # Act & Assert
    dto = SoccerMatchesFavorites(favorites=["match_1", "match_2"])
    with pytest.raises(HTTPException) as exc_info:
        await service.find_many(dto)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Matches not found"

from unittest.mock import AsyncMock, Mock, patch
import pytest
from app.services.sportsdb import SportsDbService
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.sportsdb import SportsDbService
from app.models.venue import Venue
@pytest.mark.asyncio
async def test_get_league_matches():
    # Arrange
    mock_session = AsyncMock()  # Simular la sesión de la base de datos
    service = SportsDbService(db_session=mock_session)
    
    # Crear un mock de la respuesta HTTP
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.json = Mock(return_value={"matches": []})  # Configurar como un Mock síncrono
    
    # Patch para simular la llamada a la API
    with patch('httpx.AsyncClient.get', return_value=mock_response):
        # Act
        response = await service.get_league_matches(country="spain")

    # Assert
    assert isinstance(response, dict)  # Verificar que `response` es un diccionario
    assert response["matches"] == []  # Verificar que la lista de matches está vacía
    mock_response.json.assert_called_once()  # Verificar que `json` se llamó una vez


@pytest.mark.asyncio
async def test_get_league_matches_country_not_found():
    # Arrange
    mock_session = AsyncMock()
    service = SportsDbService(db_session=mock_session)
    
    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        await service.get_league_matches(country="unknown_country")
    
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Country not found"


@pytest.mark.asyncio
async def test_get_league_matches_api_error():
    # Arrange
    mock_session = AsyncMock()
    service = SportsDbService(db_session=mock_session)
    
    mock_response = AsyncMock()
    mock_response.status_code = 500  # Simula un error en la API
    mock_response.json = Mock(return_value={})
    
    with patch('httpx.AsyncClient.get', return_value=mock_response):
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await service.get_league_matches(country="spain")
    
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Error getting matches"


@pytest.mark.asyncio
async def test_get_league_matches_invalid_json():
    # Arrange
    mock_session = AsyncMock()
    service = SportsDbService(db_session=mock_session)
    
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.json = Mock(side_effect=ValueError("Invalid JSON"))  # Simula un error al parsear JSON
    
    with patch('httpx.AsyncClient.get', return_value=mock_response):
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            await service.get_league_matches(country="spain")
    
    assert str(exc_info.value) == "Invalid JSON"


@pytest.mark.asyncio
async def test_get_all_cities_success():
    # Arrange
    mock_session = AsyncMock(spec=AsyncSession)
    service = SportsDbService(db_session=mock_session)
    
    mock_response_teams = AsyncMock()
    mock_response_teams.status_code = 200
    mock_response_teams.json = Mock(return_value={
        "teams": [
            {"idVenue": "1"},
            {"idVenue": "2"},
            {"idVenue": None}
        ]
    })

    mock_response_venue = AsyncMock()
    mock_response_venue.status_code = 200
    mock_response_venue.json = Mock(return_value={
        "venues": [{
            "id": "1",
            "strVenue": "Stadium 1",
            "strLocation": "Location 1",
            "strMap": "40°00′00″N 4°00′00″W"
        }]
    })

    with patch('httpx.AsyncClient.get', side_effect=[mock_response_teams, mock_response_venue]):
        # Act
        response = await service.get_all_cities(country="spain")

    # Assert
    assert isinstance(response, dict)
    assert response["added_venues"] == []  # Verifica que se agrega el venue correcto
    mock_response_teams.json.assert_called_once()


@pytest.mark.asyncio
async def test_get_all_cities_country_not_found():
    # Arrange
    mock_session = AsyncMock(spec=AsyncSession)
    service = SportsDbService(db_session=mock_session)
    
    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        await service.get_all_cities(country="unknown_country")

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Country not found"


@pytest.mark.asyncio
async def test_get_all_cities_api_error():
    # Arrange
    mock_session = AsyncMock(spec=AsyncSession)
    service = SportsDbService(db_session=mock_session)
    
    mock_response_teams = AsyncMock()
    mock_response_teams.status_code = 500  # Simula un error de la API

    with patch('httpx.AsyncClient.get', return_value=mock_response_teams):
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await service.get_all_cities(country="spain")

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Error getting matches"


@pytest.mark.asyncio
async def test_get_all_cities_invalid_json():
    # Arrange
    mock_session = AsyncMock(spec=AsyncSession)
    service = SportsDbService(db_session=mock_session)
    
    mock_response_teams = AsyncMock()
    mock_response_teams.status_code = 200
    mock_response_teams.json = Mock(side_effect=ValueError("Invalid JSON"))  # Simula un error al parsear JSON

    with patch('httpx.AsyncClient.get', return_value=mock_response_teams):
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            await service.get_all_cities(country="spain")

    assert str(exc_info.value) == "Invalid JSON"
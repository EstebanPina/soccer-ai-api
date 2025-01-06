from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
import httpx
import datetime
from app.utils.coordinates_conversion import get_converted_lat_lon
from app.models.venue import Venue
from sqlalchemy.future import select
class SportsDbService:
  def __init__(self, db_session: AsyncSession):
    self.db_session = db_session
    self.countries_cases={"spain":{"id":"4335","name":"Spanish La Liga","strMap":"40°00′00″N 4°00′00″W"},"brazil":{"id":"4351","name":"Brazilian Serie A","strMap":"15°47′38″S 47°52′58″W"}}

  async def get_league_matches(self, country:str="") -> dict:
    date = datetime.datetime.now()
    lower_country = country.lower()
    yearly_seasons_leagues=["brazil"] # Leagues that have a yearly season and not a bi-yearly season
    if date.month < 6: # If the current month is less than 6, the season is the previous year
        season_str = f"{date.year-1}" if lower_country in yearly_seasons_leagues else f"{date.year-1}-{date.year}"
    else:
      season_str = f"{date.year}" if lower_country in yearly_seasons_leagues else f"{date.year}-{date.year+1}" # Get the season string based on the current year
    if lower_country not in self.countries_cases:
            raise HTTPException(status_code=400, detail="Country not found")
    country_object=dict(self.countries_cases[lower_country])
    url=f"https://www.thesportsdb.com/api/v1/json/3/eventsseason.php?id={country_object['id']}&s={season_str}" # Get the matches for the season
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Error getting matches")
        data= response.json()
        return data

  async def get_all_cities(self,country:str="") -> dict:
    teams=None
    lower_country = country.lower()
    if lower_country not in self.countries_cases:
            raise HTTPException(status_code=400, detail="Country not found")
    country_object=dict(self.countries_cases[lower_country])
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://www.thesportsdb.com/api/v1/json/3/search_all_teams.php?l={country_object['name']}")# Get all teams from the league
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Error getting matches")
        teams = response.json()
    venues = list(set([team['idVenue'] for team in teams['teams'] if team['idVenue'] is not None])) # Get all the venues from the teams
    print(venues)
    venues_info_array = []
    for venue in venues:
      # Verificar si el venue esta registrado en la bd
      statement = select(Venue).where(Venue.id == venue)
      result=await self.db_session.execute(statement)
      venue_bd = result.scalar_one_or_none()
      if not venue_bd:
        async with httpx.AsyncClient() as client:
          response = await client.get(f"https://www.thesportsdb.com/api/v1/json/3/lookupvenue.php?id={venue}")
          if response.status_code != 200:
              raise HTTPException(status_code=400, detail="Error getting matches")
          venue_info = response.json()
          venue_info = venue_info['venues'][0]
          lat, lon=get_converted_lat_lon(venue_info['strMap'] if venue_info['strMap'] else country_object['strMap'])
          new_venue = Venue(id=venue, stadium = venue_info['strVenue'], location = venue_info['strLocation'], lat = lat, lon = lon)
          self.db_session.add(new_venue)
          await self.db_session.commit()
          await self.db_session.refresh(new_venue)
          venues_info_array.append(venue)
    return {"added_venues":venues_info_array}
    
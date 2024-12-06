from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.models.user import User
from app.models.favorite import Favorite
from app.schemas.OpenAi import OpenAiCreate
from app.core.security import hash_password
from typing import Dict, Any
from app.core.exceptions import UserNotFoundException
from sqlalchemy.future import select
from openai import OpenAI
from app.core.config import settings
class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    async def create_prediction(self, dto: OpenAiCreate) -> Dict[str, Any]:
        # Verificar si el usuario ya existe
        prompt = f'''In the next format write a prediction for the soccer match between local: {dto.local_team} versus visitor: {dto.visitor_team} considering 
        the following information: Temperature is {dto.temperature}°C, Weather is {dto.weather}% and Wind speed is {dto.wind_speed} miles/hour.
        the format is:
        Análisis del Partido: 'local_team' vs 'visitor_team'
        Basado en las condiciones climáticas y el contexto actual, 'type of match like Equilibrado or Con ventaja para un equipo'.
        'temperature_description' 'weather description' y 'wind description'.
        'favored playstyle according with the conditions justified ' 'Prediction of the performance of the teams' 'Prediction of winner with a percentage'
        '''
        response = self.client.chat.completions.create(
            messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="gpt-4o-mini-2024-07-18",
  )
        print(response.choices[0].message.content)
        return response.choices[0].message.content
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.models.user import User
from app.models.favorite import Favorite
from app.schemas.user import CreateUserDto, AddFavoriteDto, UserResponse
from app.core.security import hash_password
from typing import Dict, Any
from app.core.exceptions import UserNotFoundException
from sqlalchemy.future import select

class UserService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(self, dto: CreateUserDto) -> Dict[str, Any]:
        # Verificar si el usuario ya existe
        statement = select(User).where(User.email == dto.email)
        result=await self.db_session.execute(statement)
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="User already exists")

        # Crear un nuevo usuario
        hashed_password = hash_password(dto.password)
        new_user = User(email=dto.email, name=dto.name, password=hashed_password)
        self.db_session.add(new_user)
        await self.db_session.commit()
        await self.db_session.refresh(new_user)

        # Excluir contraseña de la respuesta
        return {key: value for key, value in vars(new_user).items() if key != "hashed_password"}

    async def find_by_email(self, email: str) -> User:
        statement = select(User).where(User.email == email)
        result=await self.db_session.execute(statement)
        user=result.scalar_one_or_none()
        
        if not user:
            raise UserNotFoundException("User not found")
        return user

    async def find_by_id(self, user_id: str) -> User:
        statement = select(User).where(User.id == user_id)
        result=await self.db_session.execute(statement)
        user=result.scalar_one_or_none()
        if not user:
            raise UserNotFoundException("User not found")
        return user

    async def add_favorite(self, user: Dict[str, str], match_id: str) -> Dict[str, Any]:
        # Obtener usuario
        username = user["username"]
        user = await self.find_by_email(username)

        # Verificar si el favorito ya existe
        statement = select(Favorite).where(Favorite.matchId == match_id)
        result=await self.db_session.execute(statement)
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Favorite already exists")

        # Crear un nuevo favorito
        new_favorite = Favorite(userId=user.id, matchId=match_id)
        self.db_session.add(new_favorite)
        await self.db_session.commit()
        await self.db_session.refresh(new_favorite)

        # Actualizar y devolver el usuario con favoritos
        statement_user_favorites = select(Favorite).where(Favorite.userId == user.id)
        user_favorites=await self.db_session.execute(statement_user_favorites)
        favorites = [fav.matchId for fav in user_favorites.scalars().all()]
        response={"id": user.id,"name":user.name, "email": user.email, "favorites": favorites}
        print(response)
        return response

    async def remove_favorite(self, user_id: Dict[str, str], match_id: str) -> Dict[str, Any]:
        # Obtener usuario
        username = user_id["username"]
        user = await self.find_by_email(username)

        # Verificar si el favorito existe
        statement = select(Favorite).where(Favorite.matchId == match_id)
        result=await self.db_session.execute(statement)
        favorite = result.scalar_one_or_none()
        if not favorite:
            raise HTTPException(status_code=400, detail="Favorite not found")

        # Eliminar favorito
        await self.db_session.delete(favorite)
        await self.db_session.commit()

        # Actualizar y devolver el usuario con favoritos restantes
        statement_user_favorites = select(Favorite).where(Favorite.userId == user.id)
        user_favorites=await self.db_session.execute(statement_user_favorites)
        favorites = [fav.matchId for fav in user_favorites.scalars().all()]
        return {"id": user.id, "email": user.email, "name": user.name, "favorites": favorites}

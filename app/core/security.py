from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
from app.core.config import settings
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Request, HTTPException, status
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Secretos y configuración de JWT
JWT_SECRET_KEY = settings.JWT_SECRET
JWT_REFRESH_SECRET_KEY = settings.JWT_REFRESH_SECRET
ALGORITHM = "HS256"

class RefreshTokenScheme(HTTPBearer):
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        authorization: str = request.headers.get("Authorization")
        if not authorization or not authorization.startswith("Refresh "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing authorization header",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return authorization


refresh_token_scheme = RefreshTokenScheme()
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(hours=1))  # Por defecto 1 hora de expiración
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(days=7))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, algorithm=ALGORITHM)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

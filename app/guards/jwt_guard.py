from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from app.core.config import settings

# Usamos OAuth2PasswordBearer para obtener el token del encabezado Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Función para verificar el JWT
def verify_jwt(token: str):
    try:
        # Decodificar el JWT usando pyjwt
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=["HS256"]
        )
        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Dependencia para proteger los endpoints
def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_jwt(token)

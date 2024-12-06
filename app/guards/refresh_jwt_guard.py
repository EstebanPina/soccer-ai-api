from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from app.core.config import settings
from app.core.security import RefreshTokenScheme

# Usamos OAuth2PasswordBearer para obtener el token del encabezado Authorization
refresh_token_scheme = RefreshTokenScheme()

# Función para verificar el Refresh Token
def verify_refresh_token(token: str):
    try:
        # Decodificar el Refresh Token usando pyjwt
        payload = jwt.decode(
            token,
            settings.JWT_REFRESH_SECRET,  # Usamos la clave secreta del refresh token
            algorithms=["HS256"]
        )
        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Dependencia para proteger los endpoints con Refresh Token
def get_refresh_token(token: str = Depends(refresh_token_scheme)):
    # Verificamos si el tipo de token es 'Refresh'
    print	(token)
    if token.split()[0] != "Refresh":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token type, expected 'Refresh'"
        )
    return verify_refresh_token(token.split()[1])  # Extraemos solo el token sin el 'Refresh'

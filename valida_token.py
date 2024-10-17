import datetime
from datetime import timedelta

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from oauthlib.oauth2 import WebApplicationClient
from starlette import status

client = WebApplicationClient("seu_client_id")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Criar Token

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, "sua_chave_secreta", algorithm="HS256")
    return encoded_jwt

# Validar token
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, "sua_chave_secreta", algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.JWTError:
        raise credentials_exception
    user = get_user(username)  # Função para buscar o usuário no banco de dados
    if user is None:
        raise credentials_exception
    return user

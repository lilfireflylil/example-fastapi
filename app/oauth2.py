from jose import jwt, JWTError # jwt stands for "JSON Web Token"
from datetime import datetime, timedelta
from . import schemas
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .config import settings


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes * 24 
# (60minutes * 24)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # expire = datetime.now(datetime.UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: int = payload.get("user_id")

        if not id:
            raise credentials_exception

        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception

    return token_data


oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")
def get_current_user(token: str = Depends(oauth2_schema)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail='Could not validate hehe credentials',
                                          headers={'WWW-Authenticate': 'Bearer'})
    
    return verify_access_token(token, credentials_exception)

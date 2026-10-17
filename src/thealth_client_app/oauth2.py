import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
from thealth_client_app.models.employee import TokenData
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from thealth_client_app import database

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = os.getenv("DB_SECRET_KEY")
ALGORITHM = os.getenv("DB_ALGORITHM")
EXPIRATION = 30

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRATION)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # type: ignore
        id = payload.get("sub")

        if id is None:
            raise credentials_exception
        return  TokenData(id=id)
    except InvalidTokenError as e:
        print("JWT ERROR: ", e)
        raise credentials_exception


def get_current_user(token: str = Depends(oauth2_scheme), conn = Depends(database.get_database)):
    credentials_exception = HTTPException(status_code=401, 
                                          detail=f"Invalid Credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    token_data = verify_token(token, credentials_exception)

    with conn.cursor() as cursor:
        cursor.execute("""SELECT * FROM employees WHERE id = %s""",
                        (token_data.id,))
        user = cursor.fetchone()

    return user
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException

from app.models import UserModel

load_dotenv()

EXPIRE_IN_MINUTE = int(os.getenv("JWT_EXP_MIN"))
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_scheme = HTTPBearer()

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password) 


def create_access_token(data: dict, expires_delta: timedelta = EXPIRE_IN_MINUTE*60):
    print(type(EXPIRE_IN_MINUTE))
    to_encode = data.copy()

    expire = (
        datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    )

    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
        creds: HTTPAuthorizationCredentials = Depends(oauth_scheme)
    ):
    credential_exp = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Please provide correct credentials.",
        headers={"WWW-Authenticate":"Bearer"},
    )
    try:
        token = creds.credentials.split(" ")[1]
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        email = payload.get("email")
        if email is None:
            raise credential_exp
    except JWTError:
        raise credential_exp
    
    user = await get_user_by_email(email)
    print(user)
    if user is None:
        raise credential_exp
    return user

async def get_user_by_email(email):
    user = await UserModel.filter(email=email).first()
    return user
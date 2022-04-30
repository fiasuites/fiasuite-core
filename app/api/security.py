from datetime import datetime, timedelta
from typing import Optional

# Third Parties
from passlib.context import CryptContext
from jose import JWTError, jwt

# FastAPi
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.api.schemas.auth_schema import TokenDataSchema

# API Folder
from app.api.schemas.user_schema import UserInDB, UserSchema

# Services Folder
from app.services.enums import UserRole

# to get a string like this run
# openssl rand -hex 32
SECRET_KEY = "8fd41ac098b88995604b44fb9124c31bfa8f36fd44077a70e1bee1d6dd016956"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "name": "John Doe",
        "email": "johndoe@326news.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
        "role": UserRole.User.value,
        "last_seen": str(datetime.today()),
        "date_joined": str(datetime.today()),
    },
}


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenDataSchema(username=username)
    except JWTError:
        raise credentials_exception

    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def fake_decode_token(token):
    return UserSchema(
        name="Nigeria 326 News",
        email="admin@326news.com",
        date_joined=datetime.today(),
        last_seen=datetime.today(),
        disabled=False,
        role=UserRole.User,
    )


def fake_hash_password(password: str):
    return "fakehashed" + password


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        print(user_dict)
        return UserInDB(**user_dict)


async def get_current_active_user(current_user: UserSchema = Depends(get_current_user)):
    print(current_user.disabled)
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


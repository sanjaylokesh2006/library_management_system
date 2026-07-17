import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import ValidationError
from sqlalchemy.orm import Session

from backend.app.config import settings
from backend.app.database import get_db
from backend.app.models.user import User
from backend.app.schemas.auth import TokenData, Token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify if the plain password matches the hashed password.
    
    Args:
        plain_password (str): The plain text password to be verified.
        hashed_password (str): The hashed password stored in the database.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Generate a hashed version of the given password.

    Args:
        password (str): The plain text password to be hashed.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)

async def authenticate_user(db: Session, username: str, password: str) -> User | None:
    """
    Authenticate a user by checking the provided credentials against the database.

    Args:
        db (Session): The SQLAlchemy session object.
        username (str): The username of the user to be authenticated.
        password (str): The plain text password provided by the user.

    Returns:
        User | None: The authenticated user if successful, None otherwise.
    """
    user = await User.get_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Create a JWT access token with the given data and expiration time.

    Args:
        data (dict): The data to be encoded in the token.
        expires_delta (timedelta | None): The time until the token expires. If None, the default expiration is used.

    Returns:
        str: The JWT access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Get the current authenticated user from the JWT token.

    Args:
        token (str): The JWT access token.
        db (Session): The SQLAlchemy session object.

    Returns:
        User: The current authenticated user.

    Raises:
        HTTPException: If the token is invalid or expired.
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except (jwt.PyJWTError, ValidationError):
        raise credentials_exception
    user = await User.get_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Get the current active authenticated user.

    Args:
        current_user (User): The current authenticated user.

    Returns:
        User: The current active authenticated user.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.app import crud, models, schemas
from backend.app.api.deps import get_db, get_current_user
from backend.app.core.config import settings
from backend.app.core.security import create_access_token, verify_password

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = crud.user.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user


@router.post("/users/", response_model=schemas.User)
async def create_user(
    user: schemas.UserCreate, db: Session = Depends(get_db)
):
    db_user = crud.user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.user.create_user(db=db, user=user)


@router.post("/users/{user_id}/items/", response_model=schemas.Item)
async def create_item_for_user(
    item: schemas.ItemCreate,
    user_id: int,
    db: Session = Depends(get_db),
):
    return crud.item.create_item_with_owner(db=db, item=item, owner_id=user_id)


@router.get("/users/{user_id}/items/", response_model=list[schemas.Item])
async def read_user_items(
    user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return crud.item.get_items_by_owner(db=db, owner_id=user_id, skip=skip, limit=limit)


@router.get("/items/", response_model=list[schemas.Item])
async def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.item.get_multi(db, skip=skip, limit=limit)
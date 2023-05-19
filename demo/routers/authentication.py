from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import auth.oauth as oauth
import demo.schemas.user as user_schema
from auth.hash import Hash

from ..database import session_local
from ..models.user import User

router = APIRouter(tags=["authentication"])


def get_db():
    db = session_local()

    try:
        yield db
    finally:
        db.close()


@router.post("/token", response_model=user_schema.UserOut)
def get_token(
    request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials"
        )
    if not Hash.verify_password(user.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password"
        )
    access_token = oauth.create_access_token(data={"sub": user.username})
    return {
        "access_token": access_token,
        "user_id": user.id,
        "username": user.username,
    }

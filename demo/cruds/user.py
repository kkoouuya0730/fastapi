from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session

from auth.hash import Hash

from ..models.user import User as UserModel
from ..schemas.user import User, UserCreate


def create_user(db: Session, request: UserCreate) -> User:
    new_user = UserModel(
        username=request.username,
        email=request.email,
        password=Hash.get_password_hash(request.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_username(db: Session, username: str) -> User:
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user} not found",
        )
    return user

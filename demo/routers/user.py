from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from demo.cruds.user import create_user
from demo.schemas.user import User, UserCreate

from ..database import get_db

router = APIRouter(prefix="/user", tags=["user"])


# response_model_exclude: 指定したプロパティを除外することができるが、OpenAPIのドキュメントからは消えない
@router.post("/", response_model=User, response_model_exclude={"password"})
def create_todo(request: UserCreate, db: Session = Depends(get_db)):
    user = create_user(db, request)
    if not user:
        raise HTTPException(status_code=404, detail="User create failed")
    return user

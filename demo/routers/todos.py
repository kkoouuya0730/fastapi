from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import demo.cruds.todo as todo_crud
import demo.schemas.todo as todo_schema
from auth.oauth import get_current_user

from ..database import get_db

router = APIRouter(
    prefix="/todos", tags=["todos"], responses={404: {"description": "Not Found"}}
)


"""
Noneのエラーハンドリングだったりをハンドリングする
(crudでdbとちゃんとやり取りできたか否かなどをエラーハンドリングする)
"""


@router.get("/", response_model=List[todo_schema.Todo])
def list_todos(
    db: Session = Depends(get_db), current_user: str = Depends(get_current_user)
):
    todos = todo_crud.get_todos(db)
    if len(todos) == 0:
        raise HTTPException(status_code=404, detail="There is no Todos")
    return todos


@router.get("/{id}", response_model=todo_schema.Todo)
def get_todo(id: UUID, db: Session = Depends(get_db)):
    todo = todo_crud.get_todo(db, id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not Found")
    return todo


@router.post("/", response_model=todo_schema.Todo)
def create_todo(todo_body: todo_schema.TodoCreate, db: Session = Depends(get_db)):
    return todo_crud.create_todo(db, todo_body)


@router.put("/{id}", response_model=todo_schema.Todo)
def update_todo(
    todo_body: todo_schema.TodoCreate, id: UUID, db: Session = Depends(get_db)
):
    original = todo_crud.get_todo(db, id)
    if not original:
        raise HTTPException(status_code=404, detail="Todo not Found")
    return todo_crud.update_todo(db, original, todo_body)

from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
import demo.schemas.todo as todo_schema
import demo.cruds.todo as todo_crud
import demo.cruds.done as done_crud

from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter(
    prefix="/done",
    tags=["done", "todos"],
    responses={404: {"description": "Not Found"}},
)


@router.put("/{todo_id}", response_model=todo_schema.Todo)
def update_todo_done(todo_id: UUID, db: Session = Depends(get_db)):
    todo = todo_crud.get_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not Found")
    return done_crud.update_todo_done(db, todo)
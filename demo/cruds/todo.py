from datetime import datetime, timedelta, timezone
from logging import getLogger
from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from log.log import ApiName, start_and_end_logging

from ..models.todo import Todo as TodoModel
from ..schemas.todo import Todo, TodoCreate

JST = timezone(timedelta(hours=+9), "JST")


def get_todos(db: Session) -> List[Todo]:
    try:
        todo_list = db.query(TodoModel).all()
    except Exception as e:
        print(e)
    return todo_list


def get_todo(db: Session, id: UUID) -> Todo:
    try:
        todo = db.query(TodoModel).filter(TodoModel.id == id).first()
    except Exception as e:
        print(e)
    return todo


@start_and_end_logging(ApiName.TODO)
def create_todo(address_base, request_id, db: Session, todo: TodoCreate) -> Todo:
    try:
        new_todo = TodoModel(**todo.dict())
        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)
    except Exception as e:
        print(e)
    return new_todo


def update_todo(db: Session, origin: Todo, todo: TodoCreate) -> Todo:
    origin.title = todo.title
    origin.description = todo.description
    origin.updated_at = datetime.now(JST)
    try:
        db.add(origin)
        db.commit()
        db.refresh(origin)
    except Exception as e:
        print(e)
    return origin

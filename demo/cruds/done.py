from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from ..schemas.todo import Todo

JST = timezone(timedelta(hours=+9), "JST")


def update_todo_done(db: Session, origin: Todo) -> Todo:
    origin.is_done = not origin.is_done
    origin.updated_at = datetime.now(JST)
    try:
        db.add(origin)
        db.commit()
        db.refresh(origin)
    except Exception as e:
        print(e)
    return origin

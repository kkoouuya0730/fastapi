from fastapi.testclient import TestClient

from demo import __version__
from demo.database import get_db
from demo.main import app


def temp_db(f):
    def func(SessionLocal, *args, **kwargs):
        def override_get_db():
            try:
                db = SessionLocal()
                yield db
            finally:
                db.close()

        app.dependency_overrides[get_db] = override_get_db
        f(*args, **kwargs)
        app.dependency_overrides[get_db] = get_db

    return func


client = TestClient(app)


def test_version():
    assert __version__ == "0.1.0"


# # def test_list_todos():
# #     response = client.get("/todos/")
# #     assert response.status_code == 200


# # def test_get_todo():
# #     response = client.get("/{todo_id}/")
# #     assert response.status_code == 200


@temp_db
def test_create_todo():
    response = client.post(
        "/todos", json={"title": "temp_db_test", "description": "temp_db_test"}
    )
    assert response.status_code == 200

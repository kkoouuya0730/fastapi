from fastapi import FastAPI

from demo.routers import authentication, done, todos, user
from log.log import read_logger

read_logger()

app = FastAPI()

app.include_router(todos.router)
app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(done.router)

from fastapi import FastAPI

from demo.routers import todos, user, authentication

app = FastAPI()

app.include_router(todos.router)
app.include_router(user.router)
app.include_router(authentication.router)

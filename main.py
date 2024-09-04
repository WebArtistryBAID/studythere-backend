from fastapi import FastAPI

from routers import user, api

app = FastAPI()

app.include_router(user.router)
app.include_router(api.router)

import os

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers import user, api

app = FastAPI()

if os.environ.get("DEVELOPMENT") == "true":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(user.router)
app.include_router(api.router)

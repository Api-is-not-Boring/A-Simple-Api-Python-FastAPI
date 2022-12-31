from os import getenv
from fastapi import FastAPI
from app.router import v1

app = FastAPI(
    debug=True,
    title=getenv("NAME"),
    version=getenv("VERSION"),
    description=getenv("DESCRIPTION")
)

app.include_router(v1.router)

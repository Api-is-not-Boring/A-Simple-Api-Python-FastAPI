from fastapi import FastAPI, APIRouter, Header
from app.model.v1 import Ping, Info, Connections

router = APIRouter(prefix="/api/v1")


@router.get("/ping", response_model=Ping)
async def get_ping(user_agent: str | None = Header(default=None)):
    return Ping(agent=user_agent)


@router.get("/info", response_model=Info)
async def get_info():
    return Info()


@router.get("/connections", response_model=Connections)
async def get_connections():
    return Connections()

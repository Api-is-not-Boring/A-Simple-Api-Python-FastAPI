from fastapi import APIRouter, Header, Response, status
from fastapi.responses import RedirectResponse, JSONResponse
from app.model.v1 import Ping, Info, Connections

router = APIRouter(prefix="/api/v1")


@router.get("/", response_class=JSONResponse, status_code=status.HTTP_301_MOVED_PERMANENTLY)
async def router_redirect():
    return JSONResponse(
        status_code=status.HTTP_301_MOVED_PERMANENTLY,
        content={"status": "[router] -> 301 Redirect"},
        headers={"Location": "/api/v1/ping"}
    )


@router.get("/ping", response_model=Ping)
async def get_ping(user_agent: str | None = Header(default=None)):
    return Ping(agent=user_agent)


@router.get("/info", response_model=Info)
async def get_info():
    return Info()


@router.get("/connections", response_model=Connections)
async def get_connections():
    return Connections()

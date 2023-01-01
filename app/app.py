from os import getenv
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.router import v1, v2

app = FastAPI(
    debug=True,
    title=getenv("NAME"),
    version=getenv("VERSION"),
    description=getenv("DESCRIPTION")
)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": f"[router] -> {exc.status_code} {exc.detail}"}
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    code = status.HTTP_422_UNPROCESSABLE_ENTITY
    return JSONResponse(
        status_code=code,
        content={"status": f"[router] -> {code} Unprocessable Entity"}
    )

app.include_router(v1.router)
app.include_router(v2.router)

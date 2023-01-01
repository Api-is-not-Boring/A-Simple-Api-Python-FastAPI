from fastapi import APIRouter, Request, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, ExpiredSignatureError
from app.model.v3 import *

router = APIRouter(prefix="/api/v3")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.on_event("startup")
def on_startup():
    auth_db_init()


async def _token_check(token: str = Depends(oauth2_scheme)):
    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return v3_message("Token Valid", status.HTTP_200_OK)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )


@router.get("/auth", response_model=V3Message, response_model_exclude_none=True)
async def get_auth():
    return v3_message("Login with Post Request", status.HTTP_200_OK)


@router.post("/auth", response_model=V3Message, response_model_exclude_none=True)
async def post_auth(form_data: OAuth2PasswordRequestForm = Depends()):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == form_data.username)).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        if not verify_password(form_data.password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return v3_message("Login Successful !!!", t=create_access_token())


@router.get("/check", response_model=V3Message, response_model_exclude_none=True)
async def check_auth(m: V3Message = Depends(_token_check)):
    return m


@router.get("/secure", response_model=S3c5t, response_model_exclude_none=True, dependencies=[Depends(_token_check)])
async def get_secure():
    return S3c5t()

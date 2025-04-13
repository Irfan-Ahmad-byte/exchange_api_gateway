from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi import Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.api_clients.auth import AuthApiClient
from app.schemas.login_history import LoginHistoryOut
from app.schemas.user import UserCreate, UserOut
from app.schemas.token import Token
from app.utils.logs import get_logger

logger = get_logger(__name__)

router = APIRouter()
auth_client = AuthApiClient.prepare()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/register", response_model=UserOut)
async def register(payload: UserCreate):
    return await auth_client.register(payload.model_dump())

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends()
    ):
    return await auth_client.login(form_data)

@router.get("/me", response_model=UserOut)
async def get_me(token: str = Header("Authorization")):
    return await auth_client.get_user(token)

@router.post("/refresh", response_model=Token)
async def refresh_token(token: str = Header("Authorization")):
    return await auth_client.refresh(token)

@router.post("/logout")
async def logout(token: str = Header("Authorization")):
    return await auth_client.logout(token)

@router.get("/login-history", response_model=list[LoginHistoryOut])
async def login_history(token: str = Header("Authorization")):
    return await auth_client.get_login_history(token)
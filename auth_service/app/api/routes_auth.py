from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic
from app.usecases.auth import AuthUsecase
from app.api.deps import get_auth_uc, get_current_user_id

router = APIRouter(prefix="/auth", tags=["Authentication"])

# эндпоинты
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    data: RegisterRequest,
    uc: AuthUsecase = Depends(get_auth_uc)
):
    result = await uc.register(data.email, data.password)
    return result


@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    uc: AuthUsecase = Depends(get_auth_uc)
):
    token = await uc.login(form_data.username, form_data.password)
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserPublic)
async def get_me(
    user_id: int = Depends(get_current_user_id),
    uc: AuthUsecase = Depends(get_auth_uc)
):
    return await uc.get_current_user(user_id)

from fastapi import APIRouter, Depends, HTTPException

from app.schemas.user_schema import (
    UserLogin,
    UserRegister,
    UserResponse,
    TokenResponse,
)

from app.services.auth_service import AuthService
from app.dependencies.auth_dependency import get_current_user
from app.mappers.user_mapper import UserMapper


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


# --------------------------------
# Register
# --------------------------------

@router.post(
    "/register",
    response_model=TokenResponse,
)
async def register(user: UserRegister):

    created_user, token = await AuthService.register(user)

    return TokenResponse(
        access_token=token,
        user=UserMapper.to_response(created_user),
    )


# --------------------------------
# Login
# --------------------------------

@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(user: UserLogin):

    try:

        existing_user, token = await AuthService.login(user)

        return TokenResponse(
            access_token=token,
            user=UserMapper.to_response(existing_user),
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


# --------------------------------
# Get Current User
# --------------------------------

@router.get(
    "/me",
    response_model=UserResponse,
)
async def current_user(
    user=Depends(get_current_user),
):

    return UserMapper.to_response(user)
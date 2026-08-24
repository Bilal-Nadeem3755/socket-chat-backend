from app.repositories.user_repository import UserRepository
from app.core.security import (
    hash_password,
    create_access_token,
    verify_password,
)
from app.schemas.user_schema import UserRegister
from app.exceptions.custom_exceptions import(
    EmailAlreadyExists,
    InvalidCredentials,
    UsernameAlreadyExists
    )

class AuthService:

    @staticmethod
    

    async def register(user: UserRegister):

        # Check email
        existing_email = await UserRepository.get_user_by_email(
            user.email
        )

        if existing_email:
            raise EmailAlreadyExists()

        # Check username
        existing_username = await UserRepository.get_user_by_username(
            user.username
        )

        if existing_username:
            raise UsernameAlreadyExists()
        # Hash password
        hashed_password = hash_password(user.password)

        # Save user
        created_user = await UserRepository.create_user(
            full_name=user.full_name,
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
        )

        # JWT
        token = create_access_token(
            {
                "user_id": str(created_user["_id"]),
                "username": created_user["username"],
            }
        )

        return created_user, token
    
    @staticmethod
    async def login(user):

        # Find user
        existing_user = await UserRepository.get_user_by_email(
            user.email
        )

        if not existing_user:
            raise ValueError("Invalid email or password.")

        # Verify password
        password_valid = verify_password(
            user.password,
            existing_user["hashed_password"],
        )

        if not password_valid:
            raise ValueError("Invalid email or password.")

        # Create JWT
        token = create_access_token(
            {
                "user_id": str(existing_user["_id"]),
                "username": existing_user["username"],
            }
        )

        return existing_user, token

from pydantic import BaseModel, EmailStr, Field


# -----------------------------
# Register Request
# -----------------------------

class UserRegister(BaseModel):

    full_name: str = Field(
        min_length=3,
        max_length=50,
    )

    username: str = Field(
        min_length=3,
        max_length=20,
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=64,
    )


# -----------------------------
# Login Request
# -----------------------------

class UserLogin(BaseModel):

    email: EmailStr

    password: str


# -----------------------------
# Update Profile
# -----------------------------

class UserUpdate(BaseModel):

    full_name: str | None = Field(
        default=None,
        min_length=3,
        max_length=50,
    )

    username: str | None = Field(
        default=None,
        min_length=3,
        max_length=20,
    )

    profile_picture: str | None = None


# -----------------------------
# User Response
# -----------------------------

class UserResponse(BaseModel):

    id: str

    full_name: str

    username: str

    email: EmailStr

    is_online: bool

    profile_picture: str | None = None


# -----------------------------
# JWT Token Response
# -----------------------------

class TokenResponse(BaseModel):

    access_token: str

    token_type: str = "Bearer"

    user: UserResponse


# -----------------------------
# Generic Message
# -----------------------------

class MessageResponse(BaseModel):

    message: str
from fastapi import status


class AppException(Exception):

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ):
        super().__init__(message)

        self.message = message
        self.status_code = status_code
        

class EmailAlreadyExists(AppException):

    def __init__(self):

        super().__init__(
            message="Email already exists.",
            status_code=status.HTTP_409_CONFLICT,
        )


class UsernameAlreadyExists(AppException):

    def __init__(self):

        super().__init__(
            message="Username already exists.",
            status_code=status.HTTP_409_CONFLICT,
        )


class InvalidCredentials(AppException):

    def __init__(self):

        super().__init__(
            message="Invalid email or password.",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class UserNotFound(AppException):

    def __init__(self):

        super().__init__(
            message="User not found.",
            status_code=status.HTTP_404_NOT_FOUND,
        )        
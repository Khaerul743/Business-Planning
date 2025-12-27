from typing import Optional

from fastapi import status

from .base import BaseCustomeException


class EmailAlreadyExistsException(BaseCustomeException):
    """Exception raised when email is already registered."""

    def __init__(self, email: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "EMAIL_ALREADY_EXISTS",
                "message": "Email is already registered",
                "field": "email",
                "value": email,
            },
        )


class EmailNotFoundException(BaseCustomeException):
    """Exception raised when email is not found."""

    def __init__(self, email: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "EMAIL_NOT_FOUND",
                "message": "Email not found",
                "field": "email",
                "value": email,
            },
        )


class InvalidCredentialsException(BaseCustomeException):
    """Exception raised when credentials are invalid."""

    def __init__(self, email: str):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "INVALID_CREDENTIALS",
                "message": "Invalid email or password",
                "field": "credentials",
            },
        )


class PasswordTooWeakException(BaseCustomeException):
    """Exception raised when password doesn't meet requirements."""

    def __init__(self, message: str = "Password does not meet security requirements"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "PASSWORD_TOO_WEAK",
                "message": message,
                "field": "password",
            },
        )


class InvalidEmailFormatException(BaseCustomeException):
    """Exception raised when email format is invalid."""

    def __init__(self, email: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "INVALID_EMAIL_FORMAT",
                "message": "Invalid email format",
                "field": "email",
                "value": email,
            },
        )


class ValidationException(BaseCustomeException):
    """Exception raised when input validation fails."""

    def __init__(self, field: str, message: str, value: Optional[str] = None):
        detail = {"code": "VALIDATION_ERROR", "message": message, "field": field}
        if value is not None:
            detail["value"] = value

        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail
        )


class RemoveTokenError(BaseCustomeException):
    def __init__(self, message: str = "Internal server error, please try again later."):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": "REMOVE_TOKEN_FAILED",
                "message": message,
            },
        )


class NotAuthenticateException(BaseCustomeException):
    def __init__(self, field: str, message: str, value: Optional[str] = None):
        detail = {"code": "NOT_AUTHENTICATED", "message": message, "field": field}
        if value is not None:
            detail["value"] = value

        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class UnauthorizedException(BaseCustomeException):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "UNAUTHORIZED",
                "message": message,
            },
        )


class ForbiddenException(BaseCustomeException):
    def __init__(self, message: str = "forbidden"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "FORBIDDEN",
                "message": message,
            },
        )

from fastapi import status

from .base import BaseCustomeException


class JWTTokenExpired(BaseCustomeException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "TOKEN_EXPIRED",
                "message": "jwt token has expired",
            },
        )


class JWTInvalidToken(BaseCustomeException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "INVALID_TOKEN",
                "message": "invalid jwt token",
            },
        )

from fastapi import status

from .base import BaseCustomeException


class TokenIsNotVerified(BaseCustomeException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": "TOKEN_IS_NOT_VERIFIED",
                "message": "Token is not verified, please enter the correct token",
            },
        )


class WhatsappBadRequest(BaseCustomeException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "BAD_REQUEST",
                "message": "Bad request",
            },
        )

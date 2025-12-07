from fastapi import status

from .base import BaseCustomeException


class InternalServerError(BaseCustomeException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": "INTERNAL_SERVER_ERROR",
                "message": "Internal server error, please try again later.",
            },
        )

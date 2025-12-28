from fastapi import status

from .base import BaseCustomeException


class BusinessNotFound(BaseCustomeException):
    def __init__(self, message: str = "Business not found") -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "BUSINESS_NOT_FOUND",
                "message": message,
            },
        )

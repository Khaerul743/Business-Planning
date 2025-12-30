from fastapi import status

from .base import BaseCustomeException


class BusinessKnowladgeNotFound(BaseCustomeException):
    def __init__(self, message: str = "Business knowladge not found") -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "BUSINESS_KNOWLADGE_NOT_FOUND",
                "message": message,
            },
        )

from fastapi import status

from .base import BaseCustomeException


class FileLargeException(BaseCustomeException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "FILE_IS_TOO_LARGE",
                "message": "file is too large",
            },
        )

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


class BusinessIsAlreadyExist(BaseCustomeException):
    def __init__(self, message: str = "Business is already exist") -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "BUSINESS_IS_ALREAY_EXIST",
                "message": message,
            },
        )


class BusinessPermissionNeeded(BaseCustomeException):
    def __init__(
        self, message: str = "You don't have permission access for this business"
    ) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "DONT_HAVE_BUSINESS_PERMISSION_ACCESS",
                "message": message,
            },
        )

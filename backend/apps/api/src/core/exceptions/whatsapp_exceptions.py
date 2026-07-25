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


class ConversationNotFound(BaseCustomeException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "CONVERSATION_NOT_FOUND",
                "message": "Conversation not found, please enter the right id",
            },
        )


class CustomerNotFound(BaseCustomeException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "CUSTOMER_NOT_FOUND",
                "message": "customer not found, please enter the right id",
            },
        )


class WaBridgeException(BaseCustomeException):
    def __init__(self, message: str = "WhatsApp Bridge Service Error", status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        super().__init__(
            status_code=status_code,
            detail={
                "code": "WA_BRIDGE_ERROR",
                "message": message,
            },
        )

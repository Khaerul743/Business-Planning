from fastapi import status

from .base import BaseCustomeException


class AgentNotFound(BaseCustomeException):
    def __init__(self, message: str = "Agent not found") -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "AGENT_NOT_FOUND",
                "message": message,
            },
        )


class DocumentKnowladgeNotFound(BaseCustomeException):
    def __init__(self, message: str = "Document knowladge not found") -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "DOCUMENT_KNOWLADGE_NOT_FOUND",
                "message": message,
            },
        )

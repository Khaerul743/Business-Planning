from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from uuid import uuid4

import jwt
from fastapi import Request

from src.config import settings
from src.core.context.request_context import (
    current_user_email,
    current_user_id,
    current_user_role,
)
from src.core.exceptions import JWTInvalidToken, JWTTokenExpired, UnauthorizedException
from src.core.utils.logger import get_logger


class JWTHandler:
    def __init__(self):
        self.logger = get_logger(__name__)

    def create_access_token(
        self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None
    ):
        """
        Generate JWT token dengan payload dan expiry.
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + (
            expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        to_encode.update({"exp": expire})
        token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return token

    def create_refresh_token(self, user_id: str) -> str:
        payload = {
            "sub": user_id,
            "type": "refresh",
            "jti": uuid4().hex,
            "exp": datetime.utcnow() + timedelta(days=7),
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return token

    def verify_token(self, token: str):
        """
        Decode dan verifikasi JWT token.
        """
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            return payload
        except jwt.ExpiredSignatureError:
            self.logger.warning("Token expired")
            raise JWTTokenExpired()

        except jwt.PyJWTError as e:
            self.logger.warning(f"Invalid token: {str(e)}")
            raise JWTInvalidToken()

    async def jwt_required(self, request: Request):
        token = request.cookies.get("access_token")
        if not token:
            raise UnauthorizedException("Missing access token")

        payload = self.verify_token(token)
        if not payload:
            raise UnauthorizedException("Invalid token")

        # SET CONTEXTVAR
        current_user_id.set(payload["id"])
        current_user_email.set(payload["email"])
        current_user_role.set(payload["role"])


jwtHandler = JWTHandler()
